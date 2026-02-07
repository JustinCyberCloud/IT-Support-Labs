# Lab 7: Automated Onboarding/Offboarding System

## Description
A comprehensive Python-based system for automating employee onboarding and offboarding processes. Simulates account creation, asset assignment, access provisioning, and complete lifecycle management.

## Features
- **Employee Onboarding**: Complete new hire setup workflow
- **Account Creation**: Simulate user accounts across multiple systems
- **Asset Assignment**: Track laptops, phones, monitors, and equipment
- **Access Provisioning**: Assign groups, permissions, and system access
- **Employee Offboarding**: Structured departure process
- **Asset Recovery**: Track returned equipment
- **Account Deactivation**: Disable access across all systems
- **Audit Trail**: Complete logging of all actions
- **Employee Directory**: View all active and inactive employees
- **Reports**: Generate onboarding/offboarding reports

## Requirements
- Python 3.7 or higher
- No external libraries required (uses standard library)

## How to Run

1. Run the program:
python onboarding_system.py


## Usage Examples

### Onboard a New Employee
- Select option 1
- Enter employee details (name, email, department, title, start date)
- Select asset assignments (laptop, phone, monitor)
- Choose access groups and systems
- System creates accounts and logs all actions

### Offboard an Employee
- Select option 2
- Select employee to offboard
- System disables accounts across all systems
- Track asset returns
- Generate offboarding report

### View Employee Directory
- Select option 3
- See all employees with status, department, and assets
- Filter by active/inactive status

### Generate Reports
- Select option 5
- View onboarding/offboarding statistics
- Export audit logs

## Onboarding Workflow

1. **Employee Information**: Name, email, department, title, start date
2. **Account Creation**: 
- Active Directory account
- Email account
- VPN access
- System logins
3. **Asset Assignment**:
- Laptop (with serial number)
- Phone (with number)
- Monitor
- Keyboard/Mouse
- Other equipment
4. **Access Provisioning**:
- Department groups
- Role-based access
- Application permissions
5. **Documentation**: Complete audit trail

## Offboarding Workflow

1. **Select Employee**: Choose from active employees
2. **Account Deactivation**:
- Disable AD account
- Disable email
- Revoke VPN access
- Remove system access
3. **Asset Recovery**:
- Mark assets as returned
- Track condition
- Reassign to inventory
4. **Exit Interview**: Record departure details
5. **Final Report**: Generate offboarding summary

## Common Use Cases
- New hire IT setup automation
- Standardized onboarding process
- Employee departure management
- Asset lifecycle tracking
- Compliance and audit requirements
- IT inventory management
- Access control documentation

## Skills Demonstrated
- Employee lifecycle management
- Workflow automation
- Asset tracking and inventory
- Access control concepts
- Audit logging and compliance
- Data management and reporting
- Process standardization
- IT security best practices