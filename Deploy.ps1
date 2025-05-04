param(
    [Parameter(Mandatory=$true)]
    [string]$Version
)

# Validate version format
if (-not ($Version -match '^\d+\.\d+\.\d+$')) {
    Write-Error "Version must be in format: X.Y.Z (e.g. 1.2.3)"
    exit 1
}

# Update version in pyproject.toml
$pyprojectPath = "pyproject.toml"
if (Test-Path $pyprojectPath) {
    Write-Host "Updating version in $pyprojectPath to $Version..."
    $content = Get-Content -Path $pyprojectPath -Raw
    $newContent = $content -replace 'version = "[0-9]+\.[0-9]+\.[0-9]+"', "version = `"$Version`""
    Set-Content -Path $pyprojectPath -Value $newContent -NoNewline
    Write-Host "✓ Updated $pyprojectPath"
}
else {
    Write-Warning "$pyprojectPath not found"
}

# Update version in main.py
$mainPyPath = "main.py"
if (Test-Path $mainPyPath) {
    Write-Host "Updating version in $mainPyPath to $Version..."
    $content = Get-Content -Path $mainPyPath -Raw
    $newContent = $content -replace 'APP_VERSION = "[0-9]+\.[0-9]+\.[0-9]+"', "APP_VERSION = `"$Version`""
    Set-Content -Path $mainPyPath -Value $newContent -NoNewline
    Write-Host "✓ Updated $mainPyPath"
}
else {
    Write-Warning "$mainPyPath not found"
}

# Update uv.lock
$uvLockPath = "uv.lock"
if (Test-Path $uvLockPath) {
    Write-Host "Updating version in $uvLockPath..."
    
    if (Get-Command uv -ErrorAction SilentlyContinue) {
        # Regenerate the lock file with uv
        uv lock
        Write-Host "✓ Updated $uvLockPath using uv lock"
    }
    else {
        Write-Warning "uv command not found. Please install uv or manually update the lock file."
    }
}
else {
    Write-Warning "$uvLockPath not found"
}

# Create git tag if git is available
if (Get-Command git -ErrorAction SilentlyContinue) {
    $tagName = "v$Version"
    
    # Check if tag already exists
    $tagExists = git tag -l $tagName
    
    if ($tagExists) {
        Write-Warning "Tag $tagName already exists. Skipping tag creation."
    }
    else {
        Write-Host "Creating git tag $tagName..."
        git tag $tagName
        Write-Host "✓ Created tag $tagName"
    }
    
    Write-Host "Committing changes..."
    git add $pyprojectPath $mainPyPath $uvLockPath
    git commit -m "Increase version to $Version"
    Write-Host "✓ Committed changes"
    
    Write-Host "Pushing changes and tag..."
    git push
    git push origin $tagName
    Write-Host "✓ Pushed changes and tag"
}
else {
    Write-Warning "Git not found. Skipping tag creation and commit/push operations."
}

Write-Host "`nVersion updated to $Version successfully!"