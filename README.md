# Budget Tracker

Simple terminal-based budget tracker that stores categories and expenses in a JSON file.

## Features

- Add expenses (amount, category, description, date)
- View all expenses
- View expenses for a specific month
- Delete saved expenses
- Add custom categories
- Generate a monthly category report

## Requirements

- Python 3.8+

## Install

1. (Optional) Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. No external dependencies are required.

## Run

From the project directory run:

```powershell
python .\budget_tracker.py
```

The app stores data in `expenses.json` in the same folder.

## Usage

Follow the numbered menu to add/view/delete expenses and run reports. Dates use `YYYY-MM-DD` format.

## Files

- `budget_tracker.py` — main program
- `expenses.json` — persisted data file (created automatically)

## License

This project is provided as-is for personal use.
A simple budget tracker app.
