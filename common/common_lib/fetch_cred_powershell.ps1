#-=-=-=-=-= FETCH_CRED macro start -=-=-=-=-=
function fetch_cred([string] $user_label){

    function get_ccp_creds([string] $ccp_endpoint, [string] $ccp_endpoint_service, [string] $ccp_app_id, [string] $ccp_safe, [string] $ccp_virtuser){
        $url = "https://$ccp_endpoint/$ccp_endpoint_service/api/Accounts?AppId=$ccp_app_id&Query=Safe=$ccp_safe;VirtualUserName=$ccp_virtuser"
        try {
            $response = Invoke-RestMethod -Uri $url -Method Get
        } catch {
            Write-Host "get_ccp_creds: Received $($_.Exception.Response.StatusCode.value__) response: $_" -ForegroundColor Red
            return $null
        }
        return @{username=$response.UserName+'@'+$response.Address; secret=$response.Content}
    }

    $cred_config = @"
@@{CRED_CONFIG}@@
"@ | ConvertFrom-Json

    $virt_user = $cred_config.virtual_users.$user_label.vuser
    $ccp_safe = $cred_config.virtual_users.$user_label.safe
    if ($null -eq $ccp_safe) {
        $ccp_safe = $cred_config.ccp_default_safe
    }
    $ccp_endpoint = $cred_config.ccp_endpoint
    $ccp_endpoint_service = $cred_config.ccp_endpoint_service
    $ccp_app_id = $cred_config.ccp_app_id

    Write-Host "Retrieving credentials for $virt_user from CyberArk..."
    $cred = get_ccp_creds $ccp_endpoint $ccp_endpoint_service $ccp_app_id $ccp_safe $virt_user

    Write-Host "Returning credentials to caller." -ForegroundColor Green
    return $cred
}
#-=-=-=-=-= FETCH_CRED macro end -=-=-=-=-=