$compName = $env:computername
$domname = "@@{DOMAIN}@@"
$oupath = "@@{OU}@@"
$uname = "@@{Domain_Admin.username}@@"
$passwd = ConvertTo-SecureString -AsPlainText '@@{Domain_Admin.secret}@@' -Force

$cred = New-Object System.Management.Automation.PSCredential ($uname,$passwd)

Write-Output "$(Get-Date) [INFO] Attempting to join $compName to $domname"
Write-Output ""

Install-windowsfeature -name AD-Domain-Services -IncludeManagementTools

Try {

	# join domain
	Add-Computer -DomainName $domname -OUPath $oupath -Credential $cred -Restart -Force -ErrorAction Stop -Verbose
    # Add-Computer -DomainName $domname -Credential $cred -Restart -Force -ErrorAction Stop

} Catch {

	Write-Output "$(Get-Date) [ERROR] Joining domain failed"
	# send exit code to Calm to stop provisioning process
	exit 1
    
}

Write-Output "$(Get-Date) [INFO] $compName succesfully joined to $domname"