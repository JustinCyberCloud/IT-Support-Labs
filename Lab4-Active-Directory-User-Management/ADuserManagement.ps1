# Active Directory User Management Simulator
# IT Support Lab 4

# Initialize user database file
$script:userDatabase = "ad_users.json"

# Function to load users from database
function Load-Users {
    if (Test-Path $script:userDatabase) {
        $json = Get-Content $script:userDatabase -Raw
        return $json | ConvertFrom-Json
    } else {
        return @()
    }
}

# Function to save users to database
function Save-Users {
    param($Users)
    $Users | ConvertTo-Json -Depth 10 | Set-Content $script:userDatabase
    Write-Host "Database updated successfully" -ForegroundColor Green
}

# Function to create a single user
function New-ADUserAccount {
    Write-Host ""
    Write-Host "--- Create New User Account ---" -ForegroundColor Yellow
    
    $username = Read-Host "Username"
    $firstName = Read-Host "First Name"
    $lastName = Read-Host "Last Name"
    $email = Read-Host "Email"
    $department = Read-Host "Department"
    $title = Read-Host "Job Title"
    
    # Load existing users
    $users = Load-Users
    
    # Check if username already exists
    if ($users | Where-Object { $_.Username -eq $username }) {
        Write-Host ""
        Write-Host "ERROR: Username '$username' already exists" -ForegroundColor Red
        return
    }
    
    # Create new user object
    $newUser = [PSCustomObject]@{
        Username = $username
        FirstName = $firstName
        LastName = $lastName
        FullName = "$firstName $lastName"
        Email = $email
        Department = $department
        Title = $title
        Status = "Enabled"
        CreatedDate = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
        LastModified = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
        Groups = @()
    }
    
    # Add to users array
    $users = @($users) + $newUser
    
    # Save to database
    Save-Users -Users $users
    
    Write-Host ""
    Write-Host "SUCCESS: User '$username' created successfully!" -ForegroundColor Green
    Write-Host "Full Name: $($newUser.FullName)" -ForegroundColor Cyan
    Write-Host "Email: $($newUser.Email)" -ForegroundColor Cyan
    Write-Host "Department: $($newUser.Department)" -ForegroundColor Cyan
}

# Function to bulk create users from CSV
function Import-BulkUsers {
    Write-Host ""
    Write-Host "--- Bulk Import Users from CSV ---" -ForegroundColor Yellow
    
    $csvPath = Read-Host "Enter CSV file path"
    
    if (-not (Test-Path $csvPath)) {
        Write-Host ""
        Write-Host "ERROR: File not found" -ForegroundColor Red
        return
    }
    
    try {
        $csvUsers = Import-Csv -Path $csvPath
        $users = Load-Users
        $created = 0
        $skipped = 0
        
        Write-Host ""
        Write-Host "Processing users..." -ForegroundColor Cyan
        
        foreach ($csvUser in $csvUsers) {
            # Check if user already exists
            if ($users | Where-Object { $_.Username -eq $csvUser.Username }) {
                Write-Host "SKIPPED: $($csvUser.Username) - already exists" -ForegroundColor Yellow
                $skipped++
                continue
            }
            
            # Create user object
            $newUser = [PSCustomObject]@{
                Username = $csvUser.Username
                FirstName = $csvUser.FirstName
                LastName = $csvUser.LastName
                FullName = "$($csvUser.FirstName) $($csvUser.LastName)"
                Email = $csvUser.Email
                Department = $csvUser.Department
                Title = if ($csvUser.Title) { $csvUser.Title } else { "Employee" }
                Status = "Enabled"
                CreatedDate = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
                LastModified = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
                Groups = @()
            }
            
            $users = @($users) + $newUser
            Write-Host "CREATED: $($csvUser.Username)" -ForegroundColor Green
            $created++
        }
        
        # Save all users
        Save-Users -Users $users
        
        Write-Host ""
        Write-Host "========================================" -ForegroundColor Cyan
        Write-Host "Bulk Import Complete" -ForegroundColor Green
        Write-Host "Users Created: $created" -ForegroundColor Green
        Write-Host "Users Skipped: $skipped" -ForegroundColor Yellow
        Write-Host "========================================" -ForegroundColor Cyan
    }
    catch {
        Write-Host ""
        Write-Host "ERROR: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# Function to modify user properties
function Set-ADUserProperties {
    Write-Host ""
    Write-Host "--- Modify User Properties ---" -ForegroundColor Yellow
    
    $username = Read-Host "Enter username to modify"
    
    $users = Load-Users
    $user = $users | Where-Object { $_.Username -eq $username }
    
    if (-not $user) {
        Write-Host ""
        Write-Host "ERROR: User '$username' not found" -ForegroundColor Red
        return
    }
    
    Write-Host ""
    Write-Host "Current User Information:" -ForegroundColor Cyan
    Write-Host "Username: $($user.Username)"
    Write-Host "Full Name: $($user.FullName)"
    Write-Host "Email: $($user.Email)"
    Write-Host "Department: $($user.Department)"
    Write-Host "Title: $($user.Title)"
    Write-Host "Status: $($user.Status)"
    
    Write-Host ""
    Write-Host "Enter new values (press Enter to keep current value):" -ForegroundColor Yellow
    
    $newEmail = Read-Host "Email [$($user.Email)]"
    $newDepartment = Read-Host "Department [$($user.Department)]"
    $newTitle = Read-Host "Title [$($user.Title)]"
    
    # Update properties if new values provided
    if ($newEmail) { $user.Email = $newEmail }
    if ($newDepartment) { $user.Department = $newDepartment }
    if ($newTitle) { $user.Title = $newTitle }
    
    $user.LastModified = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    
    # Save changes
    Save-Users -Users $users
    
    Write-Host ""
    Write-Host "SUCCESS: User '$username' updated successfully!" -ForegroundColor Green
}

# Function to disable user account
function Disable-ADUserAccount {
    Write-Host ""
    Write-Host "--- Disable User Account ---" -ForegroundColor Yellow
    
    $username = Read-Host "Enter username to disable"
    
    $users = Load-Users
    $user = $users | Where-Object { $_.Username -eq $username }
    
    if (-not $user) {
        Write-Host ""
        Write-Host "ERROR: User '$username' not found" -ForegroundColor Red
        return
    }
    
    if ($user.Status -eq "Disabled") {
        Write-Host ""
        Write-Host "WARNING: User '$username' is already disabled" -ForegroundColor Yellow
        return
    }
    
    $user.Status = "Disabled"
    $user.LastModified = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    
    Save-Users -Users $users
    
    Write-Host ""
    Write-Host "SUCCESS: User '$username' has been disabled" -ForegroundColor Green
}

# Function to enable user account
function Enable-ADUserAccount {
    Write-Host ""
    Write-Host "--- Enable User Account ---" -ForegroundColor Yellow
    
    $username = Read-Host "Enter username to enable"
    
    $users = Load-Users
    $user = $users | Where-Object { $_.Username -eq $username }
    
    if (-not $user) {
        Write-Host ""
        Write-Host "ERROR: User '$username' not found" -ForegroundColor Red
        return
    }
    
    if ($user.Status -eq "Enabled") {
        Write-Host ""
        Write-Host "WARNING: User '$username' is already enabled" -ForegroundColor Yellow
        return
    }
    
    $user.Status = "Enabled"
    $user.LastModified = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    
    Save-Users -Users $users
    
    Write-Host ""
    Write-Host "SUCCESS: User '$username' has been enabled" -ForegroundColor Green
}

# Function to manage user groups
function Manage-UserGroups {
    Write-Host ""
    Write-Host "--- Manage User Groups ---" -ForegroundColor Yellow
    
    $username = Read-Host "Enter username"
    
    $users = Load-Users
    $user = $users | Where-Object { $_.Username -eq $username }
    
    if (-not $user) {
        Write-Host ""
        Write-Host "ERROR: User '$username' not found" -ForegroundColor Red
        return
    }
    
    Write-Host ""
    Write-Host "Current Groups: $($user.Groups -join ', ')" -ForegroundColor Cyan
    if ($user.Groups.Count -eq 0) {
        Write-Host "Current Groups: None" -ForegroundColor Cyan
    }
    
    Write-Host ""
    Write-Host "1. Add to group"
    Write-Host "2. Remove from group"
    $choice = Read-Host "Select action (1-2)"
    
    if ($choice -eq '1') {
        $groupName = Read-Host "Enter group name to add"
        
        if ($user.Groups -contains $groupName) {
            Write-Host ""
            Write-Host "WARNING: User is already in group '$groupName'" -ForegroundColor Yellow
        } else {
            $user.Groups += $groupName
            $user.LastModified = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
            Save-Users -Users $users
            Write-Host ""
            Write-Host "SUCCESS: User added to group '$groupName'" -ForegroundColor Green
        }
    }
    elseif ($choice -eq '2') {
        $groupName = Read-Host "Enter group name to remove"
        
        if ($user.Groups -contains $groupName) {
            $user.Groups = $user.Groups | Where-Object { $_ -ne $groupName }
            $user.LastModified = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
            Save-Users -Users $users
            Write-Host ""
            Write-Host "SUCCESS: User removed from group '$groupName'" -ForegroundColor Green
        } else {
            Write-Host ""
            Write-Host "WARNING: User is not in group '$groupName'" -ForegroundColor Yellow
        }
    }
}

# Function to generate user report
function Get-ADUserReport {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "   ACTIVE DIRECTORY USER REPORT" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    
    $users = Load-Users
    
    if ($users.Count -eq 0) {
        Write-Host ""
        Write-Host "No users found in the database" -ForegroundColor Yellow
        return
    }
    
    Write-Host ""
    Write-Host "Total Users: $($users.Count)" -ForegroundColor Green
    
    $enabled = ($users | Where-Object { $_.Status -eq "Enabled" }).Count
    $disabled = ($users | Where-Object { $_.Status -eq "Disabled" }).Count
    
    Write-Host "Enabled: $enabled" -ForegroundColor Green
    Write-Host "Disabled: $disabled" -ForegroundColor Yellow
    
    Write-Host ""
    Write-Host "User List:" -ForegroundColor Cyan
    Write-Host "-" * 120
    
    $users | Format-Table -Property Username, FullName, Email, Department, Title, Status -AutoSize
    
    Write-Host "========================================" -ForegroundColor Cyan
    
    # Option to export
    Write-Host ""
    $export = Read-Host "Export to CSV? (y/n)"
    
    if ($export -eq 'y') {
        $filename = "AD_Users_Report_$(Get-Date -Format 'yyyyMMdd_HHmmss').csv"
        $users | Export-Csv -Path $filename -NoTypeInformation
        Write-Host ""
        Write-Host "Report exported to: $filename" -ForegroundColor Green
    }
}

# Function to search users
function Search-ADUsers {
    Write-Host ""
    Write-Host "--- Search Users ---" -ForegroundColor Yellow
    
    Write-Host ""
    Write-Host "Search by:"
    Write-Host "1. Username"
    Write-Host "2. Department"
    Write-Host "3. Status"
    $searchType = Read-Host "Select search type (1-3)"
    
    $users = Load-Users
    
    if ($searchType -eq '1') {
        $searchTerm = Read-Host "Enter username (partial match)"
        $results = $users | Where-Object { $_.Username -like "*$searchTerm*" }
    }
    elseif ($searchType -eq '2') {
        $searchTerm = Read-Host "Enter department"
        $results = $users | Where-Object { $_.Department -like "*$searchTerm*" }
    }
    elseif ($searchType -eq '3') {
        $searchTerm = Read-Host "Enter status (Enabled/Disabled)"
        $results = $users | Where-Object { $_.Status -eq $searchTerm }
    }
    else {
        Write-Host ""
        Write-Host "Invalid search type" -ForegroundColor Red
        return
    }
    
    Write-Host ""
    if ($results.Count -eq 0) {
        Write-Host "No users found matching your search" -ForegroundColor Yellow
    } else {
        Write-Host "Found $($results.Count) user(s):" -ForegroundColor Green
        Write-Host ""
        $results | Format-Table -Property Username, FullName, Email, Department, Status -AutoSize
    }
}

# Function to view single user details
function Get-ADUserDetails {
    Write-Host ""
    Write-Host "--- View User Details ---" -ForegroundColor Yellow
    
    $username = Read-Host "Enter username"
    
    $users = Load-Users
    $user = $users | Where-Object { $_.Username -eq $username }
    
    if (-not $user) {
        Write-Host ""
        Write-Host "ERROR: User '$username' not found" -ForegroundColor Red
        return
    }
    
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "USER DETAILS: $($user.Username)" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "Full Name:      $($user.FullName)"
    Write-Host "Email:          $($user.Email)"
    Write-Host "Department:     $($user.Department)"
    Write-Host "Title:          $($user.Title)"
    Write-Host "Status:         $($user.Status)"
    Write-Host "Created:        $($user.CreatedDate)"
    Write-Host "Last Modified:  $($user.LastModified)"
    Write-Host "Groups:         $($user.Groups -join ', ')"
    if ($user.Groups.Count -eq 0) {
        Write-Host "Groups:         None"
    }
    Write-Host "========================================" -ForegroundColor Cyan
}

# Main menu
function Show-Menu {
    Clear-Host
    Write-Host "================================================" -ForegroundColor Cyan
    Write-Host "   ACTIVE DIRECTORY USER MANAGEMENT" -ForegroundColor Cyan
    Write-Host "================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "1.  Create Single User" -ForegroundColor White
    Write-Host "2.  Bulk Import Users from CSV" -ForegroundColor White
    Write-Host "3.  Modify User Properties" -ForegroundColor White
    Write-Host "4.  Disable User Account" -ForegroundColor White
    Write-Host "5.  Enable User Account" -ForegroundColor White
    Write-Host "6.  Manage User Groups" -ForegroundColor White
    Write-Host "7.  Generate User Report" -ForegroundColor White
    Write-Host "8.  Search Users" -ForegroundColor White
    Write-Host "9.  View User Details" -ForegroundColor White
    Write-Host "10. Exit" -ForegroundColor White
    Write-Host "------------------------------------------------" -ForegroundColor Cyan
}

# Main program loop
do {
    Show-Menu
    $choice = Read-Host "`nSelect an option (1-10)"
    
    switch ($choice) {
        '1' { New-ADUserAccount }
        '2' { Import-BulkUsers }
        '3' { Set-ADUserProperties }
        '4' { Disable-ADUserAccount }
        '5' { Enable-ADUserAccount }
        '6' { Manage-UserGroups }
        '7' { Get-ADUserReport }
        '8' { Search-ADUsers }
        '9' { Get-ADUserDetails }
        '10' {
            Write-Host ""
            Write-Host "Thank you for using AD User Management!" -ForegroundColor Green
            Write-Host "Exiting..." -ForegroundColor Yellow
            Write-Host ""
            break
        }
        default {
            Write-Host ""
            Write-Host "Invalid option. Please select 1-10." -ForegroundColor Red
        }
    }
    
    if ($choice -ne '10') {
        Write-Host ""
        Write-Host "Press any key to continue..."
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    }
    
} while ($choice -ne '10')