Param (
    [parameter(mandatory=$True)] $Datetime,
    $Dir = (Join-Path $PSScriptRoot 'raw/')
)

if (!(Test-Path $Dir)) {
    "$Dir was not found"
    exit
}

if (!(Get-Item $Dir).PSIsContainer) {
    "$Dir is not directory"
    exit
}

$strs = adb shell ls '/sdcard/tangoLogger/' | Select-String -Pattern "$Datetime.*_cameraPose.csv"

foreach ($s in $strs) {
    adb pull "/sdcard/tangoLogger/$($s.Line)" $Dir
}
