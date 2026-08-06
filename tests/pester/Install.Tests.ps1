$Repo=(Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
Describe 'Install manifest lifecycle' {
 It 'installs 39 and uninstalls only manifest-owned unchanged copies' {
  $dest=Join-Path $TestDrive 'skills'
  $install=& (Join-Path $Repo 'scripts\repo\Install-WindowsMasterSkills.ps1') -Destination $dest -Source (Join-Path $Repo '.agents\skills') -Mode Copy
  if($install.Installed -ne 39){throw "Installed $($install.Installed), expected 39"}
  & (Join-Path $Repo 'scripts\repo\Uninstall-WindowsMasterSkills.ps1') -Destination $dest -Confirm:$false|Out-Null
  if(@(Get-ChildItem $dest -Directory|Where-Object Name -notmatch '^\.').Count -ne 0){throw 'Installed skill directories remained'}
 }
 It 'keeps installer and packager WhatIf free of filesystem mutations' {
  $installDest=Join-Path $TestDrive 'whatif-install'
  $packageDest=Join-Path $TestDrive 'whatif-packages'
  & (Join-Path $Repo 'scripts\repo\Install-WindowsMasterSkills.ps1') -Destination $installDest -Source (Join-Path $Repo '.agents\skills') -Mode Copy -WhatIf|Out-Null
  & (Join-Path $Repo 'scripts\repo\Build-SkillPackages.ps1') -Destination $packageDest -WhatIf|Out-Null
  if(Test-Path -LiteralPath $installDest){throw 'Installer WhatIf created a destination'}
  if(Test-Path -LiteralPath $packageDest){throw 'Packager WhatIf created a destination'}
 }
 It 'uses self-contained dist packages as the default install source' {
  $dest=Join-Path $TestDrive 'packaged-skills'
  $install=& (Join-Path $Repo 'scripts\repo\Install-WindowsMasterSkills.ps1') -Scope User -Destination $dest -Mode Copy
  $shared=Join-Path $dest 'windows-master-router\references\_shared\schemas\playbook.schema.json'
  if($install.Installed -ne 39 -or -not(Test-Path -LiteralPath $shared)){throw 'Default install was not self-contained'}
  & (Join-Path $Repo 'scripts\repo\Uninstall-WindowsMasterSkills.ps1') -Scope User -Destination $dest -Confirm:$false|Out-Null
 }
}
