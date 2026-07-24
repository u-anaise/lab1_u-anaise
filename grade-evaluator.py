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


    # --- b) Weight Validation ---
    # Split the assignments into their two groups so we can check each group's
    # total weight separately, as well as the grand total.
    formatives = [row for row in data if row['group'] == 'Formative']
    summatives = [row for row in data if row['group'] == 'Summative']

    total_weight = sum(row['weight'] for row in data)
    formative_weight = sum(row['weight'] for row in formatives)
    summative_weight = sum(row['weight'] for row in summatives)

    # Use a tiny tolerance (0.01) instead of exact equality, since floating-point
    # addition can produce results like 99.99999999999999 instead of a clean 100.0
    if abs(total_weight - 100) > 0.01:
        print(f"Error: Total weights must sum to 100, but they sum to {total_weight}.")
        return
    if abs(formative_weight - 60) > 0.01:
        print(f"Error: Formative weights must sum to 60, but they sum to {formative_weight}.")
        return
    if abs(summative_weight - 40) > 0.01:
        print(f"Error: Summative weights must sum to 40, but they sum to {summative_weight}.")
        return

    
    # --- c) GPA Calculation ---
    # Each category's percentage score is a WEIGHTED average:
    # sum(score * weight) for that group, divided by that group's total weight.
    formative_pct = sum(row['score'] * row['weight'] for row in formatives) / formative_weight
    summative_pct = sum(row['score'] * row['weight'] for row in summatives) / summative_weight

    # The overall total grade is the weighted average across ALL assignments
    total_grade = sum(row['score'] * row['weight'] for row in data) / total_weight
    gpa = (total_grade / 100) * 5.0

    print(f"Formative average: {formative_pct:.2f}%")
    print(f"Summative average: {summative_pct:.2f}%")
    print(f"Total grade: {total_grade:.2f}%")
    print(f"GPA: {gpa:.3f}")

    
    # --- d) Final Decision: must be >=50% in BOTH categories, not just the overall total ---
    passed = formative_pct >= 50 and summative_pct >= 50
    status = "PASSED" if passed else "FAILED"
    print(f"Status: {status}")


    # --- e) Resubmission Logic ---
    # Only FORMATIVE assignments below 50% are eligible.
    failed_formatives = [row for row in formatives if row['score'] < 50]

    if not failed_formatives:
        print("No formative resubmissions needed.")
    else:
        # Find the highest weight among the FAILED formatives specifically
        # (not the highest weight overall — a passed assignment doesn't need resubmission
        # even if it happens to carry more weight).
        highest_weight = max(row['weight'] for row in failed_formatives)

        # Collect every failed formative that shares that highest weight — this
        # handles ties, as the spec requires (show ALL of them, not just one).
        resubmission_candidates = [
            row['assignment'] for row in failed_formatives if row['weight'] == highest_weight
        ]

        
        print("Eligible for resubmission (highest-weight failed formative(s)):")
        for name in resubmission_candidates:
            print(f"  - {name}")

    
    pass

if __name__ == "__main__":
    # 1. Load the data
    course_data = load_csv_data()
    
    # 2. Process the features
    evaluate_grades(course_data)