import pytest
from secret_santa_assigner.models import Employee
from secret_santa_assigner.services.assignment_service import SecretSantaAssigner

def test_simple_assignment():
    employees = [
        Employee("Alice", "alice@acme.com"),
        Employee("Bob", "bob@acme.com"),
        Employee("Charlie", "charlie@acme.com")
    ]
    # Suppose last year's map is empty
    assigner = SecretSantaAssigner(employees, {})
    result = assigner.assign()

    # Check we got a mapping for each employee
    assert len(result) == 3

    # No one assigned to themselves
    for e in employees:
        assert result[e.email] != e.email

def test_no_repeat_from_last_year():
    employees = [
        Employee("Alice", "alice@acme.com"),
        Employee("Bob", "bob@acme.com"),
    ]
    # Suppose last year Alice -> Bob, Bob -> Alice
    last_year_map = {
        "alice@acme.com": "bob@acme.com",
        "bob@acme.com": "alice@acme.com"
    }
    assigner = SecretSantaAssigner(employees, last_year_map)

    with pytest.raises(Exception) as excinfo:
        # With only 2 employees, if last year was A->B and B->A,
        # there's no valid "derangement" that changes the pairing.
        assigner.assign()

    assert "Could not find a valid Secret Santa assignment" in str(excinfo.value)
