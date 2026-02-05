# Password Reset Automation Script
# IT Support Lab 2

# Function to generate a secure random password
function Generate-SecurePassword {
    param(
        [int]$Length = 12
    )
    
    $uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    $lowercase = "abcdefghijklmnopqrstuvwxyz"
    $numbers = "0123456789"
    $special = "!@#$%^&*()"
    
    $allChars = $uppercase + $lowercase + $numbers + $special
    
    # Ensure at least one of each type
    $password = ""
    $password += $uppercase[(Get-Random -Maximum $uppercase.Length)]
    $password += $lowercase[(Get-Random -Maximum $lowercase.Length)]
    $password += $numbers[(Get-Random -Maximum $numbers.Length)]
    $password += $special[(Get-Random -Maximum $special.Length)]
    
    # Fill the rest randomly
    for ($i = 4; $i -lt $Length; $i++) {
        $password += $allChars[(Get-Random -Maximum $allChars.Length)]
    }
    
    # Shuffle the password
    $passwordArray = $password.ToCharArray()
    $shuffled = $passwordArray | Get-Random -Count $passwordArray.Length
    $finalPassword = -join $shuffled
    
    return $finalPassword
}

# Function to validate password strength
function Test-PasswordStrength {
    param(
        [string]$Password
    )
    
    $strength = @{
        Length = $Password.Length -ge 8
        Uppercase = $Password -cmatch '[A-Z]'
        Lowercase = $Password -cmatch '[a-z]'
        Number = $Password -match '[0-9]'
        Special = $Password -match '[!@#$%^&*()]'
    }
    
    $passed = ($strength.Values | Where-Object { $_ -eq $true }).Count
    $total = $strength.Count
    
    return @{
        Strength = $strength
        Passed = $passed
        Total = $total
        IsStrong = $passed -eq $total
    }
}

# Function to log password reset activity
function Write-PasswordLog {
    param(
        [string]$Username,
        [string]$Action,
        [string]$Details = ""
    )
    
    $logFile = "password_reset_log.csv"
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    
    $logEntry = [PSCustomObject]@{
        Timestamp = $timestamp
        Username = $Username
        Action = $Action
        Details = $Details
        PerformedBy = $env:USERNAME
    }
    
    # Create file with headers if it doesn't exist
    if (-not (Test-Path $logFile)) {
        $logEntry | Export-Csv -Path $logFile -NoTypeInformation
    } else {
        $logEntry | Export-Csv -Path $logFile -NoTypeInformation -Append
    }
    
    Write-Host ""
    Write-Host "Activity logged successfully" -ForegroundColor Green
}


# Function to display password strength results
function Show-PasswordStrength {
    param($Result)
    
    Write-Host ""
    Write-Host "========== Password Strength Analysis ==========" -ForegroundColor Cyan
    Write-Host "Length (8+ chars):    " -NoNewline
    if ($Result.Strength.Length) { Write-Host "PASS" -ForegroundColor Green } else { Write-Host "FAIL" -ForegroundColor Red }
    
    Write-Host "Uppercase letter:     " -NoNewline
    if ($Result.Strength.Uppercase) { Write-Host "PASS" -ForegroundColor Green } else { Write-Host "FAIL" -ForegroundColor Red }
    
    Write-Host "Lowercase letter:     " -NoNewline
    if ($Result.Strength.Lowercase) { Write-Host "PASS" -ForegroundColor Green } else { Write-Host "FAIL" -ForegroundColor Red }
    
    Write-Host "Number:               " -NoNewline
    if ($Result.Strength.Number) { Write-Host "PASS" -ForegroundColor Green } else { Write-Host "FAIL" -ForegroundColor Red }
    
    Write-Host "Special character:    " -NoNewline
    if ($Result.Strength.Special) { Write-Host "PASS" -ForegroundColor Green } else { Write-Host "FAIL" -ForegroundColor Red }
    
    Write-Host ""
    Write-Host "Score: $($Result.Passed)/$($Result.Total)" -ForegroundColor Yellow
    
    if ($Result.IsStrong) {
        Write-Host "Overall: STRONG PASSWORD" -ForegroundColor Green
    } else {
        Write-Host "Overall: WEAK PASSWORD" -ForegroundColor Red
    }
    Write-Host "================================================" -ForegroundColor Cyan
    Write-Host ""
}

# Function to simulate password reset
function Reset-UserPassword {
    param(
        [string]$Username
    )
    
    Write-Host ""
    Write-Host "--- Simulating Password Reset for: $Username ---" -ForegroundColor Yellow
    
    # Generate new password
    $newPassword = Generate-SecurePassword -Length 12
    
    Write-Host ""
    Write-Host "New password generated successfully!" -ForegroundColor Green
    Write-Host "Temporary Password: $newPassword" -ForegroundColor Cyan
    
    # Validate the generated password
    $validation = Test-PasswordStrength -Password $newPassword
    Write-Host ""
    Write-Host "Password meets all security requirements: " -NoNewline
    if ($validation.IsStrong) {
        Write-Host "YES" -ForegroundColor Green
    }
    
    # Log the activity
    Write-PasswordLog -Username $Username -Action "Password Reset" -Details "Temporary password generated"
    
    Write-Host ""
    Write-Host "User should change password on next login" -ForegroundColor Yellow
    
    # Try to copy to clipboard
    try {
        Set-Clipboard -Value $newPassword
        Write-Host "Password copied to clipboard" -ForegroundColor Green
    } catch {
        Write-Host "Could not copy to clipboard" -ForegroundColor Yellow
    }
}

# Function to view password reset history
function Show-PasswordHistory {
    $logFile = "password_reset_log.csv"
    
    if (Test-Path $logFile) {
        Write-Host ""
        Write-Host "========== Password Reset History ==========" -ForegroundColor Cyan
        $logs = Import-Csv -Path $logFile
        
        if ($logs.Count -eq 0) {
            Write-Host "No password reset activities found." -ForegroundColor Yellow
        } else {
            $logs | Format-Table -AutoSize
            Write-Host "Total activities: $($logs.Count)" -ForegroundColor Green
        }
        Write-Host "===========================================" -ForegroundColor Cyan
        Write-Host ""
    } else {
        Write-Host ""
        Write-Host "No log file found. No password resets have been performed yet." -ForegroundColor Yellow
    }
}

# Main menu function
function Show-Menu {
    Clear-Host
    Write-Host "================================================" -ForegroundColor Cyan
    Write-Host "   PASSWORD RESET AUTOMATION TOOL" -ForegroundColor Cyan
    Write-Host "================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "1. Generate Secure Password" -ForegroundColor White
    Write-Host "2. Validate Password Strength" -ForegroundColor White
    Write-Host "3. Simulate User Password Reset" -ForegroundColor White
    Write-Host "4. View Password Reset History" -ForegroundColor White
    Write-Host "5. Export Logs to Desktop" -ForegroundColor White
    Write-Host "6. Exit" -ForegroundColor White
    Write-Host "------------------------------------------------" -ForegroundColor Cyan
}

# Main program loop
do {
    Show-Menu
    $choice = Read-Host "`nSelect an option (1-6)"
    
    switch ($choice) {
        '1' {
            Write-Host ""
            Write-Host "--- Generate Secure Password ---" -ForegroundColor Yellow
            $length = Read-Host "Enter password length (default: 12, min: 8)"
            
            if ([string]::IsNullOrWhiteSpace($length)) {
                $length = 12
            } else {
                $length = [int]$length
                if ($length -lt 8) {
                    Write-Host "Minimum length is 8. Using 8." -ForegroundColor Yellow
                    $length = 8
                }
            }
            
            $password = Generate-SecurePassword -Length $length
            
            Write-Host ""
            Write-Host "Generated Password: $password" -ForegroundColor Cyan
            
            # Validate it
            $validation = Test-PasswordStrength -Password $password
            Show-PasswordStrength -Result $validation
            
            try {
                Set-Clipboard -Value $password
                Write-Host "Password copied to clipboard" -ForegroundColor Green
            } catch {
                Write-Host "Could not copy to clipboard" -ForegroundColor Yellow
            }
            
            Write-Host ""
            Write-Host "Press any key to continue..."
            $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        }
        
        '2' {
            Write-Host ""
            Write-Host "--- Validate Password Strength ---" -ForegroundColor Yellow
            $testPassword = Read-Host "Enter password to test"
            
            $validation = Test-PasswordStrength -Password $testPassword
            Show-PasswordStrength -Result $validation
            
            Write-Host "Press any key to continue..."
            $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        }
        
        '3' {
            Write-Host ""
            Write-Host "--- Simulate User Password Reset ---" -ForegroundColor Yellow
            $username = Read-Host "Enter username"
            
            if ([string]::IsNullOrWhiteSpace($username)) {
                Write-Host "Username cannot be empty" -ForegroundColor Red
            } else {
                Reset-UserPassword -Username $username
            }
            
            Write-Host ""
            Write-Host "Press any key to continue..."
            $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        }
        
        '4' {
            Show-PasswordHistory
            Write-Host "Press any key to continue..."
            $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        }
        
        '5' {
            $logFile = "password_reset_log.csv"
            if (Test-Path $logFile) {
                $desktopPath = [Environment]::GetFolderPath("Desktop")
                $destFile = Join-Path $desktopPath "password_reset_log.csv"
                Copy-Item -Path $logFile -Destination $destFile -Force
                Write-Host ""
                Write-Host "Log file exported to: $destFile" -ForegroundColor Green
            } else {
                Write-Host ""
                Write-Host "No log file found" -ForegroundColor Red
            }
            
            Write-Host ""
            Write-Host "Press any key to continue..."
            $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        }
        
        '6' {
            Write-Host ""
            Write-Host "Thank you for using Password Reset Automation Tool!" -ForegroundColor Green
            Write-Host "Exiting..." -ForegroundColor Yellow
            Write-Host ""
            break
        }
        
        default {
            Write-Host ""
            Write-Host "Invalid option. Please select 1-6." -ForegroundColor Red
            Write-Host "Press any key to continue..."
            $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        }
    }
    
} while ($choice -ne '6')