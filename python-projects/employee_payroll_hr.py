from datetime import datetime

class Employee:
    """Base class that stores employee details and salary calculations."""

    def __init__(self, employee_id, name, department, basic_salary):
        self.employee_id = employee_id
        self.name = name
        self.department = department
        self.basic_salary = basic_salary
        self.present_days = 0
        self.absent_days = 0
        self.leave_days = 0

    def calculate_attendance(self, present_days, absent_days):
        """Store employee attendance details."""
        self.present_days = present_days
        self.absent_days = absent_days

    def calculate_hra(self):
        """Calculate House Rent Allowance as 20% of basic salary."""
        return self.basic_salary * 0.20

    def calculate_allowance(self):
        """Calculate allowance as 10% of basic salary."""
        return self.basic_salary * 0.10

    def calculate_deduction(self):
        """Calculate deduction as 5% of basic salary."""
        return self.basic_salary * 0.05

    def calculate_tax(self, gross_salary):
        """Calculate tax as 10% of gross salary."""
        return gross_salary * 0.10

    def calculate_bonus(self):
        """Default bonus. Child classes override this method."""
        return 0

    def calculate_salary(self):
        """Calculate and return complete payroll details."""
        hra = self.calculate_hra()
        allowance = self.calculate_allowance()
        bonus = self.calculate_bonus()
        gross_salary = self.basic_salary + hra + allowance + bonus
        tax = self.calculate_tax(gross_salary)
        deduction = self.calculate_deduction()
        net_salary = gross_salary - tax - deduction
        return {
            "Basic Salary": self.basic_salary,
            "HRA": hra,
            "Allowance": allowance,
            "Bonus": bonus,
            "Gross Salary": gross_salary,
            "Tax": tax,
            "Deduction": deduction,
            "Net Salary": net_salary,
        }

class PermanentEmployee(Employee):
    """Permanent employees receive a 10% bonus."""

    def calculate_bonus(self):
        return self.basic_salary * 0.10

class ContractEmployee(Employee):
    """Contract employees receive a 5% bonus."""

    def calculate_bonus(self):
        return self.basic_salary * 0.05

class Intern(Employee):
    """Interns receive lower HRA, allowance and bonus."""

    def calculate_hra(self):
        return self.basic_salary * 0.10

    def calculate_allowance(self):
        return self.basic_salary * 0.05

    def calculate_bonus(self):
        return self.basic_salary * 0.02

class HRManagementSystem:
    """Main class that manages employees, departments and payroll."""

    def __init__(self):
        self.employees = []
        self.departments = []
        self.payroll_records = []

    def find_employee(self, employee_id):
        """Search and return an employee using employee ID."""
        for employee in self.employees:
            if employee.employee_id == employee_id:
                return employee
        return None

    def register_employee(self):
        """Register a new employee."""
        try:
            employee_id = input("Enter Employee ID: ").strip()
            if self.find_employee(employee_id):
                print("Employee ID already exists.")
                return

            name = input("Enter Employee Name: ").strip()
            department = input("Enter Department: ").strip()
            basic_salary = float(input("Enter Basic Salary: "))

            if basic_salary <= 0:
                print("Salary must be greater than zero.")
                return

            print("\n1. Permanent Employee")
            print("2. Contract Employee")
            print("3. Intern")
            employee_type = input("Select Employee Type: ").strip()

            if employee_type == "1":
                employee = PermanentEmployee(employee_id, name, department, basic_salary)
            elif employee_type == "2":
                employee = ContractEmployee(employee_id, name, department, basic_salary)
            elif employee_type == "3":
                employee = Intern(employee_id, name, department, basic_salary)
            else:
                print("Invalid employee type.")
                return

            self.employees.append(employee)
            if department not in self.departments:
                self.departments.append(department)

            print("Employee registered successfully.")
        except ValueError:
            print("Please enter a valid salary.")

    def show_departments(self):
        """Display all available departments."""
        if not self.departments:
            print("No departments available.")
            return

        print("\n===== DEPARTMENTS =====")
        for index, department in enumerate(self.departments, start=1):
            print(f"{index}. {department}")

    def attendance_management(self):
        """Update employee attendance."""
        employee_id = input("Enter Employee ID: ").strip()
        employee = self.find_employee(employee_id)

        if employee is None:
            print("Employee not found.")
            return

        try:
            present_days = int(input("Enter Present Days: "))
            absent_days = int(input("Enter Absent Days: "))

            if present_days < 0 or absent_days < 0:
                print("Days cannot be negative.")
                return

            employee.calculate_attendance(present_days, absent_days)
            print("Attendance updated successfully.")
        except ValueError:
            print("Please enter valid numbers.")

    def leave_management(self):
        """Update employee leave details."""
        employee_id = input("Enter Employee ID: ").strip()
        employee = self.find_employee(employee_id)

        if employee is None:
            print("Employee not found.")
            return

        try:
            leave_days = int(input("Enter Leave Days: "))

            if leave_days < 0:
                print("Leave days cannot be negative.")
                return

            employee.leave_days = leave_days
            print("Leave details updated successfully.")
        except ValueError:
            print("Please enter a valid number.")

    def update_basic_salary(self):
        """Update the basic salary of an employee."""
        employee_id = input("Enter Employee ID: ").strip()
        employee = self.find_employee(employee_id)

        if employee is None:
            print("Employee not found.")
            return

        try:
            new_salary = float(input("Enter New Basic Salary: "))

            if new_salary <= 0:
                print("Salary must be greater than zero.")
                return

            employee.basic_salary = new_salary
            print("Basic salary updated successfully.")
        except ValueError:
            print("Please enter a valid salary.")

    def generate_payroll(self):
        """Generate payroll for a selected employee."""
        employee_id = input("Enter Employee ID: ").strip()
        employee = self.find_employee(employee_id)

        if employee is None:
            print("Employee not found.")
            return

        salary = employee.calculate_salary()
        payroll = {
            "Employee ID": employee.employee_id,
            "Name": employee.name,
            "Department": employee.department,
            "Date": datetime.now().strftime("%d-%m-%Y"),
            "Salary Details": salary,
        }
        self.payroll_records.append(payroll)

        print("\n===== PAYROLL =====")
        print(f"Employee ID : {employee.employee_id}")
        print(f"Name        : {employee.name}")
        print(f"Department  : {employee.department}")
        print(f"Date        : {payroll['Date']}")

        for key, value in salary.items():
            print(f"{key:<15}: ₹{value:.2f}")

    def search_employee(self):
        """Search and display one employee's information."""
        employee_id = input("Enter Employee ID: ").strip()
        employee = self.find_employee(employee_id)

        if employee is None:
            print("Employee not found.")
            return

        print("\n===== EMPLOYEE DETAILS =====")
        print(f"Employee ID : {employee.employee_id}")
        print(f"Name        : {employee.name}")
        print(f"Department  : {employee.department}")
        print(f"Basic Salary: ₹{employee.basic_salary:.2f}")
        print(f"Present Days: {employee.present_days}")
        print(f"Absent Days : {employee.absent_days}")
        print(f"Leave Days  : {employee.leave_days}")
        print(f"Type        : {employee.__class__.__name__}")

    def employee_report(self):
        """Display details of all registered employees."""
        if not self.employees:
            print("No employee records available.")
            return

        print("\n===== EMPLOYEE REPORT =====")
        for employee in self.employees:
            print("-" * 35)
            print(f"Employee ID : {employee.employee_id}")
            print(f"Name        : {employee.name}")
            print(f"Department  : {employee.department}")
            print(f"Type        : {employee.__class__.__name__}")
            print(f"Basic Salary: ₹{employee.basic_salary:.2f}")
            print(f"Present Days: {employee.present_days}")
            print(f"Absent Days : {employee.absent_days}")
            print(f"Leave Days  : {employee.leave_days}")

    def save_employee_records(self):
        """Save employee information into a text file."""
        try:
            with open("employee_records.txt", "w", encoding="utf-8") as file:
                for employee in self.employees:
                    file.write(f"Employee ID: {employee.employee_id}\n")
                    file.write(f"Name: {employee.name}\n")
                    file.write(f"Department: {employee.department}\n")
                    file.write(f"Type: {employee.__class__.__name__}\n")
                    file.write(f"Basic Salary: ₹{employee.basic_salary:.2f}\n")
                    file.write(f"Present Days: {employee.present_days}\n")
                    file.write(f"Absent Days: {employee.absent_days}\n")
                    file.write(f"Leave Days: {employee.leave_days}\n")
                    file.write("-" * 35 + "\n")
            print("Employee records saved successfully.")
        except OSError as error:
            print("File error:", error)

    def save_payroll_records(self):
        """Save generated payroll information into a text file."""
        try:
            with open("payroll_records.txt", "w", encoding="utf-8") as file:
                for payroll in self.payroll_records:
                    file.write(f"Employee ID: {payroll['Employee ID']}\n")
                    file.write(f"Name: {payroll['Name']}\n")
                    file.write(f"Department: {payroll['Department']}\n")
                    file.write(f"Date: {payroll['Date']}\n")
                    for key, value in payroll["Salary Details"].items():
                        file.write(f"{key}: ₹{value:.2f}\n")
                    file.write("-" * 35 + "\n")
            print("Payroll records saved successfully.")
        except OSError as error:
            print("File error:", error)

def main():
    """Run the Employee Payroll and HR Management System."""
    hr = HRManagementSystem()

    while True:
        print("\n==========================================")
        print(" EMPLOYEE PAYROLL & HR MANAGEMENT SYSTEM")
        print("==========================================")
        print("1. Register Employee")
        print("2. Show Departments")
        print("3. Manage Attendance")
        print("4. Manage Leave")
        print("5. Update Basic Salary")
        print("6. Generate Payroll")
        print("7. Search Employee")
        print("8. Employee Report")
        print("9. Save Employee Records")
        print("10. Save Payroll Records")
        print("11. Exit")

        choice = input("Enter Your Choice: ").strip()

        if choice == "1":
            hr.register_employee()
        elif choice == "2":
            hr.show_departments()
        elif choice == "3":
            hr.attendance_management()
        elif choice == "4":
            hr.leave_management()
        elif choice == "5":
            hr.update_basic_salary()
        elif choice == "6":
            hr.generate_payroll()
        elif choice == "7":
            hr.search_employee()
        elif choice == "8":
            hr.employee_report()
        elif choice == "9":
            hr.save_employee_records()
        elif choice == "10":
            hr.save_payroll_records()
        elif choice == "11":
            print("Thank you for using the HR Management System.")
            break
        else:
            print("Invalid choice. Please select 1-11.")

if __name__ == "__main__":
    main()
