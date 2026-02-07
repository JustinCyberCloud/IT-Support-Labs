import json
import os
import subprocess
from datetime import datetime
import platform

# Database file for connections
CONNECTIONS_FILE = "rdp_connections.json"
HISTORY_FILE = "connection_history.json"

# Function to load connections
def load_connections():
    """Load saved RDP connections from file"""
    if os.path.exists(CONNECTIONS_FILE):
        with open(CONNECTIONS_FILE, 'r') as f:
            return json.load(f)
    return []

# Function to save connections
def save_connections(connections):
    """Save RDP connections to file"""
    with open(CONNECTIONS_FILE, 'w') as f:
        json.dump(connections, f, indent=4)
    print("\nConnections saved successfully!")

# Function to load connection history
def load_history():
    """Load connection history from file"""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    return []

# Function to save connection history
def save_history(history):
    """Save connection history to file"""
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=4)

# Function to log connection
def log_connection(connection_name, hostname):
    """Log a connection to history"""
    history = load_history()
    
    log_entry = {
        'connection_name': connection_name,
        'hostname': hostname,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    history.append(log_entry)
    
    # Keep only last 50 entries
    if len(history) > 50:
        history = history[-50:]
    
    save_history(history)

# Function to add a new connection
def add_connection():
    """Add a new RDP connection profile"""
    print("\n--- Add New RDP Connection ---")
    
    display_name = input("Display Name (e.g., Production Server): ").strip()
    hostname = input("Hostname or IP Address: ").strip()
    username = input("Username: ").strip()
    port = input("Port (default 3389): ").strip() or "3389"
    tags = input("Tags (comma-separated, e.g., production,web): ").strip()
    notes = input("Notes (optional): ").strip()
    
    if not display_name or not hostname:
        print("\nERROR: Display name and hostname are required!")
        return
    
    connections = load_connections()
    
    # Check for duplicate
    if any(conn['display_name'] == display_name for conn in connections):
        print(f"\nERROR: Connection '{display_name}' already exists!")
        return
    
    new_connection = {
        'display_name': display_name,
        'hostname': hostname,
        'username': username,
        'port': port,
        'tags': [tag.strip() for tag in tags.split(',') if tag.strip()],
        'notes': notes,
        'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    connections.append(new_connection)
    save_connections(connections)
    
    print(f"\nSUCCESS: Connection '{display_name}' added!")
    print(f"Hostname: {hostname}")
    print(f"Username: {username}")
    print(f"Port: {port}")

# Function to connect via RDP
def connect_rdp(connection):
    """Launch RDP connection"""
    print(f"\nConnecting to {connection['display_name']}...")
    print(f"Hostname: {connection['hostname']}")
    print(f"Username: {connection['username']}")
    
    # Build mstsc command
    if platform.system() != 'Windows':
        print("\nERROR: RDP is only available on Windows systems")
        return
    
    # Create RDP command
    rdp_command = f"mstsc /v:{connection['hostname']}:{connection['port']}"
    
    try:
        # Launch RDP
        subprocess.Popen(rdp_command, shell=True)
        
        # Log the connection
        log_connection(connection['display_name'], connection['hostname'])
        
        print("\nRDP session launched!")
        print("Note: You may need to enter your password in the RDP window")
    except Exception as e:
        print(f"\nERROR: Failed to launch RDP - {str(e)}")
        
# Function to quick connect
def quick_connect():
    """Select and connect to a saved connection"""
    connections = load_connections()
    
    if not connections:
        print("\nNo saved connections found. Add a connection first!")
        return
    
    print("\n--- Quick Connect ---")
    print("\nSaved Connections:")
    print("="*80)
    
    for idx, conn in enumerate(connections, 1):
        tags_str = ', '.join(conn['tags']) if conn['tags'] else 'None'
        print(f"{idx}. {conn['display_name']}")
        print(f"   Host: {conn['hostname']} | User: {conn['username']} | Tags: {tags_str}")
        print("-"*80)
    
    try:
        choice = int(input("\nSelect connection number (0 to cancel): "))
        
        if choice == 0:
            return
        
        if 1 <= choice <= len(connections):
            connect_rdp(connections[choice - 1])
        else:
            print("\nInvalid selection!")
    except ValueError:
        print("\nInvalid input!")

# Function to view all connections
def view_connections():
    """Display all saved connections"""
    connections = load_connections()
    
    if not connections:
        print("\nNo saved connections found.")
        return
    
    print("\n" + "="*80)
    print("SAVED RDP CONNECTIONS")
    print("="*80)
    print(f"Total Connections: {len(connections)}\n")
    
    for idx, conn in enumerate(connections, 1):
        print(f"{idx}. {conn['display_name']}")
        print(f"   Hostname: {conn['hostname']}")
        print(f"   Username: {conn['username']}")
        print(f"   Port: {conn['port']}")
        print(f"   Tags: {', '.join(conn['tags']) if conn['tags'] else 'None'}")
        if conn['notes']:
            print(f"   Notes: {conn['notes']}")
        print(f"   Created: {conn['created']}")
        print("-"*80)
    
    print("="*80)

# Function to search connections
def search_connections():
    """Search connections by name, hostname, or tags"""
    connections = load_connections()
    
    if not connections:
        print("\nNo saved connections found.")
        return
    
    print("\n--- Search Connections ---")
    search_term = input("Enter search term (name, IP, or tag): ").strip().lower()
    
    if not search_term:
        print("\nNo search term entered.")
        return
    
    results = []
    
    for conn in connections:
        # Search in display name, hostname, and tags
        if (search_term in conn['display_name'].lower() or
            search_term in conn['hostname'].lower() or
            any(search_term in tag.lower() for tag in conn['tags'])):
            results.append(conn)
    
    if not results:
        print(f"\nNo connections found matching '{search_term}'")
        return
    
    print(f"\nFound {len(results)} connection(s):")
    print("="*80)
    
    for idx, conn in enumerate(results, 1):
        print(f"{idx}. {conn['display_name']}")
        print(f"   Hostname: {conn['hostname']}")
        print(f"   Username: {conn['username']}")
        print(f"   Tags: {', '.join(conn['tags']) if conn['tags'] else 'None'}")
        print("-"*80)
    
    # Option to connect
    try:
        connect_choice = input("\nConnect to a result? Enter number (0 to cancel): ")
        choice = int(connect_choice)
        
        if choice > 0 and choice <= len(results):
            connect_rdp(results[choice - 1])
    except ValueError:
        pass

# Function to delete a connection
def delete_connection():
    """Delete a saved connection"""
    connections = load_connections()
    
    if not connections:
        print("\nNo saved connections found.")
        return
    
    print("\n--- Delete Connection ---")
    print("\nSaved Connections:")
    
    for idx, conn in enumerate(connections, 1):
        print(f"{idx}. {conn['display_name']} ({conn['hostname']})")
    
    try:
        choice = int(input("\nSelect connection to delete (0 to cancel): "))
        
        if choice == 0:
            return
        
        if 1 <= choice <= len(connections):
            deleted = connections.pop(choice - 1)
            save_connections(connections)
            print(f"\nSUCCESS: Connection '{deleted['display_name']}' deleted!")
        else:
            print("\nInvalid selection!")
    except ValueError:
        print("\nInvalid input!")

# Function to view connection history
def view_history():
    """Display connection history"""
    history = load_history()
    
    if not history:
        print("\nNo connection history found.")
        return
    
    print("\n" + "="*80)
    print("CONNECTION HISTORY")
    print("="*80)
    print(f"Total Connections: {len(history)}\n")
    
    # Show last 20 entries
    recent = history[-20:]
    recent.reverse()
    
    for entry in recent:
        print(f"[{entry['timestamp']}] {entry['connection_name']} ({entry['hostname']})")
    
    print("="*80)
    
# Function to export connections
def export_connections():
    """Export connections to a backup file"""
    connections = load_connections()
    
    if not connections:
        print("\nNo connections to export.")
        return
    
    filename = f"rdp_connections_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    try:
        with open(filename, 'w') as f:
            json.dump(connections, f, indent=4)
        
        print(f"\nSUCCESS: Connections exported to {filename}")
        print(f"Total connections exported: {len(connections)}")
    except Exception as e:
        print(f"\nERROR: Failed to export - {str(e)}")

# Function to import connections
def import_connections():
    """Import connections from a backup file"""
    print("\n--- Import Connections ---")
    filename = input("Enter backup file name: ").strip()
    
    if not os.path.exists(filename):
        print(f"\nERROR: File '{filename}' not found!")
        return
    
    try:
        with open(filename, 'r') as f:
            imported = json.load(f)
        
        if not isinstance(imported, list):
            print("\nERROR: Invalid backup file format!")
            return
        
        connections = load_connections()
        
        added = 0
        skipped = 0
        
        for conn in imported:
            # Check if connection already exists
            if any(c['display_name'] == conn['display_name'] for c in connections):
                print(f"SKIPPED: {conn['display_name']} (already exists)")
                skipped += 1
            else:
                connections.append(conn)
                print(f"ADDED: {conn['display_name']}")
                added += 1
        
        save_connections(connections)
        
        print(f"\nImport complete!")
        print(f"Added: {added}")
        print(f"Skipped: {skipped}")
    
    except Exception as e:
        print(f"\nERROR: Failed to import - {str(e)}")

# Function to test connection
def test_connection():
    """Test if a server is reachable"""
    connections = load_connections()
    
    if not connections:
        print("\nNo saved connections found.")
        return
    
    print("\n--- Test Connection ---")
    print("\nSaved Connections:")
    
    for idx, conn in enumerate(connections, 1):
        print(f"{idx}. {conn['display_name']} ({conn['hostname']})")
    
    try:
        choice = int(input("\nSelect connection to test (0 to cancel): "))
        
        if choice == 0:
            return
        
        if 1 <= choice <= len(connections):
            conn = connections[choice - 1]
            print(f"\nTesting connection to {conn['hostname']}...")
            
            # Ping test
            param = '-n' if platform.system().lower() == 'windows' else '-c'
            command = ['ping', param, '2', conn['hostname']]
            
            result = subprocess.run(command, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                print(f"SUCCESS: {conn['hostname']} is reachable!")
            else:
                print(f"FAILED: {conn['hostname']} is not reachable")
        else:
            print("\nInvalid selection!")
    except ValueError:
        print("\nInvalid input!")
    except subprocess.TimeoutExpired:
        print("\nTIMEOUT: Connection test timed out")
    except Exception as e:
        print(f"\nERROR: {str(e)}")

# Main menu
def show_menu():
    print("\n" + "="*60)
    print("  REMOTE DESKTOP CONNECTION MANAGER")
    print("="*60)
    print("1. Add New Connection")
    print("2. Quick Connect")
    print("3. View All Connections")
    print("4. Search Connections")
    print("5. View Connection History")
    print("6. Delete Connection")
    print("7. Test Connection")
    print("8. Export Connections")
    print("9. Import Connections")
    print("10. Exit")
    print("-"*60)

# Main program
def main():
    # Check if running on Windows
    if platform.system() != 'Windows':
        print("\nWARNING: This tool is designed for Windows systems.")
        print("RDP functionality may not work on other operating systems.\n")
    
    while True:
        show_menu()
        choice = input("\nSelect an option (1-10): ").strip()
        
        if choice == '1':
            add_connection()
        
        elif choice == '2':
            quick_connect()
        
        elif choice == '3':
            view_connections()
        
        elif choice == '4':
            search_connections()
        
        elif choice == '5':
            view_history()
        
        elif choice == '6':
            delete_connection()
        
        elif choice == '7':
            test_connection()
        
        elif choice == '8':
            export_connections()
        
        elif choice == '9':
            import_connections()
        
        elif choice == '10':
            print("\nThank you for using RDP Connection Manager!")
            print("Exiting...\n")
            break
        
        else:
            print("\nInvalid option. Please select 1-10.")
        
        if choice != '10':
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()