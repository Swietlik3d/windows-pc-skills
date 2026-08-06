$Repo=(Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
Describe 'Router and toolkit' {
 It 'routes boot, storage and update examples to exactly one expected primary' {
  $cases=@(
   @('Laptop zapętla Automatic Repair po aktualizacji, dysk nie klika','windows-boot-recovery'),
   @('Dysk klika, SMART critical i komputer zamiera przy kopiowaniu','storage-triage-cloning-recovery'),
   @('Windows Update 0x800f0922 ciągle wraca po restarcie','windows-update-servicing')
  )
  foreach($case in $cases){
   $json=& python (Join-Path $Repo 'scripts\repo\route_issue.py') --text $case[0] --json
   $result=$json|ConvertFrom-Json
   if($result.primary -ne $case[1]){throw "Router '$($case[0])' -> $($result.primary), expected $($case[1])"}
   if(@($result.supporting).Count -gt 3){throw 'Router returned more than three supporting skills'}
  }
 }
 It 'queries release and tool registries without network access' {
  $matrix=& python (Join-Path $Repo 'scripts\repo\query_matrix.py') --os windows-11 --build 26100
  if(@(($matrix|ConvertFrom-Json).matches).Count -ne 1){throw 'Release matrix query failed'}
  $tools=& python (Join-Path $Repo 'scripts\repo\query_tools.py') --use-case network --os 'Windows 11' --arch x64
  if(@(($tools|ConvertFrom-Json).results).Count -lt 1){throw 'Tool query returned no result'}
 }
 It 'generates a no-download service-media plan' {
  $out=Join-Path $TestDrive 'media-plan.json'
  $plan=& (Join-Path $Repo 'scripts\toolkit\New-ServiceMediaPlan.ps1') -ManifestPath (Join-Path $Repo 'tools\manifests\service-media.yaml') -OutputPath $out
  if($plan.downloads_performed -ne 0 -or $plan.usb_writes_performed -ne 0){throw 'Service media plan performed a mutation'}
 }
 It 'returns downloader metadata without downloading when no asset URL is supplied' {
  $plan=& (Join-Path $Repo 'scripts\toolkit\Get-VerifiedServiceTool.ps1') -ToolId rufus -Destination (Join-Path $TestDrive 'tools') -WhatIf
  if($plan.will_execute){throw 'Downloader plan claims execution'}
  if(Test-Path (Join-Path $TestDrive 'tools')){throw 'Downloader plan created destination unexpectedly'}
 }
 It 'keeps knowledge and tool refreshes review-only under WhatIf' {
  $knowledgeOut=Join-Path $TestDrive 'knowledge-candidate.json'
  $toolsOut=Join-Path $TestDrive 'tool-candidate.json'
  $knowledge=& (Join-Path $Repo 'scripts\repo\Update-WindowsKnowledgeBase.ps1') -Fetch -OutputPath $knowledgeOut -WhatIf
  $tools=& (Join-Path $Repo 'scripts\repo\Update-ToolCatalog.ps1') -Fetch -OutputPath $toolsOut -MaxTools 2 -WhatIf
  if($knowledge.auto_accept -ne $false -or $tools.auto_accept -ne $false){throw 'Refresh plan allows automatic acceptance'}
  if(Test-Path -LiteralPath $knowledgeOut){throw 'Knowledge WhatIf wrote a candidate'}
  if(Test-Path -LiteralPath $toolsOut){throw 'Tool WhatIf wrote a candidate'}
 }
}
