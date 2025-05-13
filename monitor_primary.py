#!/usr/bin/env python3
import subprocess
import sys
from rich import console

console = console.Console()

def get_current_config():
    current = subprocess.check_output("xrandr", shell=True).decode()
    return current

def set_primary(monitor):
    current = get_current_config()
    
    # Check if the specified monitor is connected
    if f"{monitor} connected" not in current:
        console.log(f"Monitor {monitor} no está conectado")
        return f"Monitor {monitor} no está conectado"
    
    # Get list of connected monitors
    connected_monitors = []
    for line in current.splitlines():
        if " connected" in line:
            mon = line.split(" ")[0]
            connected_monitors.append(mon)
    
    # Set the specified monitor as primary
    command = f"xrandr --output {monitor} --auto --primary"
    
    # Configure other connected monitors to be to the right of the primary
    other_monitors = [m for m in connected_monitors if m != monitor]
    for other in other_monitors:
        command += f" --output {other} --auto --right-of {monitor}"
    
    console.log(f"Setting {monitor} as primary")
    console.log(f"Running command: {command}")
    subprocess.Popen(command, shell=True)
    return command

def set_hdmi_primary():
    return set_primary("HDMI-1")

def set_edp_primary():
    return set_primary("eDP-1")

if __name__ == "__main__":
    # If argument is provided, use that as the monitor to set as primary
    if len(sys.argv) > 1:
        set_primary(sys.argv[1])
    else:
        # Default to setting HDMI as primary if no argument provided
        set_hdmi_primary() 