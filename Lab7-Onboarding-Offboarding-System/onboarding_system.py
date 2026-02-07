import json
import os
from datetime import datetime

# Database files
EMPLOYEES_FILE = "employees.json"
ASSETS_FILE = "assets.json"
AUDIT_LOG_FILE = "audit_log.json"

# Function to load employees
def load_employees():
    """Load employee database"""
    if os.path.exists(EMPLOYEES_FILE):
        with open(EMPLOYEES_FILE, 'r') as f:
            return json.load(f)
    return []

# Function to save employees
def save_employees(employees):
    """Save employee database"""
    with open(EMPLOYEES_FILE, 'w') as f:
        json.dump(employees, f, indent=4)

# Function to load assets
def load_assets():
    """Load asset database"""
    if os.path.exists(ASSETS_FILE):
        with open(ASSETS_FILE, 'r') as f:
            return json.load(f)
    return []

# Function to save assets
def save_assets(assets):
    """Save asset database"""
    with open(ASSETS_FILE, 'w') as f:
        json.dump(assets, f, indent=4)

# Function to log audit entry
def log_audit(action, employee_name, details):
    """Log action to audit trail"""
    if os.path.exists(AUDIT_LOG_FILE):
        with open(AUDIT_LOG_FILE, 'r') as f:
            logs = json.load(f)
    else:
        logs = []
    
    log_entry = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'action': action,
        'employee': employee_name,
        'details': details,
        'performed_by': 'IT Admin'
    }
    
    logs.append(log_entry)
    
    with open(AUDIT_LOG_FILE, 'w') as f:
        json.dump(logs, f, indent=4)

# Function to generate employee ID
def generate_employee_id(employees):
    """Generate unique employee ID"""
    if not employees:
        return "EMP001"
    
    last_id = max([int(emp['employee_id'][3:]) for emp in employees])
    return f"EMP{str(last_id + 1).zfill(3)}"

# Function to onboard new employee
def onboard_employee():
    """Complete onboarding workflow for new employee"""
    print("\n" + "="*70)
    print("EMPLOYEE ONBOARDING WORKFLOW")
    print("="*70)
    
    # Step 1: Employee Information
    print("\nSTEP 1: Employee Information")
    print("-"*70)
    
    first_name = input("First Name: ").strip()
    last_name = input("Last Name: ").strip()
    email = input("Email Address: ").strip()
    department = input("Department: ").strip()
    title = input("Job Title: ").strip()
    start_date = input("Start Date (YYYY-MM-DD): ").strip()
    manager = input("Manager Name: ").strip()
    
    if not all([first_name, last_name, email, department, title]):
        print("\nERROR: All fields are required!")
        return
    
    full_name = f"{first_name} {last_name}"
    
    employees = load_employees()
    employee_id = generate_employee_id(employees)
    
    # Step 2: Account Creation
    print("\nSTEP 2: Account Creation")
    print("-"*70)
    print("Creating accounts...")
    
    accounts = {
        'active_directory': f"{first_name.lower()}.{last_name.lower()}",
        'email': email,
        'vpn': f"{first_name.lower()}{last_name.lower()}",
        'status': 'Active'
    }
    
    print(f"  Active Directory: {accounts['active_directory']} - CREATED")
    print(f"  Email: {accounts['email']} - CREATED")
    print(f"  VPN Access: {accounts['vpn']} - CREATED")
    
    # Step 3: Asset Assignment
    print("\nSTEP 3: Asset Assignment")
    print("-"*70)
    print("Available assets to assign:")
    print("1. Laptop")
    print("2. Phone")
    print("3. Monitor")
    print("4. Keyboard & Mouse")
    print("5. Headset")
    
    asset_choices = input("\nSelect assets (comma-separated, e.g., 1,2,3): ").strip()
    
    assigned_assets = []
    asset_map = {
        '1': 'Laptop',
        '2': 'Phone',
        '3': 'Monitor',
        '4': 'Keyboard & Mouse',
        '5': 'Headset'
    }
    
    if asset_choices:
        for choice in asset_choices.split(','):
            choice = choice.strip()
            if choice in asset_map:
                asset_name = asset_map[choice]
                serial = f"SN{datetime.now().strftime('%Y%m%d%H%M%S')}"
                
                asset = {
                    'asset_type': asset_name,
                    'serial_number': serial,
                    'assigned_to': employee_id,
                    'assigned_date': datetime.now().strftime('%Y-%m-%d'),
                    'status': 'Assigned'
                }
                
                assigned_assets.append(asset)
                print(f"  {asset_name} (SN: {serial}) - ASSIGNED")
    
    # Step 4: Access Provisioning
    print("\nSTEP 4: Access Provisioning")
    print("-"*70)
    print("Available access groups:")
    print("1. Department Access")
    print("2. Email & Calendar")
    print("3. File Shares")
    print("4. VPN Access")
    print("5. Application Access")
    
    access_choices = input("\nSelect access groups (comma-separated): ").strip()
    
    access_groups = []
    access_map = {
        '1': 'Department Access',
        '2': 'Email & Calendar',
        '3': 'File Shares',
        '4': 'VPN Access',
        '5': 'Application Access'
    }
    
    if access_choices:
        for choice in access_choices.split(','):
            choice = choice.strip()
            if choice in access_map:
                access_groups.append(access_map[choice])
                print(f"  {access_map[choice]} - GRANTED")
    
    # Create employee record
    new_employee = {
        'employee_id': employee_id,
        'first_name': first_name,
        'last_name': last_name,
        'full_name': full_name,
        'email': email,
        'department': department,
        'title': title,
        'manager': manager,
        'start_date': start_date,
        'status': 'Active',
        'accounts': accounts,
        'assets': assigned_assets,
        'access_groups': access_groups,
        'onboarded_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    employees.append(new_employee)
    save_employees(employees)
    
    # Save assets
    all_assets = load_assets()
    all_assets.extend(assigned_assets)
    save_assets(all_assets)
    
    # Log audit
    log_audit('ONBOARDING', full_name, f"Employee onboarded - ID: {employee_id}")
    
    # Summary
    print("\n" + "="*70)
    print("ONBOARDING COMPLETE")
    print("="*70)
    print(f"Employee ID: {employee_id}")
    print(f"Name: {full_name}")
    print(f"Email: {email}")
    print(f"Department: {department}")
    print(f"Assets Assigned: {len(assigned_assets)}")
    print(f"Access Groups: {len(access_groups)}")
    print("="*70)
    print("\nAll accounts created and access provisioned successfully!")
    
# Function to offboard employee
def offboard_employee():
    """Complete offboarding workflow for departing employee"""
    employees = load_employees()
    
    active_employees = [emp for emp in employees if emp['status'] == 'Active']
    
    if not active_employees:
        print("\nNo active employees found.")
        return
    
    print("\n" + "="*70)
    print("EMPLOYEE OFFBOARDING WORKFLOW")
    print("="*70)
    
    print("\nActive Employees:")
    for idx, emp in enumerate(active_employees, 1):
        print(f"{idx}. {emp['full_name']} - {emp['title']} ({emp['department']})")
    
    try:
        choice = int(input("\nSelect employee to offboard (0 to cancel): "))
        
        if choice == 0:
            return
        
        if choice < 1 or choice > len(active_employees):
            print("\nInvalid selection!")
            return
        
        employee = active_employees[choice - 1]
        
        print(f"\nOffboarding: {employee['full_name']}")
        print("-"*70)
        
        # Confirm
        confirm = input(f"Are you sure you want to offboard {employee['full_name']}? (yes/no): ").strip().lower()
        
        if confirm != 'yes':
            print("\nOffboarding cancelled.")
            return
        
        # Step 1: Account Deactivation
        print("\nSTEP 1: Account Deactivation")
        print("-"*70)
        
        employee['accounts']['status'] = 'Disabled'
        
        print(f"  Active Directory: {employee['accounts']['active_directory']} - DISABLED")
        print(f"  Email: {employee['accounts']['email']} - DISABLED")
        print(f"  VPN Access: {employee['accounts']['vpn']} - REVOKED")
        
        # Step 2: Access Removal
        print("\nSTEP 2: Access Removal")
        print("-"*70)
        
        for group in employee['access_groups']:
            print(f"  {group} - REMOVED")
        
        employee['access_groups'] = []
        
        # Step 3: Asset Recovery
        print("\nSTEP 3: Asset Recovery")
        print("-"*70)
        
        if employee['assets']:
            print(f"Assets to be returned ({len(employee['assets'])}):")
            
            for asset in employee['assets']:
                print(f"  {asset['asset_type']} (SN: {asset['serial_number']})")
                returned = input(f"    Mark as returned? (y/n): ").strip().lower()
                
                if returned == 'y':
                    asset['status'] = 'Returned'
                    asset['return_date'] = datetime.now().strftime('%Y-%m-%d')
                    print(f"    Status: RETURNED")
                else:
                    asset['status'] = 'Pending Return'
                    print(f"    Status: PENDING RETURN")
        else:
            print("  No assets assigned")
        
        # Step 4: Exit Details
        print("\nSTEP 4: Exit Details")
        print("-"*70)
        
        last_day = input("Last Working Day (YYYY-MM-DD): ").strip()
        exit_reason = input("Exit Reason (optional): ").strip()
        notes = input("Additional Notes (optional): ").strip()
        
        # Update employee record
        employee['status'] = 'Inactive'
        employee['last_day'] = last_day
        employee['exit_reason'] = exit_reason
        employee['exit_notes'] = notes
        employee['offboarded_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Save changes
        save_employees(employees)
        
        # Update assets
        all_assets = load_assets()
        for emp_asset in employee['assets']:
            for asset in all_assets:
                if asset['serial_number'] == emp_asset['serial_number']:
                    asset['status'] = emp_asset['status']
                    if 'return_date' in emp_asset:
                        asset['return_date'] = emp_asset['return_date']
        
        save_assets(all_assets)
        
        # Log audit
        log_audit('OFFBOARDING', employee['full_name'], f"Employee offboarded - ID: {employee['employee_id']}")
        
        # Summary
        print("\n" + "="*70)
        print("OFFBOARDING COMPLETE")
        print("="*70)
        print(f"Employee: {employee['full_name']}")
        print(f"Employee ID: {employee['employee_id']}")
        print(f"Last Day: {last_day}")
        print(f"Accounts: DISABLED")
        print(f"Access: REMOVED")
        print(f"Assets: {len([a for a in employee['assets'] if a['status'] == 'Returned'])} returned, "
              f"{len([a for a in employee['assets'] if a['status'] == 'Pending Return'])} pending")
        print("="*70)
        print("\nOffboarding process completed successfully!")
    
    except ValueError:
        print("\nInvalid input!")
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        
# Function to view employee directory
def view_employee_directory():
    """Display all employees"""
    employees = load_employees()
    
    if not employees:
        print("\nNo employees found.")
        return
    
    print("\n" + "="*80)
    print("EMPLOYEE DIRECTORY")
    print("="*80)
    
    print("\nFilter by:")
    print("1. All Employees")
    print("2. Active Only")
    print("3. Inactive Only")
    
    filter_choice = input("\nSelect filter (1-3): ").strip()
    
    if filter_choice == '2':
        filtered = [emp for emp in employees if emp['status'] == 'Active']
    elif filter_choice == '3':
        filtered = [emp for emp in employees if emp['status'] == 'Inactive']
    else:
        filtered = employees
    
    if not filtered:
        print("\nNo employees found matching filter.")
        return
    
    print(f"\nTotal Employees: {len(filtered)}")
    print("="*80)
    
    for emp in filtered:
        print(f"\nEmployee ID: {emp['employee_id']}")
        print(f"Name: {emp['full_name']}")
        print(f"Email: {emp['email']}")
        print(f"Department: {emp['department']}")
        print(f"Title: {emp['title']}")
        print(f"Status: {emp['status']}")
        print(f"Start Date: {emp['start_date']}")
        
        if emp['status'] == 'Active':
            print(f"Assets: {len(emp['assets'])}")
            print(f"Access Groups: {len(emp['access_groups'])}")
        else:
            print(f"Last Day: {emp.get('last_day', 'N/A')}")
        
        print("-"*80)

# Function to view employee details
def view_employee_details():
    """View detailed information for a specific employee"""
    employees = load_employees()
    
    if not employees:
        print("\nNo employees found.")
        return
    
    print("\n--- View Employee Details ---")
    
    search = input("Enter employee name or ID: ").strip().lower()
    
    results = [emp for emp in employees if 
               search in emp['full_name'].lower() or 
               search in emp['employee_id'].lower()]
    
    if not results:
        print(f"\nNo employees found matching '{search}'")
        return
    
    if len(results) > 1:
        print("\nMultiple employees found:")
        for idx, emp in enumerate(results, 1):
            print(f"{idx}. {emp['full_name']} ({emp['employee_id']})")
        
        try:
            choice = int(input("\nSelect employee (0 to cancel): "))
            if choice == 0:
                return
            if 1 <= choice <= len(results):
                employee = results[choice - 1]
            else:
                print("\nInvalid selection!")
                return
        except ValueError:
            print("\nInvalid input!")
            return
    else:
        employee = results
    
    # Display detailed information
    print("\n" + "="*80)
    print(f"EMPLOYEE DETAILS: {employee['full_name']}")
    print("="*80)
    
    print(f"\nEmployee ID: {employee['employee_id']}")
    print(f"Name: {employee['full_name']}")
    print(f"Email: {employee['email']}")
    print(f"Department: {employee['department']}")
    print(f"Title: {employee['title']}")
    print(f"Manager: {employee.get('manager', 'N/A')}")
    print(f"Start Date: {employee['start_date']}")
    print(f"Status: {employee['status']}")
    
    print("\nAccounts:")
    for account, value in employee['accounts'].items():
        print(f"  {account}: {value}")
    
    print("\nAssets:")
    if employee['assets']:
        for asset in employee['assets']:
            print(f"  {asset['asset_type']} - SN: {asset['serial_number']} - Status: {asset['status']}")
    else:
        print("  None")
    
    print("\nAccess Groups:")
    if employee['access_groups']:
        for group in employee['access_groups']:
            print(f"  - {group}")
    else:
        print("  None")
    
    if employee['status'] == 'Inactive':
        print(f"\nLast Day: {employee.get('last_day', 'N/A')}")
        print(f"Exit Reason: {employee.get('exit_reason', 'N/A')}")
    
    print("="*80)

# Function to generate reports
def generate_reports():
    """Generate onboarding/offboarding reports"""
    employees = load_employees()
    
    if not employees:
        print("\nNo employee data available.")
        return
    
    print("\n" + "="*80)
    print("EMPLOYEE LIFECYCLE REPORTS")
    print("="*80)
    
    active = [emp for emp in employees if emp['status'] == 'Active']
    inactive = [emp for emp in employees if emp['status'] == 'Inactive']
    
    print(f"\nTotal Employees: {len(employees)}")
    print(f"Active: {len(active)}")
    print(f"Inactive: {len(inactive)}")
    
    # Department breakdown
    departments = {}
    for emp in active:
        dept = emp['department']
        departments[dept] = departments.get(dept, 0) + 1
    
    print("\nActive Employees by Department:")
    for dept, count in departments.items():
        print(f"  {dept}: {count}")
    
    # Asset statistics
    all_assets = load_assets()
    assigned = [a for a in all_assets if a['status'] == 'Assigned']
    returned = [a for a in all_assets if a['status'] == 'Returned']
    pending = [a for a in all_assets if a['status'] == 'Pending Return']
    
    print(f"\nAsset Statistics:")
    print(f"  Total Assets: {len(all_assets)}")
    print(f"  Assigned: {len(assigned)}")
    print(f"  Returned: {len(returned)}")
    print(f"  Pending Return: {len(pending)}")
    
    # Recent activity
    if os.path.exists(AUDIT_LOG_FILE):
        with open(AUDIT_LOG_FILE, 'r') as f:
            logs = json.load(f)
        
        recent = logs[-10:]
        recent.reverse()
        
        print("\nRecent Activity (Last 10):")
        for log in recent:
            print(f"  [{log['timestamp']}] {log['action']}: {log['employee']}")
    
    print("="*80)
    
    # Export option
    export = input("\nExport report to file? (y/n): ").strip().lower()
    
    if export == 'y':
        filename = f"employee_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(filename, 'w') as f:
            f.write("EMPLOYEE LIFECYCLE REPORT\n")
            f.write("="*80 + "\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"Total Employees: {len(employees)}\n")
            f.write(f"Active: {len(active)}\n")
            f.write(f"Inactive: {len(inactive)}\n\n")
            f.write("Active Employees by Department:\n")
            for dept, count in departments.items():
                f.write(f"  {dept}: {count}\n")
        
        print(f"\nReport exported to: {filename}")

# Main menu
def show_menu():
    print("\n" + "="*70)
    print("  EMPLOYEE ONBOARDING/OFFBOARDING SYSTEM")
    print("="*70)
    print("1. Onboard New Employee")
    print("2. Offboard Employee")
    print("3. View Employee Directory")
    print("4. View Employee Details")
    print("5. Generate Reports")
    print("6. Exit")
    print("-"*70)

# Main program
def main():
    while True:
        show_menu()
        choice = input("\nSelect an option (1-6): ").strip()
        
        if choice == '1':
            onboard_employee()
        
        elif choice == '2':
            offboard_employee()
        
        elif choice == '3':
            view_employee_directory()
        
        elif choice == '4':
            view_employee_details()
        
        elif choice == '5':
            generate_reports()
        
        elif choice == '6':
            print("\nThank you for using the Onboarding/Offboarding System!")
            print("Exiting...\n")
            break
        
        else:
            print("\nInvalid option. Please select 1-6.")
        
        if choice != '6':
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()