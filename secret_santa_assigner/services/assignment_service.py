import random
from typing import List, Dict
from secret_santa_assigner.models import Employee

class SecretSantaAssigner:
    """
    Takes a list of current employees and (optionally) a map from last year's assignments
    to avoid repeating the same secret child.
    """
    def __init__(self, employees: List[Employee], last_year_map: Dict[str, str] = None):
        self.employees = employees
        self.last_year_map = last_year_map if last_year_map else {}

        # Build quick lookup dicts
        self.email_to_employee = {e.email: e for e in employees}
        self.emails = [e.email for e in employees]

        # Will store final assignment: {employee_email -> secret_child_email}
        self.current_assignments = {}

    def assign(self) -> Dict[str, str]:
        """
        Attempts to create a valid Secret Santa assignment with constraints:
          - Nobody is their own secret child.
          - Do not repeat last year's pairing.
          - Each employee must have exactly one child, each child has exactly one parent.
        Returns a dict: {employee_email -> secret_child_email}.
        Raises Exception if no valid assignment is found.
        """
        # Try multiple random permutations to find a valid assignment
        for _ in range(20000):
            shuffled = self.emails[:]
            random.shuffle(shuffled)
            assignment_map = {}

            valid = True
            for emp_email, child_email in zip(self.emails, shuffled):
                # 1) Not assigned to self
                if emp_email == child_email:
                    valid = False
                    break
                # 2) Not repeating last year's assignment
                if self.last_year_map.get(emp_email) == child_email:
                    valid = False
                    break

                assignment_map[emp_email] = child_email

            if valid:
                # If we made it through the loop, we found a valid assignment
                self.current_assignments = assignment_map
                return assignment_map

        # If we fail after many tries, raise an exception
        raise Exception("Could not find a valid Secret Santa assignment after many attempts.")

    def get_assignment_pairs(self) -> List[tuple]:
        """
        Returns the final assignment in a list of 4-tuples:
        (Employee_Name, Employee_EmailID, Secret_Child_Name, Secret_Child_EmailID).
        Useful for writing to CSV.
        """
        if not self.current_assignments:
            raise ValueError("No assignment found yet. Call assign() first.")

        results = []
        for emp_email, child_email in self.current_assignments.items():
            emp = self.email_to_employee[emp_email]
            child = self.email_to_employee[child_email]
            results.append((emp.name, emp.email, child.name, child.email))
        return results
