#converting password to something we can use
$adminpassword = ConvertTo-SecureString -asPlainText -Force -String "@@{active_directory.secret}@@"

#creating the credentials object based on the Calm variables
$credential = New-Object System.Management.Automation.PSCredential("@@{active_directory.username}@@",$adminpassword)

#unjoining the domain
$vm = "@@{hostname}@@"

Write-Output "Finding the Computer Object $vm in Active Directory"
$CompObj = Get-ADComputer -Identity $vm -Credential $credential -Verbose

if(!$CompObj)
    {
    Write-Output "Ad Computer Object $vm not found"
    }
else
    {
    $Identity = $CompObj.DistinguishedName
    Remove-ADObject -Identity $Identity -Credential $credential -Confirm:$false
    Write-Output "AD Computer Object $vm was deleted from Active Directory"
    }