#!/usr/bin/env python3
import subprocess
import sys
from rich import console
from dotenv import load_dotenv
import os

load_dotenv()

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




def set_two_displays(
    display_one: str, display_two: str, primary: int, mode_one: str, mode_two: str, rate_one: str, rate_two: str
):
    if primary == 1:
        subprocess.Popen(
            [
                "xrandr",
                "--output",
                display_one,
                "--mode",
                mode_one,
                "--rate",
                rate_one,
                "--auto",
                "--primary",
                "--output",
                display_two,
                "--mode",
                mode_two,
                "--rate",
                rate_two,
                "--right-of",
                display_one,
            ]
        )
        subprocess.Popen(
        [
            "dunstify",
            "-u",
            "normal",
            "Display Configuration",
            f"Using both displays with {display_one} as primary",
        ]
    )
    else:
        subprocess.Popen(
            [
                "xrandr",
                "--output",
                display_one,
                "--mode",
                mode_one,
                "--rate",
                rate_one,
                "--auto",
                "--output",
                display_two,
                "--mode",
                mode_two,
                "--rate",
                rate_two,
                "--primary",
                "--right-of",
                display_one,
            ]
        )
        subprocess.Popen(
        [
            "dunstify",
            "-u",
            "normal",
            "Display Configuration",
            f"Using both displays with {display_two} as primary",
        ]
    )



def set_one_display(display_one: str, display_two: str, mode_one: str, mode_two: str, rate_one: str, rate_two: str):
    subprocess.Popen(
        ["xrandr", "--output", display_one, "--mode", mode_one, "--rate", rate_one, "--auto", "--output", display_two, "--off"]
    )
    subprocess.Popen(
        [
            "dunstify",
            "-u",
            "normal",
            "Display Configuration",
            f"Using {display_one} as primary",
        ]
    )


def cycle_config(display: str):
    current = get_current_config()
    mode_one = os.getenv("MODE_ONE")
    mode_two = os.getenv("MODE_TWO")
    rate_one = os.getenv("RATE_ONE")
    rate_two = os.getenv("RATE_TWO")
    # mode_one = "1600x900"
    # mode_two = "2560x1440"
    # Determine current state and switch to next
    if display == "first_time":
        if "HDMI-1 connected" in current and "eDP-1 connected" in current:
            set_two_displays("eDP-1", "HDMI-1", 1, mode_one, mode_two, rate_one, rate_two)
            set_actual_display("eDP-1")
            return True
    elif "HDMI-1 connected" in current and "eDP-1 connected" in current:
        try:
            with open("actual.txt", "r") as f:
                display = f.read()
        except FileNotFoundError:
            display = "HDMI-1"
        if display == "HDMI-1":
            console.log("Both displays connected")
            set_two_displays("eDP-1", "HDMI-1", 1, mode_one, mode_two, rate_one, rate_two)
            set_actual_display("eDP-1")
        else:
            console.log("Both displays connected")
            set_two_displays("eDP-1", "HDMI-1", 0, mode_one, mode_two, rate_one, rate_two)
            set_actual_display("HDMI-1")

    elif "HDMI-1 connected" in current:
        # Only HDMI connected
        console.log("Using HDMI-1 only")
        set_actual_display("HDMI-1")
        set_one_display("HDMI-1", "eDP-1", mode_two, mode_one, rate_two, rate_one)

    else:
        # Only laptop display
        console.log("Using laptop display only")
        set_actual_display("eDP-1")
        set_one_display("eDP-1", "HDMI-1", mode_one, mode_two, rate_one, rate_two)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        cycle_config(sys.argv[1])
    else:
        cycle_config("")
