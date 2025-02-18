import argparse
import sys
from secret_santa_assigner.utils.file_utils import (
    read_employees_from_csv,
    read_last_year_assignments,
    write_assignments_to_csv
)
from secret_santa_assigner.services.assignment_service import SecretSantaAssigner

def main():
    parser = argparse.ArgumentParser(description="Secret Santa Assigner")

    parser.add_argument(
        "--employees_csv",
        required=True,
        help="Path to the employees CSV (columns: Employee_Name, Employee_EmailID)."
    )
    parser.add_argument(
        "--last_year_csv",
        required=False,
        default=None,
        help="Path to last year's assignment CSV (columns: Employee_Name, Employee_EmailID, Secret_Child_Name, Secret_Child_EmailID)."
    )
    parser.add_argument(
        "--output_csv",
        required=True,
        help="Path to output this year's assignments CSV."
    )

    args = parser.parse_args()

    try:
        # Read the current employees
        employees = read_employees_from_csv(args.employees_csv)
        if not employees:
            print("No employees found in CSV. Exiting.")
            sys.exit(1)

        # Read the last-year map if provided
        last_year_map = {}
        if args.last_year_csv:
            last_year_map = read_last_year_assignments(args.last_year_csv)

        # Create the assigner
        assigner = SecretSantaAssigner(employees, last_year_map)
        assigner.assign()  # attempt the assignment

        # Get the results in a format suitable for writing
        assignment_pairs = assigner.get_assignment_pairs()

        # Write to CSV
        write_assignments_to_csv(args.output_csv, assignment_pairs)

        print(f"Assignments successfully written to {args.output_csv}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
