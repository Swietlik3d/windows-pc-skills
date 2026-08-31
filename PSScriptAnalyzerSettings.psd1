@{
    Severity = @('Error', 'Warning')
    # Repair wrappers intentionally share one stable parameter contract even when a
    # specific backend does not consume every selector.
    ExcludeRules = @('PSAvoidUsingWriteHost', 'PSReviewUnusedParameter')
    Rules = @{
        PSAvoidUsingCmdletAliases = @{ Enable = $true }
        PSUseShouldProcessForStateChangingFunctions = @{ Enable = $true }
        PSUseDeclaredVarsMoreThanAssignments = @{ Enable = $true }
    }
}
