$Repo = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
Describe 'Skill structure' {
 It 'contains exactly 39 skills and no shared SKILL.md' {
  $skills=@(Get-ChildItem -LiteralPath (Join-Path $Repo '.agents\skills') -Directory|Where-Object Name -ne '_shared')
  if($skills.Count -ne 39){throw "Expected 39 skills, got $($skills.Count)"}
  if(Test-Path -LiteralPath (Join-Path $Repo '.agents\skills\_shared\SKILL.md')){throw '_shared contains SKILL.md'}
 }
 It 'has no unresolved creator placeholders' {
  $hits=@(Get-ChildItem (Join-Path $Repo '.agents\skills') -Recurse -File|Select-String -Pattern '\[TODO|TODO: Complete')
  if($hits.Count -ne 0){throw "Creator placeholders found: $($hits.Count)"}
 }
}
