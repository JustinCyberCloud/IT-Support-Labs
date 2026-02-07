# Lab 5: System Health Monitoring Dashboard

## Description
A Python-based system monitoring tool that tracks CPU, memory, disk usage, and running processes. Provides real-time health checks and alerts when thresholds are exceeded.

## Features
- **Real-time System Monitoring**: CPU, RAM, disk space, network stats
- **Process Management**: View running processes and resource usage
- **Threshold Alerts**: Get warnings when resources exceed limits
- **Health Reports**: Generate system health snapshots
- **Historical Logging**: Track system performance over time
- **Service Status Check**: Monitor critical services/processes
- **Export Reports**: Save monitoring data to JSON/CSV

## Requirements
- Python 3.7 or higher
- psutil library (install with: `pip install psutil`)

## Installation

1. Install required library:
pip install psutil


2. Run the program:
python system_monitor.py


## Usage Examples

### View Current System Status
- Select option 1
- See real-time CPU, RAM, disk, and network usage

### Monitor with Alerts
- Select option 2
- Set custom thresholds (e.g., alert if CPU > 80%)
- Get warnings when limits are exceeded

### View Running Processes
- Select option 3
- See all processes sorted by CPU or memory usage
- Identify resource-heavy applications

### Generate Health Report
- Select option 4
- Get comprehensive system snapshot
- Export to file for documentation

### Check Service Status
- Select option 5
- Monitor if critical services are running
- Useful for server monitoring

## Default Alert Thresholds
- CPU Usage: 80%
- Memory Usage: 85%
- Disk Usage: 90%
- (Customizable in the script)

## Common Use Cases
- Proactive server monitoring
- Troubleshooting performance issues
- Identifying resource bottlenecks
- Documenting system health for tickets
- Capacity planning
- Detecting runaway processes

## Skills Demonstrated
- System administration concepts
- Performance monitoring and analysis
- Python scripting with external libraries
- Real-time data collection
- Alert/threshold management
- Process management
- Report generation
