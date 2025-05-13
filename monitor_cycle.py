#!/usr/bin/env python3
import subprocess
import sys
from rich import console

console = console.Console()

def get_current_config():
    current = subprocess.check_output("xrandr", shell=True).decode()
    # print(current)
    return current

def set_actual_display(actual: str):
    if actual == "HDMI-1":
        with open("actual.txt", "w") as f:
            f.write("HDMI-1")
    else:
        with open("actual.txt", "w") as f:
            f.write("eDP-1")

def get_actual_display():
    with open("actual.txt", "r") as f:
        return f.read()
    
def set_wallpaper():
    subprocess.Popen(['sh', './wallpaper.sh'])

def set_two_displays(display_one: str, display_two: str, primary: int):
    if primary == 1:
        subprocess.Popen(['xrandr', '--output', display_one, '--auto', '--primary', '--output', display_two, '--auto', '--right-of', display_one])
    else:
        subprocess.Popen(['xrandr', '--output', display_one, '--auto', '--output', display_two, '--auto', '--primary', '--right-of', display_one])
    subprocess.Popen(['dunstify', '-u', 'normal', 'Display Configuration', f'Using both displays with {display_one} as primary'])

def set_one_display(display_one: str, display_two: str):
    subprocess.Popen(['xrandr', '--output', display_one, '--auto', '--output', display_two, '--off'])
    subprocess.Popen(['dunstify', '-u', 'normal', 'Display Configuration', f'Using {display_one} as primary'])

def cycle_config():
    current = get_current_config()
    
    # Determine current state and switch to next
    if "HDMI-1 connected" in current and "eDP-1 connected" in current:
        try:
            with open("actual.txt", "r") as f:
                display = f.read()
        except FileNotFoundError:
            display = "HDMI-1"
        if display == "HDMI-1":
            console.log("Both displays connected")
            set_two_displays("eDP-1", "HDMI-1", 1)
            set_actual_display("eDP-1")
            set_wallpaper()
        else:
            console.log("Both displays connected")
            set_two_displays("eDP-1", "HDMI-1", 0)
            set_actual_display("HDMI-1")
            set_wallpaper()

    elif "HDMI-1 connected" in current:
        # Only HDMI connected
        console.log("Using HDMI-1 only")
        set_actual_display("HDMI-1")
        set_wallpaper()
        set_one_display("HDMI-1", "eDP-1")

    else:
        # Only laptop display
        console.log("Using laptop display only")
        set_actual_display("eDP-1")
        set_wallpaper()
        set_one_display("eDP-1", "HDMI-1")

if __name__ == "__main__":
    cycle_config() 