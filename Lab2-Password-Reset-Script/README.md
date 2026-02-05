# Lab 2: Password Reset Automation Script

## Description
A PowerShell script for automating password reset tasks in IT support environments. Includes password generation, strength validation, and activity logging.

## Features
- Generate secure random passwords
- Validate password strength (complexity requirements)
- Log all password reset activities with timestamps
- Simulate user account password resets
- View password reset history
- Export logs to CSV

## Requirements
- Windows PowerShell 5.1 or higher
- Run as Administrator (for certain features)

## How to Run

1. Open PowerShell
2. Navigate to the script directory
3. Run the script:
.\PasswordReset.ps1


## Usage Examples

### Generate a Password
- Select option 1
- Choose password length (default: 12 characters)
- Password will be displayed and copied to clipboard

### Validate Password Strength
- Select option 2
- Enter a password to test
- See if it meets complexity requirements

### Simulate Password Reset
- Select option 3
- Enter username
- System generates password and logs the activity

### View Reset History
- Select option 4
- See all password reset activities with timestamps

## Password Requirements
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one number
- At least one special character

## Skills Demonstrated
- PowerShell scripting
- Password security best practices
- Logging and auditing
- User account management simulation
- Input validation
- File I/O operations