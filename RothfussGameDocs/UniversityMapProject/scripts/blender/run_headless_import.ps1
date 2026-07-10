param(
    [string]$JsonPath = "data\buildings\archives_ground_v02_canon_safe.json",
    [string]$OutputBlend = "exports\blender\archives_ground_v02_canon_safe.blend",
    [string]$OutputGlb = "godot\assets\archives_ground_v02_canon_safe.glb",
    [string]$BlenderExe = ""
)

$ErrorActionPreference = "Stop"

$ProjectDir = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $PSCommandPath))
$Importer = Join-Path $ProjectDir "scripts\blender\import_floor_plan.py"
$ResolvedJson = Join-Path $ProjectDir $JsonPath
$ResolvedOutput = Join-Path $ProjectDir $OutputBlend
$ResolvedGlb = Join-Path $ProjectDir $OutputGlb

if (-not (Test-Path -LiteralPath $ResolvedJson)) {
    throw "JSON source not found: $ResolvedJson"
}

if (-not (Test-Path -LiteralPath $Importer)) {
    throw "Blender importer not found: $Importer"
}

if ([string]::IsNullOrWhiteSpace($BlenderExe)) {
    $command = Get-Command blender -ErrorAction SilentlyContinue
    if ($command) {
        $BlenderExe = $command.Source
    }
}

if ([string]::IsNullOrWhiteSpace($BlenderExe) -or -not (Test-Path -LiteralPath $BlenderExe)) {
    throw "Blender executable not found. Pass -BlenderExe 'C:\Path\To\blender.exe' or add Blender to PATH."
}

New-Item -ItemType Directory -Force -Path (Split-Path -Parent $ResolvedOutput) | Out-Null
New-Item -ItemType Directory -Force -Path (Split-Path -Parent $ResolvedGlb) | Out-Null

& $BlenderExe --background --python $Importer -- $ResolvedJson --clear-scene --save-blend $ResolvedOutput --export-glb $ResolvedGlb
