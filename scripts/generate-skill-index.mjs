#!/usr/bin/env node
import { execFileSync } from "node:child_process";
import { promises as fs } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const repo = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const excluded = new Set([".git", ".venv", "venv", "node_modules", "dist", "dist-ts", "build", "build-artifacts", "live-artifacts", "coverage", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".research", ".hypothesis", "vendor-readonly", "workspace", "site-packages"]);
const allowed = {
  "swietlik.orchestrator.recommended-agent": new Set(["fast_reader", "fast_worker", "standard_worker", "expert_worker", "deep_worker", "reviewer"]),
  "swietlik.orchestrator.minimum-agent": new Set(["fast_reader", "fast_worker", "standard_worker", "expert_worker", "deep_worker", "reviewer"]),
  "swietlik.orchestrator.reasoning": new Set(["low", "medium", "high", "xhigh"]),
  "swietlik.orchestrator.verbosity": new Set(["low", "medium", "high"]),
  "swietlik.orchestrator.delegation": new Set(["forbidden", "optional", "preferred", "required"]),
  "swietlik.orchestrator.review": new Set(["none", "optional", "auto", "required"]),
  "swietlik.orchestrator.parallel": new Set(["forbidden", "allowed", "preferred"]),
  "swietlik.orchestrator.risk": new Set(["low", "medium", "high", "critical"]),
};

function scalar(value) {
  const trimmed = value.trim();
  if (trimmed.startsWith('"')) return JSON.parse(trimmed);
  if (trimmed.startsWith("'") && trimmed.endsWith("'")) return trimmed.slice(1, -1).replace(/''/g, "'");
  return trimmed;
}

function topLevelValue(lines, key) {
  const pattern = new RegExp(`^${key}:\\s*(.*)$`);
  for (let index = 0; index < lines.length; index += 1) {
    const match = lines[index].match(pattern);
    if (!match) continue;
    const value = match[1] ?? "";
    if (/^[>|]/.test(value.trim())) {
      const chunks = [];
      for (let next = index + 1; next < lines.length && /^\s+/.test(lines[next]); next += 1) chunks.push(lines[next].trim());
      return chunks.join(value.trim().startsWith(">") ? " " : "\n").trim();
    }
    return scalar(value);
  }
  throw new Error(`Missing ${key}`);
}

function parseSkill(text, filePath) {
  const normalized = text.replace(/^\uFEFF/, "").replace(/\r\n/g, "\n");
  if (!normalized.startsWith("---\n")) throw new Error(`${filePath}: missing frontmatter`);
  const end = normalized.indexOf("\n---\n", 4);
  if (end < 0) throw new Error(`${filePath}: unterminated frontmatter`);
  const lines = normalized.slice(4, end).split("\n");
  const name = topLevelValue(lines, "name");
  const description = topLevelValue(lines, "description");
  if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(name) || name.length > 64) throw new Error(`${filePath}: invalid skill name`);
  if (description.length < 24 || description.length > 1024) throw new Error(`${filePath}: description length is ${description.length}`);
  const metadataStart = lines.findIndex((line) => line === "metadata:");
  if (metadataStart < 0) throw new Error(`${filePath}: metadata missing`);
  const metadata = {};
  for (let index = metadataStart + 1; index < lines.length; index += 1) {
    const match = lines[index].match(/^\s{2}([^:]+):\s*(.*)$/);
    if (!match) {
      if (!/^\s/.test(lines[index])) break;
      continue;
    }
    metadata[match[1]] = scalar(match[2]);
  }
  for (const [key, values] of Object.entries(allowed)) {
    if (typeof metadata[key] !== "string" || !values.has(metadata[key])) throw new Error(`${filePath}: invalid ${key}`);
  }
  if (metadata["swietlik.orchestrator.schema"] !== "1") throw new Error(`${filePath}: invalid metadata schema`);
  return { name, description, metadata };
}

async function discover(directory, results = []) {
  const entries = await fs.readdir(directory, { withFileTypes: true });
  for (const entry of entries) {
    if (entry.isSymbolicLink()) continue;
    const fullPath = path.join(directory, entry.name);
    if (entry.isDirectory() && !excluded.has(entry.name)) await discover(fullPath, results);
    else if (entry.isFile() && entry.name === "SKILL.md") results.push(fullPath);
  }
  return results;
}

function git(...args) {
  return execFileSync("git", ["-C", repo, ...args], { encoding: "utf8", windowsHide: true }).trim();
}

function stable(index) {
  const { source_commit, generated_at, ...rest } = index;
  return rest;
}

const manifestText = await fs.readFile(path.join(repo, "pack.yaml"), "utf8");
const manifestLines = manifestText.replace(/\r\n/g, "\n").split("\n");
const manifestKeys = manifestLines.flatMap((line) => {
  const match = line.match(/^([a-z_]+):/);
  return match ? [match[1]] : [];
});
const expectedManifestKeys = ["schema_version", "id", "description", "source", "index_schema_version"];
if (JSON.stringify([...manifestKeys].sort()) !== JSON.stringify([...expectedManifestKeys].sort())) {
  throw new Error(`pack.yaml must contain exactly: ${expectedManifestKeys.join(", ")}`);
}
const manifestSchema = topLevelValue(manifestLines, "schema_version");
const packId = topLevelValue(manifestLines, "id");
const packDescription = topLevelValue(manifestLines, "description");
const source = topLevelValue(manifestLines, "source");
const indexSchema = topLevelValue(manifestLines, "index_schema_version");
if (manifestSchema !== "1" || indexSchema !== "1") throw new Error("pack.yaml schema versions must equal 1");
if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(packId)) throw new Error("pack.yaml id is invalid");
if (packDescription.length < 24 || packDescription.length > 1024) throw new Error("pack.yaml description length is invalid");
if (!/^https:\/\/github\.com\/Swietlik3d\/[A-Za-z0-9._-]+$/.test(source)) throw new Error("pack.yaml source is not trusted");
const files = (await discover(repo)).sort((a, b) => a.localeCompare(b));
const names = new Map();
const skills = [];
for (const filePath of files) {
  const parsed = parseSkill(await fs.readFile(filePath, "utf8"), path.relative(repo, filePath));
  if (parsed.metadata["swietlik.orchestrator.pack"] !== packId) throw new Error(`${filePath}: metadata pack mismatch`);
  if (names.has(parsed.name)) throw new Error(`Duplicate skill ${parsed.name}: ${names.get(parsed.name)} and ${filePath}`);
  names.set(parsed.name, filePath);
  skills.push({
    name: parsed.name,
    description: parsed.description,
    path: path.relative(repo, filePath).split(path.sep).join("/"),
    execution_metadata: parsed.metadata,
  });
}
skills.sort((a, b) => a.name.localeCompare(b.name));
const sourceCommit = git("rev-parse", "HEAD");
const epoch = process.env.SOURCE_DATE_EPOCH;
const generatedAt = epoch ? new Date(Number(epoch) * 1000).toISOString() : new Date(git("show", "-s", "--format=%cI", "HEAD")).toISOString();
const index = { schema_version: 1, pack_id: packId, source_repository: source, source_commit: sourceCommit, generated_at: generatedAt, skills };
const outputPath = path.join(repo, "skills-index.json");
if (process.argv.includes("--check")) {
  const existing = JSON.parse(await fs.readFile(outputPath, "utf8"));
  const indexKeys = Object.keys(existing).sort();
  const expectedIndexKeys = ["schema_version", "pack_id", "source_repository", "source_commit", "generated_at", "skills"].sort();
  if (JSON.stringify(indexKeys) !== JSON.stringify(expectedIndexKeys) || existing.schema_version !== 1) {
    throw new Error("skills-index.json envelope is invalid");
  }
  if (JSON.stringify(stable(existing)) !== JSON.stringify(stable(index))) {
    throw new Error("skills-index.json is stale; run node scripts/generate-skill-index.mjs");
  }
  console.log(JSON.stringify({ ok: true, pack: packId, skills: skills.length }));
} else {
  const temporary = `${outputPath}.${process.pid}.tmp`;
  await fs.writeFile(temporary, `${JSON.stringify(index, null, 2)}\n`);
  await fs.rename(temporary, outputPath);
  console.log(JSON.stringify({ ok: true, pack: packId, skills: skills.length, output: outputPath }));
}
