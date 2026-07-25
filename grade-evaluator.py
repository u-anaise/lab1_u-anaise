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
    
    # Edge case: empty CSV 
    if not data:
        print("No assignment data found. The grades file appears to be empty.")
        return


    # a) Grade Validation: every score must be within 0–100
    invalid_scores = [row for row in data if not (0 <= row['score'] <= 100)]
    if invalid_scores:
        print("Error: The following assignments have scores outside the valid 0-100 range:")
        for row in invalid_scores:
            print(f"  - {row['assignment']}: {row['score']}")
        return  


    # b) Weight Validation
    formatives = [row for row in data if row['group'] == 'Formative']
    summatives = [row for row in data if row['group'] == 'Summative']

    total_weight = sum(row['weight'] for row in data)
    formative_weight = sum(row['weight'] for row in formatives)
    summative_weight = sum(row['weight'] for row in summatives)

    # Tolerance of 0.01 instead of exact equality: floating-point addition can
    # produce results like 99.99999999999999 instead of a clean 100.0
    if abs(total_weight - 100) > 0.01:
        print(f"Error: Total weights must sum to 100, but they sum to {total_weight}.")
        return
    if abs(formative_weight - 60) > 0.01:
        print(f"Error: Formative weights must sum to 60, but they sum to {formative_weight}.")
        return
    if abs(summative_weight - 40) > 0.01:
        print(f"Error: Summative weights must sum to 40, but they sum to {summative_weight}.")
        return

    
    # c) GPA Calculation
    formative_pct = sum(row['score'] * row['weight'] for row in formatives) / formative_weight
    summative_pct = sum(row['score'] * row['weight'] for row in summatives) / summative_weight

    total_grade = sum(row['score'] * row['weight'] for row in data) / total_weight
    gpa = (total_grade / 100) * 5.0

    print(f"Formative average: {formative_pct:.2f}%")
    print(f"Summative average: {summative_pct:.2f}%")
    print(f"Total grade: {total_grade:.2f}%")
    print(f"GPA: {gpa:.3f}")

    
    # d) Final Decision: must be >=50% in BOTH categories, not just the overall total
    passed = formative_pct >= 50 and summative_pct >= 50
    status = "PASSED" if passed else "FAILED"
    print(f"Status: {status}")


    # e) Resubmission Logic: only FORMATIVE assignments below 50% are eligible.
    failed_formatives = [row for row in formatives if row['score'] < 50]

    if not failed_formatives:
        print("No formative resubmissions needed.")
    else:
        # Weight is compared only among the failed ones: a formative that passed is never up for resubmission, no matter its weight.
        # If two or more failed assignments tie for the highest weight, all of them are listed.
        highest_weight = max(row['weight'] for row in failed_formatives)
        resubmission_candidates = [
            row['assignment'] for row in failed_formatives if row['weight'] == highest_weight
        ]
        
        print("Eligible for resubmission (highest-weight failed formative(s)):")
        for name in resubmission_candidates:
            print(f"  - {name}")


if __name__ == "__main__":
    # 1. Load the data
    course_data = load_csv_data()
    
    # 2. Process the features
    evaluate_grades(course_data)