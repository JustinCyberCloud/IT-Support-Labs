import socket
import subprocess
import platform
import sys
import json
from datetime import datetime
import re

# Function to ping a host
def ping_host(host, count=4):
    """
    Ping a host and return results
    """
    print(f"\n--- Pinging {host} ---")
    
    # Determine ping command based on OS
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, str(count), host]
    
    try:
        output = subprocess.run(command, capture_output=True, text=True, timeout=30)
        
        if output.returncode == 0:
            print(f"SUCCESS: {host} is reachable")
            print(output.stdout)
            
            # Parse statistics
            if platform.system().lower() == 'windows':
                # Windows format
                loss_match = re.search(r'(\d+)% loss', output.stdout)
                time_match = re.search(r'Average = (\d+)ms', output.stdout)
            else:
                # Linux/Mac format
                loss_match = re.search(r'(\d+)% packet loss', output.stdout)
                time_match = re.search(r'avg = ([\d.]+)', output.stdout)
            
            packet_loss = loss_match.group(1) if loss_match else "Unknown"
            avg_time = time_match.group(1) if time_match else "Unknown"
            
            return {
                'host': host,
                'status': 'reachable',
                'packet_loss': packet_loss + '%',
                'avg_response_time': avg_time + 'ms',
                'output': output.stdout
            }
        else:
            print(f"FAILED: {host} is unreachable")
            print(output.stdout)
            return {
                'host': host,
                'status': 'unreachable',
                'output': output.stdout
            }
    
    except subprocess.TimeoutExpired:
        print(f"TIMEOUT: {host} did not respond in time")
        return {
            'host': host,
            'status': 'timeout'
        }
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return {
            'host': host,
            'status': 'error',
            'error': str(e)
        }

# Function to perform traceroute
def traceroute(host):
    """
    Perform traceroute to a host
    """
    print(f"\n--- Traceroute to {host} ---")
    
    # Determine traceroute command based on OS
    if platform.system().lower() == 'windows':
        command = ['tracert', host]
    else:
        command = ['traceroute', host]
    
    try:
        print("This may take a moment...\n")
        output = subprocess.run(command, capture_output=True, text=True, timeout=60)
        print(output.stdout)
        
        return {
            'host': host,
            'output': output.stdout
        }
    
    except subprocess.TimeoutExpired:
        print("TIMEOUT: Traceroute took too long")
        return {
            'host': host,
            'status': 'timeout'
        }
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return {
            'host': host,
            'status': 'error',
            'error': str(e)
        }
    
# Function to perform DNS lookup
def dns_lookup(target):
    """
    Perform DNS lookup (forward or reverse)
    """
    print(f"\n--- DNS Lookup for {target} ---")
    
    try:
        # Try forward lookup (hostname to IP)
        try:
            ip_address = socket.gethostbyname(target)
            hostname = socket.getfqdn(target)
            print(f"Hostname: {hostname}")
            print(f"IP Address: {ip_address}")
            
            # Try reverse lookup
            try:
                reverse_name = socket.gethostbyaddr(ip_address)
                print(f"Reverse DNS: {reverse_name}")
            except:
                print("Reverse DNS: Not available")
            
            return {
                'target': target,
                'hostname': hostname,
                'ip_address': ip_address,
                'status': 'success'
            }
        
        except socket.gaierror:
            # Maybe it's an IP address, try reverse lookup
            try:
                hostname = socket.gethostbyaddr(target)
                print(f"IP Address: {target}")
                print(f"Hostname: {hostname}")
                print(f"Aliases: {', '.join(hostname) if hostname else 'None'}")
                
                return {
                    'target': target,
                    'hostname': hostname,
                    'ip_address': target,
                    'status': 'success'
                }
            except:
                print(f"FAILED: Could not resolve {target}")
                return {
                    'target': target,
                    'status': 'failed'
                }
    
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return {
            'target': target,
            'status': 'error',
            'error': str(e)
        }

# Function to scan a port
def scan_port(host, port, timeout=1):
    """
    Check if a specific port is open on a host
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False

# Function to scan multiple ports
def port_scanner(host, port_range):
    """
    Scan a range of ports on a host
    """
    print(f"\n--- Port Scan: {host} ---")
    
    # Parse port range
    if '-' in port_range:
        start_port, end_port = map(int, port_range.split('-'))
    else:
        start_port = end_port = int(port_range)
    
    print(f"Scanning ports {start_port} to {end_port}...")
    print("This may take a moment...\n")
    
    open_ports = []
    common_ports = {
        20: 'FTP Data',
        21: 'FTP Control',
        22: 'SSH',
        23: 'Telnet',
        25: 'SMTP',
        53: 'DNS',
        80: 'HTTP',
        110: 'POP3',
        143: 'IMAP',
        443: 'HTTPS',
        445: 'SMB',
        3306: 'MySQL',
        3389: 'RDP',
        5432: 'PostgreSQL',
        8080: 'HTTP-Alt'
    }
    
    for port in range(start_port, end_port + 1):
        if scan_port(host, port):
            service = common_ports.get(port, 'Unknown')
            print(f"Port {port} is OPEN - {service}")
            open_ports.append({'port': port, 'service': service})
        
        # Show progress for large scans
        if (port - start_port + 1) % 20 == 0:
            print(f"Scanned {port - start_port + 1} ports...")
    
    if not open_ports:
        print("No open ports found in the specified range.")
    else:
        print(f"\nTotal open ports found: {len(open_ports)}")
    
    return {
        'host': host,
        'port_range': port_range,
        'open_ports': open_ports
    }

# Function to generate comprehensive network report
def generate_network_report(host):
    """
    Generate a comprehensive network diagnostics report
    """
    print(f"\n{'='*60}")
    print(f"NETWORK DIAGNOSTICS REPORT")
    print(f"{'='*60}")
    print(f"Target: {host}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")
    
    report = {
        'target': host,
        'timestamp': datetime.now().isoformat(),
        'tests': {}
    }
    
    # DNS Lookup
    print("1. DNS LOOKUP")
    print("-" * 60)
    dns_result = dns_lookup(host)
    report['tests']['dns'] = dns_result
    
    # Ping Test
    print("\n2. PING TEST")
    print("-" * 60)
    ping_result = ping_host(host, count=4)
    report['tests']['ping'] = ping_result
    
    # Common Port Scan
    print("\n3. COMMON PORTS SCAN")
    print("-" * 60)
    common_ports = "80,443,22,21,25,3389"
    ports_to_scan = [80, 443, 22, 21, 25, 3389]
    
    open_ports = []
    port_names = {
        80: 'HTTP',
        443: 'HTTPS',
        22: 'SSH',
        21: 'FTP',
        25: 'SMTP',
        3389: 'RDP'
    }
    
    for port in ports_to_scan:
        if scan_port(host, port):
            service = port_names.get(port, 'Unknown')
            print(f"Port {port} ({service}): OPEN")
            open_ports.append({'port': port, 'service': service})
        else:
            print(f"Port {port} ({port_names.get(port, 'Unknown')}): CLOSED")
    
    report['tests']['ports'] = {'open_ports': open_ports}
    
    print(f"\n{'='*60}")
    print("REPORT COMPLETE")
    print(f"{'='*60}\n")
    
    # Ask to save report
    save = input("Save report to file? (y/n): ").strip().lower()
    if save == 'y':
        filename = f"network_report_{host}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(report, f, indent=4)
        print(f"\nReport saved to: {filename}")
    
    return report

# Main menu
def show_menu():
    print("\n" + "="*50)
    print("  NETWORK TROUBLESHOOTING TOOLKIT")
    print("="*50)
    print("1. Ping Host")
    print("2. Traceroute")
    print("3. DNS Lookup")
    print("4. Port Scanner")
    print("5. Generate Network Report")
    print("6. Batch Ping (Multiple Hosts)")
    print("7. Exit")
    print("-"*50)

# Batch ping function
def batch_ping():
    """
    Ping multiple hosts
    """
    print("\n--- Batch Ping ---")
    print("Enter hostnames/IPs separated by commas")
    print("Example: google.com, 8.8.8.8, github.com")
    
    hosts_input = input("\nEnter hosts: ").strip()
    hosts = [h.strip() for h in hosts_input.split(',')]
    
    results = []
    print(f"\nPinging {len(hosts)} hosts...\n")
    
    for host in hosts:
        result = ping_host(host, count=2)
        results.append(result)
        print()
    
    # Summary
    print("\n" + "="*50)
    print("BATCH PING SUMMARY")
    print("="*50)
    reachable = sum(1 for r in results if r.get('status') == 'reachable')
    print(f"Total hosts: {len(hosts)}")
    print(f"Reachable: {reachable}")
    print(f"Unreachable: {len(hosts) - reachable}")
    print("="*50)

# Main program
def main():
    while True:
        show_menu()
        choice = input("\nSelect an option (1-7): ").strip()
        
        if choice == '1':
            host = input("\nEnter hostname or IP address: ").strip()
            if host:
                ping_host(host)
            else:
                print("Invalid input")
        
        elif choice == '2':
            host = input("\nEnter hostname or IP address: ").strip()
            if host:
                traceroute(host)
            else:
                print("Invalid input")
        
        elif choice == '3':
            target = input("\nEnter hostname or IP address: ").strip()
            if target:
                dns_lookup(target)
            else:
                print("Invalid input")
        
        elif choice == '4':
            host = input("\nEnter hostname or IP address: ").strip()
            port_range = input("Enter port or range (e.g., 80 or 20-100): ").strip()
            if host and port_range:
                port_scanner(host, port_range)
            else:
                print("Invalid input")
        
        elif choice == '5':
            host = input("\nEnter hostname or IP address: ").strip()
            if host:
                generate_network_report(host)
            else:
                print("Invalid input")
        
        elif choice == '6':
            batch_ping()
        
        elif choice == '7':
            print("\nThank you for using Network Troubleshooting Toolkit!")
            print("Exiting...\n")
            break
        
        else:
            print("\nInvalid option. Please select 1-7.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()