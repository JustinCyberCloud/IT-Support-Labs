# Lab 6: Remote Desktop Connection Manager

## Description
A Python-based RDP (Remote Desktop Protocol) connection manager for IT professionals. Store, organize, and quickly connect to multiple remote systems with saved credentials and connection profiles.

## Features
- **Save Connection Profiles**: Store server details (hostname, username, port)
- **Quick Connect**: Launch RDP sessions with one command
- **Credential Management**: Securely store connection information
- **Connection History**: Track when and where you connected
- **Batch Connections**: Connect to multiple servers at once
- **Search/Filter**: Find connections by name, IP, or tags
- **Export/Import**: Backup and restore connection profiles
- **Connection Testing**: Verify server availability before connecting

## Requirements
- Python 3.7 or higher
- Windows OS (for RDP functionality)
- mstsc.exe (built into Windows)

## How to Run

1. Run the program:
python rdp_manager.py


## Usage Examples

### Add a New Connection
- Select option 1
- Enter server name/IP, username, display name, optional tags
- Connection profile saved for future use

### Quick Connect
- Select option 2
- Choose from saved connections
- RDP session launches automatically

### View All Connections
- Select option 3
- See all saved servers with details
- Organized and easy to browse

### Search Connections
- Select option 4
- Search by name, IP, or tags
- Quickly find the server you need

### Connection History
- Select option 5
- View past connections with timestamps
- Track your remote access activity

## Connection Profile Format

Each saved connection includes:
- **Display Name**: Friendly name (e.g., "Production Server")
- **Hostname/IP**: Server address
- **Username**: Login username
- **Port**: RDP port (default: 3389)
- **Tags**: Categories (e.g., "production", "database", "web")
- **Notes**: Additional information

## Common Use Cases
- Managing multiple client servers
- Quick access to frequently used systems
- Organizing servers by environment (dev, test, prod)
- Tracking remote access for documentation
- Batch connecting to server groups
- Server inventory management

## Security Notes
- Passwords are NOT stored (Windows Credential Manager handles this)
- Connection profiles stored locally in JSON format
- Recommended: Use Windows Credential Manager for password storage
- Always follow your organization's security policies

## Skills Demonstrated
- Remote desktop management
- Python file I/O and JSON handling
- Process management (launching external programs)
- Data organization and search
- User interface design
- IT workflow automation