# Smart Virtual Assistant - assistant-team05

Smart Virtual Assistant is a reproducible Python application developed for CSC10014 (Practical Track, Faculty of Information Technology, University of Science, VNU-HCM). It provides an automated command-line assistant to answer student queries about university offices, room numbers, and operating hours.

## Setup
Prerequisites: Python 3.10+, Git.

```bash
git clone https://github.com/tlkha06112007/assistant-team05.git
cd assistant-team05
python -m venv .venv
source .venv/bin/activate       # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -e .
```

## Run
```bash
python -m assistant "where is the training office?"
# -> Training Office: room I.101, open Mon-Fri 07:30-16:30.
```

## Test
```bash
pytest -q                       # -> 4 passed
```

## Project structure
- `src/`: application code (backend package `assistant`)
- `tests/`: automated smoke tests
- `docs/`: blueprints, reports, and team documentation
- `data/`: sample dataset (`offices.csv`) and data source notes
- `ui/`: user interface specifications and assets (from Week 7)
- `scripts/`: helper scripts and environment verification (`check_env.py`)

## Troubleshooting
- "No module named assistant" -> you forgot `pip install -e .` or the venv is not active.
- PowerShell blocks Activate.ps1 -> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`
- python: command not found (Windows) -> use `py`, or reinstall Python with "Add to PATH" checked.
- .venv/ shows up in git status -> add `.venv/` to `.gitignore`; if already committed: `git rm -r --cached .venv`.
- pip installs into the wrong Python -> always use `python -m pip ...` inside the active venv.
- Vietnamese characters garbled in CSV -> open files with `encoding="utf-8"`.