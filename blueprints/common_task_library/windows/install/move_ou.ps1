# Requires CredSSP enabled on the target computer!
#   Enable-WSManCredSSP -Role Server -Force


$ErrorActionPreference = "Stop"


#region Capture Macros

# OU to move the computer to
$ouPath = "@@{ou_path}@@"

#endregion


#region Move OU

# Creates directory search filter to find target OU
$ouSearcher = New-Object -TypeName System.DirectoryServices.DirectorySearcher -ArgumentList "distinguishedName=$ouPath"

# Creates directory search filter to find computer
$computerSearcher = New-Object -TypeName System.DirectoryServices.DirectorySearcher -ArgumentList "(SAMAccountName=$($env:COMPUTERNAME)$)"

# Initializes the directory search and gets result
$ouObject = $ouSearcher.FindOne().GetDirectoryEntry()
$computerResult = $computerSearcher.FindOne()

try {
    Out-Host -InputObject "Attempting to move the computer object to: $($ouObject.Properties.distinguishedname)"
    
    # Gets the directory entry from the result and executes the move method
    $computerResult.GetDirectoryEntry().PSBase.MoveTo($ouObject)
}
catch {
    Out-Host -InputObject $ouObject
    Out-Host -InputObject $computerResult
    
    Throw "Couldn't find OU or Computer!"
}

# Refresh computer
$computerResult = $computerSearcher.FindOne()

if ($computerResult.Path -like "*$ouPath") {
    # Check if the computer moved OUs
    Out-Host -InputObject "Computer object move successful!"
}

#endregion