@{
    Severity = @('Error', 'Warning')
    ExcludeRules = @('PSAvoidUsingWriteHost')
    Rules = @{
        PSAvoidUsingCmdletAliases = @{ Enable = $true }
        PSUseShouldProcessForStateChangingFunctions = @{ Enable = $true }
        PSUseDeclaredVarsMoreThanAssignments = @{ Enable = $true }
    }
}
