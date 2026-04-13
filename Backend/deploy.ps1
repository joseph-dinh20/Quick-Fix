param(
    [Alias("r")]
    [switch]$RunOnly
)
param(
    [switch]$RunOnly
)


$ErrorActionPreference = "Stop"

try {
    if ($RunOnly) {
        Write-Host "Starting development server only..." -ForegroundColor Green
        uv run python manage.py runserver

        if ($LASTEXITCODE -ne 0) {
            throw "runserver failed with exit code $LASTEXITCODE"
        }

        exit 0
    }

    Write-Host "Running makemigrations..." -ForegroundColor Cyan
    uv run python manage.py makemigrations

    if ($LASTEXITCODE -ne 0) {
        throw "makemigrations failed with exit code $LASTEXITCODE"
    }

    Write-Host "Running migrate..." -ForegroundColor Cyan
    uv run python manage.py migrate

    if ($LASTEXITCODE -ne 0) {
        throw "migrate failed with exit code $LASTEXITCODE"
    }

    Write-Host "Starting development server..." -ForegroundColor Green
    uv run python manage.py runserver

    if ($LASTEXITCODE -ne 0) {
        throw "runserver failed with exit code $LASTEXITCODE"
    }
}
catch {
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
finally {
    Write-Host "Script finished." -ForegroundColor Yellow
}