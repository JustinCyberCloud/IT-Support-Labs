# Lab 3: Network Troubleshooting Toolkit

## Description
A Python-based network diagnostics toolkit for IT support professionals. Perform common network troubleshooting tasks from a single menu-driven interface.

## Features
- **Ping Test**: Check connectivity to single or multiple hosts
- **Traceroute**: Trace network path to destination
- **DNS Lookup**: Resolve hostnames to IP addresses and vice versa
- **Port Scanner**: Check if specific ports are open on a host
- **Network Report**: Generate comprehensive diagnostics report
- **Batch Testing**: Test multiple hosts from a file
- **Export Results**: Save results to text or JSON format

## Requirements
- Python 3.7 or higher
- Administrator/root privileges (for some features)

## How to Run

1. Make sure Python 3 is installed
2. Run the program:
python network_toolkit.py


## Usage Examples

### Ping a Host
- Select option 1
- Enter hostname or IP address (e.g., google.com or 8.8.8.8)
- View response time and packet loss

### Traceroute
- Select option 2
- Enter destination host
- See all hops between you and the destination

### DNS Lookup
- Select option 3
- Enter domain name or IP address
- Get DNS resolution information

### Port Scan
- Select option 4
- Enter target host
- Enter port or port range (e.g., 80 or 20-100)
- See which ports are open

### Generate Network Report
- Select option 5
- Enter target host
- Get comprehensive report with all diagnostics

## Common Use Cases
- Troubleshooting connectivity issues
- Verifying DNS configuration
- Checking if services are running (port checks)
- Documenting network issues for tickets
- Baseline network performance testing

## Skills Demonstrated
- Network fundamentals (TCP/IP, DNS, routing)
- Python networking libraries
- Command-line tool development
- Diagnostic methodology
- Report generation and documentation
