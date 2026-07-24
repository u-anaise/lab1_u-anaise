#!/bin/bash
# organizer.sh
# Archives the current grades.csv with a timestamp, resets a fresh empty one,
# and logs every archiving action to organizer.log.

# --- Step 1: Ensure the archive directory exists ---
# -d tests "does this path exist AND is it a directory".
# The ! negates it: "if archive does NOT exist, create it."
if [ ! -d "archive" ]; then
    mkdir archive
    echo "Created archive directory."
fi

# --- Step 2: Generate a timestamp string ---
# `date +"%Y%m%d-%H%M%S"` formats as YearMonthDay-HourMinuteSecond,
# e.g. 20260724-231045 — safe for filenames (no spaces or colons).
timestamp=$(date +"%Y%m%d-%H%M%S")

# --- Step 3: Build the new archived filename ---
archived_name="grades_${timestamp}.csv"

# --- Step 4: Move (and rename in the same step) grades.csv into archive/ ---
# `mv` with a different destination filename does the rename and move together.
mv grades.csv "archive/${archived_name}"

# --- Step 5: Create a fresh, empty grades.csv so the workspace is ready again ---
# `touch` creates an empty file if it doesn't exist (or updates its timestamp if it does).
touch grades.csv

# --- Step 6: Log this action ---
# `>>` appends to the log file rather than overwriting it, so history accumulates
# across every run — required by the spec.
echo "${timestamp} | original: grades.csv | archived as: archive/${archived_name}" >> organizer.log

echo "Archiving complete: grades.csv -> archive/${archived_name}"