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

$accDir = Join-Path $Dir 'acc/'
if (!(Test-Path $accDir)) {
    mkdir $accDir
}
$strs = adb shell ls '/sdcard/tangoLogger/' | Select-String -Pattern "$Datetime.*_android.sensor.accelerometer.csv"
foreach ($s in $strs) {
    adb pull "/sdcard/tangoLogger/$($s.Line)" $accDir
}

$poseDir = Join-Path $Dir 'pose/'
if (!(Test-Path $poseDir)) {
    mkdir $poseDir
}
$strs = adb shell ls '/sdcard/tangoLogger/' | Select-String -Pattern "$Datetime.*_cameraPose.csv"
foreach ($s in $strs) {
    adb pull "/sdcard/tangoLogger/$($s.Line)" $poseDir
}
