import psutil
import time
import json
from datetime import datetime
import platform

# Function to get CPU information
def get_cpu_info():
    """
    Get CPU usage information
    """
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_count = psutil.cpu_count(logical=True)
    cpu_freq = psutil.cpu_freq()
    
    return {
        'usage_percent': cpu_percent,
        'cores': cpu_count,
        'frequency_mhz': cpu_freq.current if cpu_freq else 'N/A'
    }

# Function to get memory information
def get_memory_info():
    """
    Get RAM usage information
    """
    memory = psutil.virtual_memory()
    
    return {
        'total_gb': round(memory.total / (1024**3), 2),
        'available_gb': round(memory.available / (1024**3), 2),
        'used_gb': round(memory.used / (1024**3), 2),
        'usage_percent': memory.percent
    }

# Function to get disk information
def get_disk_info():
    """
    Get disk usage information
    """
    disk = psutil.disk_usage('/')
    
    return {
        'total_gb': round(disk.total / (1024**3), 2),
        'used_gb': round(disk.used / (1024**3), 2),
        'free_gb': round(disk.free / (1024**3), 2),
        'usage_percent': disk.percent
    }

# Function to get network information
def get_network_info():
    """
    Get network statistics
    """
    net_io = psutil.net_io_counters()
    
    return {
        'bytes_sent_mb': round(net_io.bytes_sent / (1024**2), 2),
        'bytes_received_mb': round(net_io.bytes_recv / (1024**2), 2),
        'packets_sent': net_io.packets_sent,
        'packets_received': net_io.packets_recv
    }

# Function to display current system status
def show_system_status():
    """
    Display real-time system status
    """
    print("\n" + "="*60)
    print("SYSTEM HEALTH STATUS")
    print("="*60)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"System: {platform.system()} {platform.release()}")
    print("="*60)
    
    # CPU Info
    print("\nCPU:")
    print("-" * 60)
    cpu = get_cpu_info()
    print(f"  Usage: {cpu['usage_percent']}%")
    print(f"  Cores: {cpu['cores']}")
    print(f"  Frequency: {cpu['frequency_mhz']} MHz")
    
    # Memory Info
    print("\nMEMORY:")
    print("-" * 60)
    memory = get_memory_info()
    print(f"  Total: {memory['total_gb']} GB")
    print(f"  Used: {memory['used_gb']} GB")
    print(f"  Available: {memory['available_gb']} GB")
    print(f"  Usage: {memory['usage_percent']}%")
    
    # Disk Info
    print("\nDISK:")
    print("-" * 60)
    disk = get_disk_info()
    print(f"  Total: {disk['total_gb']} GB")
    print(f"  Used: {disk['used_gb']} GB")
    print(f"  Free: {disk['free_gb']} GB")
    print(f"  Usage: {disk['usage_percent']}%")
    
    # Network Info
    print("\nNETWORK:")
    print("-" * 60)
    network = get_network_info()
    print(f"  Sent: {network['bytes_sent_mb']} MB")
    print(f"  Received: {network['bytes_received_mb']} MB")
    print(f"  Packets Sent: {network['packets_sent']}")
    print(f"  Packets Received: {network['packets_received']}")
    
    print("\n" + "="*60)
    
# Function to monitor with alerts
def monitor_with_alerts():
    """
    Continuously monitor system and alert on thresholds
    """
    print("\n--- System Monitoring with Alerts ---")
    print("Press Ctrl+C to stop monitoring\n")
    
    # Default thresholds
    cpu_threshold = 80
    memory_threshold = 85
    disk_threshold = 90
    
    print("Default Thresholds:")
    print(f"  CPU: {cpu_threshold}%")
    print(f"  Memory: {memory_threshold}%")
    print(f"  Disk: {disk_threshold}%")
    
    customize = input("\nCustomize thresholds? (y/n): ").strip().lower()
    
    if customize == 'y':
        try:
            cpu_threshold = int(input("CPU threshold (%): "))
            memory_threshold = int(input("Memory threshold (%): "))
            disk_threshold = int(input("Disk threshold (%): "))
        except ValueError:
            print("Invalid input. Using default thresholds.")
    
    print("\nMonitoring started... (checking every 5 seconds)")
    print("-" * 60)
    
    try:
        while True:
            timestamp = datetime.now().strftime('%H:%M:%S')
            
            cpu = get_cpu_info()
            memory = get_memory_info()
            disk = get_disk_info()
            
            alerts = []
            
            # Check CPU
            if cpu['usage_percent'] > cpu_threshold:
                alerts.append(f"HIGH CPU: {cpu['usage_percent']}%")
            
            # Check Memory
            if memory['usage_percent'] > memory_threshold:
                alerts.append(f"HIGH MEMORY: {memory['usage_percent']}%")
            
            # Check Disk
            if disk['usage_percent'] > disk_threshold:
                alerts.append(f"HIGH DISK: {disk['usage_percent']}%")
            
            # Display status
            status = "OK" if not alerts else "ALERT"
            print(f"[{timestamp}] Status: {status} | CPU: {cpu['usage_percent']}% | RAM: {memory['usage_percent']}% | Disk: {disk['usage_percent']}%")
            
            # Display alerts
            if alerts:
                for alert in alerts:
                    print(f"  WARNING: {alert}")
            
            time.sleep(5)
    
    except KeyboardInterrupt:
        print("\n\nMonitoring stopped.")

# Function to view running processes
def show_processes():
    """
    Display running processes sorted by resource usage
    """
    print("\n--- Running Processes ---")
    print("\nSort by:")
    print("1. CPU Usage")
    print("2. Memory Usage")
    
    choice = input("Select (1-2): ").strip()
    
    processes = []
    
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    # Sort processes
    if choice == '1':
        processes.sort(key=lambda x: x['cpu_percent'] or 0, reverse=True)
        sort_by = "CPU"
    else:
        processes.sort(key=lambda x: x['memory_percent'] or 0, reverse=True)
        sort_by = "Memory"
    
    print(f"\nTop 20 Processes by {sort_by} Usage:")
    print("="*80)
    print(f"{'PID':<8} {'Name':<35} {'CPU %':<10} {'Memory %':<10}")
    print("-"*80)
    
    for proc in processes[:20]:
        pid = proc['pid']
        name = proc['name'][:33] if proc['name'] else 'N/A'
        cpu = f"{proc['cpu_percent']:.1f}" if proc['cpu_percent'] else '0.0'
        mem = f"{proc['memory_percent']:.1f}" if proc['memory_percent'] else '0.0'
        
        print(f"{pid:<8} {name:<35} {cpu:<10} {mem:<10}")
    
    print("="*80)

# Function to check service status
def check_services():
    """
    Check if specific services/processes are running
    """
    print("\n--- Service Status Check ---")
    print("Enter process names to check (comma-separated)")
    print("Example: chrome.exe, notepad.exe, python.exe")
    
    services_input = input("\nEnter process names: ").strip()
    
    if not services_input:
        print("No services specified.")
        return
    
    services = [s.strip() for s in services_input.split(',')]
    
    print("\n" + "="*60)
    print("SERVICE STATUS")
    print("="*60)
    
    running_processes = {proc.name().lower() for proc in psutil.process_iter(['name'])}
    
    for service in services:
        service_lower = service.lower()
        if service_lower in running_processes:
            print(f"  {service}: RUNNING")
        else:
            print(f"  {service}: NOT RUNNING")
    
    print("="*60)
    
# Function to generate health report
def generate_health_report():
    """
    Generate comprehensive system health report
    """
    print("\n" + "="*60)
    print("SYSTEM HEALTH REPORT")
    print("="*60)
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    report = {
        'timestamp': timestamp,
        'system': {
            'os': platform.system(),
            'release': platform.release(),
            'machine': platform.machine()
        },
        'cpu': get_cpu_info(),
        'memory': get_memory_info(),
        'disk': get_disk_info(),
        'network': get_network_info()
    }
    
    # Display report
    print(f"\nTimestamp: {timestamp}")
    print(f"System: {report['system']['os']} {report['system']['release']}")
    print(f"Architecture: {report['system']['machine']}")
    
    print("\nCPU Status:")
    print(f"  Usage: {report['cpu']['usage_percent']}%")
    print(f"  Cores: {report['cpu']['cores']}")
    
    print("\nMemory Status:")
    print(f"  Total: {report['memory']['total_gb']} GB")
    print(f"  Used: {report['memory']['used_gb']} GB ({report['memory']['usage_percent']}%)")
    print(f"  Available: {report['memory']['available_gb']} GB")
    
    print("\nDisk Status:")
    print(f"  Total: {report['disk']['total_gb']} GB")
    print(f"  Used: {report['disk']['used_gb']} GB ({report['disk']['usage_percent']}%)")
    print(f"  Free: {report['disk']['free_gb']} GB")
    
    print("\nNetwork Statistics:")
    print(f"  Sent: {report['network']['bytes_sent_mb']} MB")
    print(f"  Received: {report['network']['bytes_received_mb']} MB")
    
    # Health assessment
    print("\nHealth Assessment:")
    issues = []
    
    if report['cpu']['usage_percent'] > 80:
        issues.append("High CPU usage detected")
    if report['memory']['usage_percent'] > 85:
        issues.append("High memory usage detected")
    if report['disk']['usage_percent'] > 90:
        issues.append("Low disk space detected")
    
    if not issues:
        print("  Status: HEALTHY")
    else:
        print("  Status: ATTENTION NEEDED")
        for issue in issues:
            print(f"    - {issue}")
    
    print("="*60)
    
    # Save option
    save = input("\nSave report to file? (y/n): ").strip().lower()
    
    if save == 'y':
        filename = f"system_health_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(report, f, indent=4)
        print(f"\nReport saved to: {filename}")
    
    return report

# Function to log system metrics
def log_system_metrics():
    """
    Log current system metrics to file
    """
    log_file = "system_metrics_log.json"
    
    metric = {
        'timestamp': datetime.now().isoformat(),
        'cpu_percent': get_cpu_info()['usage_percent'],
        'memory_percent': get_memory_info()['usage_percent'],
        'disk_percent': get_disk_info()['usage_percent']
    }
    
    # Load existing logs
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            logs = json.load(f)
    else:
        logs = []
    
    logs.append(metric)
    
    # Keep only last 100 entries
    if len(logs) > 100:
        logs = logs[-100:]
    
    with open(log_file, 'w') as f:
        json.dump(logs, f, indent=4)
    
    print(f"\nMetrics logged successfully at {metric['timestamp']}")

# Main menu
def show_menu():
    print("\n" + "="*60)
    print("  SYSTEM HEALTH MONITORING DASHBOARD")
    print("="*60)
    print("1. View Current System Status")
    print("2. Monitor with Alerts (Continuous)")
    print("3. View Running Processes")
    print("4. Generate Health Report")
    print("5. Check Service Status")
    print("6. Log Current Metrics")
    print("7. Exit")
    print("-"*60)

# Main program
def main():
    # Check if psutil is installed
    try:
        import psutil
    except ImportError:
        print("\nERROR: psutil library not found!")
        print("Please install it using: pip install psutil")
        return
    
    import os
    
    while True:
        show_menu()
        choice = input("\nSelect an option (1-7): ").strip()
        
        if choice == '1':
            show_system_status()
        
        elif choice == '2':
            monitor_with_alerts()
        
        elif choice == '3':
            show_processes()
        
        elif choice == '4':
            generate_health_report()
        
        elif choice == '5':
            check_services()
        
        elif choice == '6':
            log_system_metrics()
        
        elif choice == '7':
            print("\nThank you for using System Health Monitoring Dashboard!")
            print("Exiting...\n")
            break
        
        else:
            print("\nInvalid option. Please select 1-7.")
        
        if choice != '7':
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()