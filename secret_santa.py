import csv
import random
from typing import List, Dict, Optional


class Employee:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

    def __repr__(self):
        return f"Employee(name={self.name}, email={self.email})"


class FileHandler:

    @staticmethod
    def read_csv(file_path: str) -> List[Dict[str, str]]:
       
        try:
            with open(file_path, mode='r') as file:
                reader = csv.DictReader(file)
                return list(reader)
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")
        except Exception as e:
            raise Exception(f"Error reading CSV file: {e}")

    @staticmethod
    def write_csv(file_path: str, data: List[Dict[str, str]], fieldnames: List[str]):
        
        try:
            with open(file_path, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
        except Exception as e:
            raise Exception(f"Error writing CSV file: {e}")


class Validator:
   
    @staticmethod
    def validate_employees(employees: List[Employee]):
        if not employees:
            raise ValueError("No employees provided.")

        emails = set()
        for emp in employees:
            if not emp.name or not emp.email:
                raise ValueError(f"Invalid employee data: {emp}")
            if emp.email in emails:
                raise ValueError(f"Duplicate email address: {emp.email}")
            emails.add(emp.email)


class SecretSanta:
   
    def __init__(self, employees: List[Employee], previous_assignments: Optional[List[Dict[str, str]]] = None):
        self.employees = employees
        self.previous_assignments = previous_assignments or []

    def assign_secret_children(self) -> List[Dict[str, str]]:
        assignments = []
        remaining_employees = self.employees.copy()

        for emp in self.employees:
            invalid_children = [emp]  
            valid_children = [e for e in remaining_employees if e not in invalid_children]

            if not valid_children:
                raise ValueError(f"No valid secret child found for employee: {emp.name}")

            child = random.choice(valid_children)
            assignments.append({
                "Employee_Name": emp.name,
                "Employee_EmailID": emp.email,
                "Secret_Child_Name": child.name,
                "Secret_Child_EmailID": child.email
            })
            remaining_employees.remove(child)

        return assignments


def main():
 
    try:
        print("Starting Secret Santa assignment process...")
        csv_input_path = "src/Input File/employees.csv"
        assignments_output_path = "src/Output File/assignments.csv"

        employees_data = FileHandler.read_csv(csv_input_path)
        print("\nCSV Data:")
        for row in employees_data:
            print(row)

        employees = [Employee(row["Employee_Name"], row["Employee_EmailID"]) for row in employees_data]
        Validator.validate_employees(employees)

        secret_santa = SecretSanta(employees)
        assignments = secret_santa.assign_secret_children()

        print("\nAssignments:")
        for assignment in assignments:
            print(assignment)

        FileHandler.write_csv(assignments_output_path, assignments, ["Employee_Name", "Employee_EmailID", "Secret_Child_Name", "Secret_Child_EmailID"])
        print("Secret Santa assignments generated successfully!")

    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except ValueError as e:
        print(f"Validation error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()