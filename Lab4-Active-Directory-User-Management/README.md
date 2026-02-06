# Lab 4: Active Directory User Management

## Description
A PowerShell script that simulates Active Directory user management tasks. Practice common IT admin operations like creating users, managing groups, and generating reports.

## Features
- **Create Single User**: Add new user accounts with properties
- **Bulk User Creation**: Import users from CSV file
- **Modify User Properties**: Update user information
- **Disable/Enable Accounts**: Manage user account status
- **Group Management**: Add/remove users from groups
- **User Reports**: Generate lists of users and their properties
- **Search Users**: Find users by various criteria
- **Export to CSV**: Save user data for documentation

## Requirements
- Windows PowerShell 5.1 or higher
- No actual Active Directory required (simulated environment)

## How to Run

1. Open PowerShell
2. Navigate to the script directory
3. Run the script:
.\ADUserManagement.ps1


## Usage Examples

### Create a Single User
- Select option 1
- Enter username, full name, email, department
- User is created in the simulated database

### Bulk Create Users from CSV
- Select option 2
- Prepare a CSV file with columns: Username, FirstName, LastName, Email, Department
- Import the file to create multiple users at once

### Disable a User Account
- Select option 4
- Enter username
- Account status changed to "Disabled"

### Generate User Report
- Select option 7
- View all users with their properties
- Export to CSV if needed

## Sample CSV Format for Bulk Import

```csv
Username,FirstName,LastName,Email,Department
jsmith,John,Smith,jsmith@company.com,IT
mjones,Mary,Jones,mjones@company.com,HR
bwilson,Bob,Wilson,bwilson@company.com,Sales
Common Use Cases
Onboarding new employees
Offboarding departing employees
Bulk user creation for new departments
Auditing user accounts
Managing user access and permissions
Documenting user changes for compliance
Skills Demonstrated
PowerShell scripting and automation
Active Directory concepts and structure
User lifecycle management
CSV data manipulation
Bulk operations and efficiency
Documentation and reporting
IT security best practices

---