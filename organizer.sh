#!/bin/bash
# organizer.sh
# Archives the current grades.csv with a timestamp, resets a fresh empty one,
# and logs every archiving action to organizer.log.

# Step 1: Ensure the archive directory exists
if [ ! -d "archive" ]; then
    mkdir archive
    echo "Created archive directory."
fi

# Step 2: Generate a timestamp string
timestamp=$(date +"%Y%m%d-%H%M%S")

# Step 3: Confirm grades.csv actually exists before doing anything
if [ ! -f "grades.csv" ]; then
    echo "Error: grades.csv not found in the current directory. Nothing to archive."
    exit 1
fi

# Step 4: Build the new archived filename
archived_name="grades_${timestamp}.csv"

# Step 5: Move (and rename in the same step) grades.csv into archive/
mv grades.csv "archive/${archived_name}"

# Step 6: Create a fresh, empty grades.csv so the workspace is ready again
touch grades.csv

# Step 7: Log this action
echo "${timestamp} | original: grades.csv | archived as: archive/${archived_name}" >> organizer.log

echo "Archiving complete: grades.csv -> archive/${archived_name}"