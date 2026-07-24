import csv
import sys
import os

def load_csv_data():
    """
    Prompts the user for a filename, checks if it exists, 
    and extracts all fields into a list of dictionaries.
    """
    filename = input("Enter the name of the CSV file to process (e.g., grades.csv): ")
    
    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)
        
    assignments = []
    
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Convert numeric fields to floats for calculations
                assignments.append({
                    'assignment': row['assignment'],
                    'group': row['group'],
                    'score': float(row['score']),
                    'weight': float(row['weight'])
                })
        return assignments
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)

def evaluate_grades(data):
    """
    Implement your logic here.
    'data' is a list of dictionaries containing the assignment records.
    """
    print("\n--- Processing Grades ---")
    
    # --- Edge case: empty CSV (this happens right after organizer.sh resets grades.csv) ---
    # If there's no data at all, none of the logic below is meaningful, so we
    # print a clear message and stop, instead of crashing on a ZeroDivisionError later.
    if not data:
        print("No assignment data found. The grades file appears to be empty.")
        return

    # --- a) Grade Validation: every score must be within 0–100 ---
    # We collect ALL invalid rows first (instead of stopping at the first one)
    # so the user gets one complete error report rather than fixing issues one at a time.
    invalid_scores = [row for row in data if not (0 <= row['score'] <= 100)]
    if invalid_scores:
        print("Error: The following assignments have scores outside the valid 0-100 range:")
        for row in invalid_scores:
            print(f"  - {row['assignment']}: {row['score']}")
        return  # Stop here; there's no sensible GPA to calculate with bad data
    # TODO: b) Validate total weights (Total=100, Summative=40, Formative=60)
    # TODO: c) Calculate the Final Grade and GPA
    # TODO: d) Determine Pass/Fail status (>= 50% in BOTH categories)
    # TODO: e) Check for failed formative assignments (< 50%)
    #          and determine which one(s) have the highest weight for resubmission.
    # TODO: f) Print the final decision (PASSED / FAILED) and resubmission options
    
    pass

if __name__ == "__main__":
    # 1. Load the data
    course_data = load_csv_data()
    
    # 2. Process the features
    evaluate_grades(course_data)