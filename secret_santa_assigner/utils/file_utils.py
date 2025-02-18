import pandas as pd
from typing import List, Dict
from secret_santa_assigner.models import Employee

def read_employees_from_csv(filepath: str) -> List[Employee]:
    """
    Reads a CSV with columns: Employee_Name, Employee_EmailID
    Returns a list of Employee objects.
    """
    try:
        df = pd.read_csv(filepath)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {filepath}")
    except Exception as e:
        raise ValueError(f"Error reading CSV at {filepath}: {e}")
 
    df.columns = df.columns.str.strip()
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df.dropna(how="all", inplace=True)
    print(df)
    required_columns = {"Employee_Name", "Employee_EmailID"}
    if not required_columns.issubset(df.columns):
        raise ValueError(f"CSV missing required columns: {required_columns}")

    employees = []
    for _, row in df.iterrows():
        name = str(row["Employee_Name"]).strip()
        email = str(row["Employee_EmailID"]).strip()
        if not name or not email:
            raise ValueError(f"Invalid row with missing name or email: {row}")
        employees.append(Employee(name, email))

    return employees

def read_last_year_assignments(filepath: str) -> Dict[str, str]:
    """
    Reads a CSV with columns: Employee_Name, Employee_EmailID, Secret_Child_Name, Secret_Child_EmailID
    Returns a dict mapping: {employee_email: secret_child_email}
    """
    try:
        df = pd.read_csv(filepath)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {filepath}")
    except Exception as e:
        raise ValueError(f"Error reading CSV at {filepath}: {e}")

    required_columns = {"Employee_Name", "Employee_EmailID", "Secret_Child_Name", "Secret_Child_EmailID"}
    if not required_columns.issubset(df.columns):
        raise ValueError(f"CSV missing required columns: {required_columns}")

    last_year_map = {}
    for _, row in df.iterrows():
        emp_email = str(row["Employee_EmailID"]).strip()
        child_email = str(row["Secret_Child_EmailID"]).strip()
        if emp_email and child_email:
            last_year_map[emp_email] = child_email

    return last_year_map

def write_assignments_to_csv(filepath: str, assignments: List[tuple]):
    """
    Writes the resulting assignments to a CSV.
    Each tuple in `assignments` is:
      (Employee_Name, Employee_EmailID, Secret_Child_Name, Secret_Child_EmailID)
    """
    import os
    import pandas as pd

    # Convert list of tuples to a DataFrame
    df = pd.DataFrame(assignments, columns=[
        "Employee_Name",
        "Employee_EmailID",
        "Secret_Child_Name",
        "Secret_Child_EmailID"
    ])

    # Write to CSV
    output_dir = os.path.dirname(filepath)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    df.to_csv(filepath, index=False)
