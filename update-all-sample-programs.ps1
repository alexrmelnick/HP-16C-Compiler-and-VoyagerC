# Save the current location
$originalLocation = Get-Location

# Navigate to the '/tests/Jovial Assembler (.jov)' folder
$sourceFolder = "./tests/Jovial Assembler (.jov)"
Set-Location -Path $sourceFolder

# Define the target folders with relative paths
$targetFolderTXT = "../HP16C Emulator (.txt)"
$targetFolder16C = "../JRPN Simulator (.16c)"
$targetFolderPDF = "../Keystroke Programming (.pdf)"

# Ensure target folders exist
$folders = @($targetFolderTXT, $targetFolder16C, $targetFolderPDF)
foreach ($folder in $folders) {
    if (-not (Test-Path -Path $folder)) {
        New-Item -ItemType Directory -Path $folder
    }
}

# Process each .jov file in the source folder
Get-ChildItem -Path "." -Filter *.jov | ForEach-Object {
    $file = $_.Name
    $baseName = [System.IO.Path]::GetFileNameWithoutExtension($file)
    
    # Define the output file paths
    $output16C = "$baseName.16c"
    $outputTXT = "$baseName.txt"
    $outputPDF = "$baseName.pdf"

    # Run the commands to generate the files
    jovial -i $file -o $output16C -d WARNING
    jovial -i $file -o $outputTXT -d WARNING
    jovial -i $file -o $outputPDF -d WARNING

    # Move the files to their respective folders (replacing if they already exist)
    Move-Item -Path $output16C -Destination "$targetFolder16C/$output16C" -Force
    Move-Item -Path $outputTXT -Destination "$targetFolderTXT/$outputTXT" -Force
    Move-Item -Path $outputPDF -Destination "$targetFolderPDF/$outputPDF" -Force
}

# Navigate back to the original location
Set-Location -Path $originalLocation
