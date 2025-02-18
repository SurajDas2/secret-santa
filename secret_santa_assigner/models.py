class Employee:
    """
    Represents an Employee with a name and an email.
    """
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

    def __repr__(self):
        return f"Employee(name={self.name}, email={self.email})"
