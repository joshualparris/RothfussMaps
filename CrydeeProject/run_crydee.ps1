param(
    [switch]$PipelineOnly,
    [switch]$GodotOnly,
    [switch]$SkipPipeline
)

$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
$pythonExe = "C:\Users\joshua.parris\AppData\Local\Python\pythoncore-3.14-64\python.exe"
$pipelineScript = Join-Path $PSScriptRoot "run_pipeline.py"
$godotExe = Join-Path $PSScriptRoot "Godot_v4.6.2-stable_win64.exe\Godot_v4.6.2-stable_win64.exe"
$godotProject = Join-Path $PSScriptRoot "godot"

if (-not (Test-Path -LiteralPath $pythonExe)) {
    throw "Python executable not found at $pythonExe"
}

if (-not (Test-Path -LiteralPath $pipelineScript)) {
    throw "Pipeline script not found at $pipelineScript"
}

if (-not (Test-Path -LiteralPath $godotExe)) {
    throw "Godot executable not found at $godotExe"
}

Push-Location $projectRoot
try {
    if (-not $GodotOnly -and -not $SkipPipeline) {
        & $pythonExe $pipelineScript --stage all --force
    }

    if (-not $PipelineOnly) {
        & $godotExe --path $godotProject
    }
}
finally {
    Pop-Location
}
