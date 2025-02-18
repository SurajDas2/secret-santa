# Secret Santa Assigner

A Python-based Secret Santa assignment system that **reads employees from a CSV** and **(optionally) last year's assignments** in another CSV, then **generates new assignments** ensuring:
- No one is assigned themselves.
- No one repeats last year's secret child.
- Each employee has exactly one secret child, and each child is assigned to only one employee.
- Final assignments are **written to a CSV**.

---

## Table of Contents

1. [Features](#features)
2. [Prerequisites](#prerequisites)
3. [Project Structure](#project-structure)
4. [Installation](#installation)
5. [Usage](#usage)
   - [Command Line (CLI) Mode](#command-line-cli-mode)
   - [GUI (Desktop) Mode](#gui-desktop-mode)
6. [Input File Formats](#input-file-formats)
   - [Employees CSV Format](#employees-csv-format)
   - [Last Year Assignments CSV Format](#last-year-assignments-csv-format)
7. [Running Tests](#running-tests)
8. [Potential Errors & Logging](#potential-errors--logging)
9. [License](#license)
10. [Contact](#contact)

---

## Features

- **Uniqueness**: No employee is their own secret child.
- **No Repeats**: Avoids the same (employee -> child) pairing as last year.
- **One-to-One**: Each employee has exactly one child; each child has exactly one parent.
- **Output**: Generates a CSV with columns:
  - `Employee_Name`, `Employee_EmailID`, `Secret_Child_Name`, `Secret_Child_EmailID`
- **Two Modes**: Command-line (CLI) or a simple Tkinter-based desktop GUI.

---

## Prerequisites

- **Python 3.9** (or any Python 3.8+ version).  
- **pip** (Python package manager) for installing dependencies.

> **Note**: If you’re on Python 3.9, you’re good to go.

---

## Project Structure

A typical layout (simplified):

```
secret_santa/
  ├─ main.py                   # CLI entry point
  ├─ gui_app.py                # Tkinter-based desktop GUI
  ├─ requirements.txt
  ├─ README.md
  ├─ secret_santa_assigner/
  │   ├─ __init__.py
  │   ├─ models.py
  │   ├─ utils/
  │   │   └─ file_utils.py     # CSV reading/writing logic with pandas
  │   └─ services/
  │       └─ assignment_service.py  # Core assignment logic
  └─ tests/
      ├─ __init__.py
      └─ test_assignment_service.py # Some pytest-based tests
```

---

## Installation

1. **Clone** this repository:
   ```bash
   git clone https://github.com/your-username/secret_santa.git
   cd secret_santa
   ```
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   This installs `pandas` (for CSV handling), `pytest` (for testing), and any other listed dependencies.

---

## Usage

### Command Line (CLI) Mode

If you prefer running from the command line or a terminal:

1. **Navigate** to the `secret_santa` directory (the project’s root).
2. **Run**:
   ```bash
   python main.py \
     --employees_csv path/to/employees.csv \
     --last_year_csv path/to/last_year.csv \
     --output_csv path/to/output.csv
   ```
   - **`--employees_csv`** (required): Path to the CSV listing current employees (`Employee_Name`, `Employee_EmailID`).
   - **`--last_year_csv`** (optional): Path to the CSV of last year’s assignments (`Employee_Name`, `Employee_EmailID`, `Secret_Child_Name`, `Secret_Child_EmailID`).  
     - Omit or leave it blank if you don’t have last year’s data.
   - **`--output_csv`** (required): Path where the new assignments will be written.

**Example**:
```bash
python main.py \
  --employees_csv data/employees_2023.csv \
  --last_year_csv data/employees_2022_assignments.csv \
  --output_csv data/new_assignments_2023.csv
```
Upon success, `new_assignments_2023.csv` will be created/overwritten with columns:  
`Employee_Name, Employee_EmailID, Secret_Child_Name, Secret_Child_EmailID`.

### GUI (Desktop) Mode

If you prefer a **simple desktop-like interface**:

1. **Navigate** to the `secret_santa` directory.
2. **Run**:
   ```bash
   python gui_app.py
   ```
3. A **Tkinter** window opens:
   - **Browse** for Employees CSV.
   - **Browse** (optional) for Last Year CSV.
   - **Browse or save as** for the Output CSV.
   - Click **"Generate Assignments"**.
4. If successful, a **success dialog** will appear telling you where the assignments were saved.  
   If something goes wrong (e.g., a file is missing or no valid matching found), an **error dialog** will appear with details.

> **Note**: Tkinter typically comes installed with Python. If you’re missing it on Linux, you may need to install it (e.g., `sudo apt-get install python3-tk`).

---

## Input File Formats

### Employees CSV Format

Your **employees CSV** must have the following columns:
- **`Employee_Name`**  
- **`Employee_EmailID`**

**Example**:

| Employee_Name   | Employee_EmailID          |
|-----------------|---------------------------|
| Alice Smith     | alice.smith@acme.com     |
| Bob Johnson     | bob.johnson@acme.com     |
| Carol Williams  | carol.williams@acme.com  |

### Last Year Assignments CSV Format (Optional)

| Employee_Name   | Employee_EmailID          | Secret_Child_Name  | Secret_Child_EmailID       |
|-----------------|---------------------------|--------------------|----------------------------|
| Alice Smith     | alice.smith@acme.com     | Bob Johnson        | bob.johnson@acme.com       |
| Bob Johnson     | bob.johnson@acme.com     | Carol Williams     | carol.williams@acme.com    |
| Carol Williams  | carol.williams@acme.com  | Alice Smith        | alice.smith@acme.com       |

---

## Running Tests

This project uses **pytest** for unit testing. To run tests:

```bash
pytest
```

---

## Potential Errors & Logging

- **FileNotFoundError**: If the CSV file path is wrong or the file doesn’t exist.
- **ValueError**: If the CSV is missing required columns or rows are invalid.

---

Feel free to open issues or pull requests for improvements and new features.
