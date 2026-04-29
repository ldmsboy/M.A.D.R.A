# Run tests using pytest in the virtual environment
if (Test-Path .venv) {
    . .venv\Scripts\Activate.ps1
}
pytest -q
