import tkinter as tk
from tkinter import filedialog, messagebox
import os

# Import our assignment logic & file utils from the existing modules
from secret_santa_assigner.utils.file_utils import (
    read_employees_from_csv,
    read_last_year_assignments,
    write_assignments_to_csv
)
from secret_santa_assigner.services.assignment_service import SecretSantaAssigner

class SecretSantaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Secret Santa Assigner")

        # Initialize file path variables
        self.employees_csv = None
        self.last_year_csv = None
        self.output_csv = None

        # 1) Employees CSV
        self.lbl_employees = tk.Label(root, text="Employees CSV:")
        self.lbl_employees.grid(row=0, column=0, padx=5, pady=5, sticky="e")

        self.txt_employees = tk.Entry(root, width=50)
        self.txt_employees.grid(row=0, column=1, padx=5, pady=5)

        self.btn_browse_employees = tk.Button(root, text="Browse", command=self.browse_employees)
        self.btn_browse_employees.grid(row=0, column=2, padx=5, pady=5)

        # 2) Last Year CSV
        self.lbl_last_year = tk.Label(root, text="Last Year CSV (Optional):")
        self.lbl_last_year.grid(row=1, column=0, padx=5, pady=5, sticky="e")

        self.txt_last_year = tk.Entry(root, width=50)
        self.txt_last_year.grid(row=1, column=1, padx=5, pady=5)

        self.btn_browse_last_year = tk.Button(root, text="Browse", command=self.browse_last_year)
        self.btn_browse_last_year.grid(row=1, column=2, padx=5, pady=5)

        # 3) Output CSV
        self.lbl_output = tk.Label(root, text="Output CSV:")
        self.lbl_output.grid(row=2, column=0, padx=5, pady=5, sticky="e")

        self.txt_output = tk.Entry(root, width=50)
        self.txt_output.grid(row=2, column=1, padx=5, pady=5)

        self.btn_browse_output = tk.Button(root, text="Browse", command=self.browse_output)
        self.btn_browse_output.grid(row=2, column=2, padx=5, pady=5)

        # 4) Run Button
        self.btn_run = tk.Button(root, text="Generate Assignments", command=self.generate_assignments)
        self.btn_run.grid(row=3, column=0, columnspan=3, pady=10)

    def browse_employees(self):
        """Open file dialog for Employees CSV."""
        file_path = filedialog.askopenfilename(
            title="Select Employees CSV",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        if file_path:
            self.employees_csv = file_path
            self.txt_employees.delete(0, tk.END)
            self.txt_employees.insert(0, file_path)

    def browse_last_year(self):
        """Open file dialog for Last Year CSV."""
        file_path = filedialog.askopenfilename(
            title="Select Last Year CSV",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        if file_path:
            self.last_year_csv = file_path
            self.txt_last_year.delete(0, tk.END)
            self.txt_last_year.insert(0, file_path)

    def browse_output(self):
        """Open file dialog for Output CSV."""
        file_path = filedialog.asksaveasfilename(
            title="Select Output CSV",
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        if file_path:
            self.output_csv = file_path
            self.txt_output.delete(0, tk.END)
            self.txt_output.insert(0, file_path)

    def generate_assignments(self):
        """Perform the Secret Santa assignment using the user's selected files."""
        employees_csv = self.txt_employees.get().strip()
        last_year_csv = self.txt_last_year.get().strip()
        output_csv = self.txt_output.get().strip()

        # Basic validation checks
        if not employees_csv:
            messagebox.showwarning("Validation Error", "Please select Employees CSV.")
            return
        if not output_csv:
            messagebox.showwarning("Validation Error", "Please select Output CSV.")
            return

        # Attempt to run the assignment
        try:
            employees = read_employees_from_csv(employees_csv)
            if not employees:
                messagebox.showerror("Error", "No employees found in the selected CSV.")
                return

            # If last_year_csv is provided
            if last_year_csv:
                last_year_map = read_last_year_assignments(last_year_csv)
            else:
                last_year_map = {}

            # Perform assignment
            assigner = SecretSantaAssigner(employees, last_year_map)
            assigner.assign()
            results = assigner.get_assignment_pairs()

            # Write to output CSV
            write_assignments_to_csv(output_csv, results)
            
            messagebox.showinfo("Success", f"Assignments successfully written to:\n{output_csv}")

        except Exception as e:
            messagebox.showerror("Error", str(e))

def launch_app():
    root = tk.Tk()
    app = SecretSantaGUI(root)
    root.mainloop()

if __name__ == "__main__":
    launch_app()
