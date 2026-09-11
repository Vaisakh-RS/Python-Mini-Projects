# LogParser — Multi-Source Log Ingestion & Correlation Tool

A Python tool that ingests log data from multiple configured sources, parses it into structured objects, and correlates errors across sources by time proximity — surfacing potentially related incidents that a human scanning individual log files might miss.

## What it does

Given a set of log files (defined in a config file, not hardcoded) representing different systems — say an auth service and a database — this tool:

1. **Ingests** all configured sources, parsing each into structured `LogEntry` objects, skipping malformed lines without crashing
2. **Filters** for actionable severities (ERROR/WARNING) across sources
3. **Correlates** entries across two sources by time-window proximity — flagging pairs of events that happened close enough together to plausibly be related (e.g. an auth service losing its DB connection around the same time the database itself shows signs of stress)
4. **Outputs** results two ways: a readable console summary, and a structured JSON report for downstream tooling (dashboards, alerting pipelines, tickets)

## Why this exists

Production incidents rarely show up in just one log. A real correlation tool needs to pull from several sources and surface connections a human scanning one file at a time would miss. This project is a sanitized, from-scratch practice build of that idea.

## Project structure

```
LogParser/
├── src/
│   ├── LogParser.py        # LogEntry + LogParser: parses a single log file
│   ├── LogReader.py         # LogReader: config-driven multi-source ingestion + correlation
│   ├── ApiTest.py            # fetchApi: external API client (used in Combine.py practice piece)
│   ├── Combine.py            # standalone practice artifact — LogParser + fetchApi integration
│   └── logging_config.py    # centralized logging setup (console + file handlers)
├── tests/
│   └── test_log_parser.py
├── input_logs/
│   ├── sample.log
│   ├── auth_service.log
│   └── database.log
├── config.yaml                # defines which log sources to ingest
├── example_output.json        # sample correlation report output
├── requirements.txt
└── README.md
```

## Setup

```bash
python -m venv venv
venv\Scripts\Activate.ps1      # Windows PowerShell
pip install -r requirements.txt
```

## Configuration

Log sources are defined in `config.yaml`:

```yaml
sources:
  - name: general
    path: input_logs/sample.log
  - name: auth
    path: input_logs/auth_service.log
  - name: database
    path: input_logs/database.log
```

Add or remove sources here without touching any code.

## Usage

Run from the project root:

```bash
python -m src.LogReader
```

This will:
- Parse all configured sources
- Filter `auth` and `database` entries down to ERROR/WARNING
- Correlate pairs within a configurable time window (default: 150 seconds)
- Print a readable summary to console
- Write a structured report to `correlation_report.json`

Example console output:
```
[CORRELATED] auth (2026-08-19 10:48:33): unauthorized access attempt blocked <-> database (2026-08-19 10:50:26): failed to write to transaction log | gap: 113s
```

See `example_output.json` for a sample of the structured report format.

## Logging

Logging is centralized in `logging_config.py` — configured once at the entry point, with every module pulling a named logger via `logging.getLogger(__name__)` that inherits the root logger's handlers. Output goes to both console and `app.log` (git-ignored, regenerated per run).

## Running tests

```bash
pytest
```

Tests cover core parsing/query logic (`LogEntry`, `LogParser`) using hand-built objects — no file I/O or network calls, so they run fast and don't depend on external state.

## Design notes

- **Malformed line handling:** lines that fail to parse (e.g. insufficient fields) are logged as warnings and skipped rather than crashing the run. Lines that parse without error but don't structurally represent valid log data are a known, currently-unhandled gap — flagged deliberately rather than silently assumed away.
- **Correlation window:** tuned against sample data to 150 seconds — a judgment call about what counts as "plausibly related," not a fixed rule. Configurable via `pair_logs`'s `window_seconds` parameter.
- **Why both a `LogParser` (single file) and a `LogReader` (multi-source orchestration) class exist:** kept separate deliberately — `LogParser` knows how to parse one file, `LogReader` knows how to read config and coordinate multiple `LogParser`s. Neither needs to know about the other's internals beyond that boundary.
- **`Combine.py`** is an earlier practice artifact (parser + a placeholder external API), kept as-is rather than evolved into the main project, to demonstrate cross-file integration separately from the core correlation logic.