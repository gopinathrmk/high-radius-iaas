$uname = "@@{Domain_Admin.username}@@"
$passwd = ConvertTo-SecureString -AsPlainText '@@{Domain_Admin.secret}@@' -Force
$cred = New-Object System.Management.Automation.PSCredential ($uname,$passwd)
$vm = "@@{vmname}@@"
Write-Output "Finding Computer Object $vm in Active Directory"
$CompObj = Get-ADComputer -Identity "@@{name}@@" -Credential $Cred -Verbose
if(!$CompObj)
    { 
    Write-Output "AD Computer Object $vm not found"
    }
else
    {
    $Identity = $CompObj.DistinguishedName
    Remove-ADObject -Identity $Identity -Credential $Cred -Confirm:$False
    Write-Output "AD Computer Object $vm was deleted from Active Directory" 
    }-Force