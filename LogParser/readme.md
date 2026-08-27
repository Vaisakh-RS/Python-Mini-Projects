# LogParser

A small Python tool that parses log files into structured objects, queries them by severity, and correlates error entries with data from an external API. Built as a hands-on practice project covering OOP, file I/O, error handling, logging, API integration, and testing.

## Features

- **Structured log parsing** — reads a log file and converts each line into a `LogEntry` object (timestamp, severity, message)
- **Graceful error handling** — malformed lines are logged as warnings and skipped, rather than crashing the whole run
- **Logging, not print debugging** — dual output to console and `app.log`, with configurable severity levels
- **Query methods** — filter entries by severity, get counts per severity level
- **External API correlation** — fetches supplementary data for error entries via a REST API, with proper error/timeout handling
- **Tested** — unit tests for core parsing and query logic using pytest

## Project structure

```
LogParser/
├── src/
│   ├── LogParser.py     # LogEntry + LogParser classes
│   ├── ApiTest.py       # fetchApi class (external API client)
│   └── Combine.py       # coordinates LogParser + fetchApi
├── tests/
│   └── test_log_parser.py
├── sample.log            # sample log data for testing/demo
├── requirements.txt
└── README.md
```

## Setup

```bash
# clone the repo, then from the project root:
python -m venv venv
venv\Scripts\Activate.ps1      # Windows PowerShell
pip install -r requirements.txt
```

## Usage

Run the correlation pipeline from the project root:

```bash
python -m src.Combine
```

This parses `sample.log`, filters for `ERROR` entries, fetches an external data point for each, and returns a combined result.

### Using the classes directly

```python
from src.LogParser import LogParser

parser = LogParser("sample.log")
parser.parse()

errors = parser.filter_by_severity("ERROR")
counts = parser.count_by_severity()
```

## Running tests

From the project root:

```bash
pytest
```

## What this project demonstrates

This started as a practice project to rebuild core Python fundamentals (OOP, file I/O, error handling, logging, API consumption, testing, and package structure) with an eye toward production-support/SRE tooling. It's a precursor to a larger log-ingestion and correlation tool.

## Known limitations

- Log format parsing assumes a specific structure (`timestamp timestamp severity message`); lines that don't crash but don't match this shape (wrong word count, valid word count but nonsensical content) currently parse into incorrect data rather than being flagged
- API correlation is intentionally simplified for practice purposes (uses a generic public API rather than an incident/ops-specific one)