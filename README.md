# Lab 1: Grade Evaluator & Archiver

## Overview
This project has two parts:
1. `grade-evaluator.py`: a Python script that reads student grades from `grades.csv`,
   validates them, calculates GPA, determines pass/fail status, and identifies which
   assignment (if any) is eligible for resubmission.
2. `organizer.sh`: a Bash script that archives the current `grades.csv` with a timestamp,
   resets the workspace with a fresh empty CSV, and logs the action.

## How to run the Python script

```bash
python3 grade-evaluator.py
```

When prompted, enter the CSV filename to process (e.g. `grades.csv`).

The script will:
- Validate that every score is between 0 and 100
- Validate that weights sum to 100 overall, with Formative assignments totaling 60
  and Summative assignments totaling 40
- Calculate the weighted Formative average, Summative average, total grade, and GPA
  (`GPA = (Total Grade / 100) * 5.0`)
- Print PASSED or FAILED (requires ≥50% in **both** categories)
- List any failed Formative assignment(s) eligible for resubmission i.e. the failed Formative(s) with the highest weight (ties are all listed)

If the CSV file doesn't exist, or is empty, or contains invalid scores/weights, the
script prints a clear error message instead of crashing.

## How to run the shell script

```bash
chmod +x organizer.sh
./organizer.sh
```

- Create an `archive/` directory if one doesn't already exist
- Rename the current `grades.csv` by appending a timestamp (e.g. `grades_20260724-225317.csv`)
  and move it into `archive/`
- Create a fresh, empty `grades.csv` in the working directory
- Append a log entry (timestamp, original filename, archived filename) to `organizer.log`,
  which accumulates entries across every run
