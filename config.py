# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person/dev/nvme0n1p3
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile import bar, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
import os
import subprocess
from libqtile import hook


# Add this function for monitor cycling
def cycle_monitors():
    script_path = os.path.expanduser("~/.config/qtile/monitor_cycle.py")
    subprocess.call([script_path])
    # refresh_wallpapers()

def refresh_monitors():
    subprocess.Popen(["xrandr", "--output", "HDMI-1", "--off", "--output", "eDP-1", "--auto"])
    # refresh_wallpapers()

def refresh_wallpapers():
    dir = "/home/osmar/Pictures"
    import random
    wallpapers = [os.path.join(dir, f) for f in os.listdir(dir) if f.endswith(('.jpg', '.png', '.jpeg'))]
    wallpaper1 = random.choice(wallpapers)
    wallpaper2 = random.choice(wallpapers)
    while wallpaper2 == wallpaper1:  # Ensure different wallpapers
        wallpaper2 = random.choice(wallpapers)
    subprocess.Popen(
        [
            "dunstify",
            "-u",
            "normal",
            "Wallpaper Configuration",
            f"Using {wallpaper1} and {wallpaper2}",
        ]
    )
    subprocess.Popen(["feh", "--bg-scale", wallpaper1, "--bg-scale", wallpaper2, "&"])

def open_app(app):
    subprocess.Popen([app])

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser("~/.config/qtile/autostart.sh")
    subprocess.Popen([home])


@hook.subscribe.client_new
def client_new(client):
    if client.window.get_class() in ["steam", "discord", "dota2"]:
        client.togroup("GAME")

    elif client.window.get_name() in ["whatsapp", "teams"]:
        client.togroup("CHAT")

    elif client.window.get_name() in ["gmail", "outlook"]:
        client.togroup("MAIL")

    elif client.window.get_class() in ["vscode", "cursor", "windsurf"]:
        client.togroup("IDE")

    elif client.window.get_class() in ["brave", "firefox"]:
        client.togroup("WEB")

    elif client.window.get_name() in ["webui", "openai", "claude", "gemini", "gpt"]:
        client.togroup("AI")

    elif client.window.get_class() in [
        "blender",
        "krita",
        "gimp",
        "inkscape",
        "bricscad",
        "cad",
    ]:
        client.togroup("CAD")


mod = "mod4"
terminal = guess_terminal()

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    Key([mod], "left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "up", lazy.layout.up(), desc="Move focus up"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key(
        [mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"
    ),
    Key(
        [mod, "shift"],
        "l",
        lazy.layout.shuffle_right(),
        desc="Move window to the right",
    ),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    Key(
        [mod, "shift"],
        "left",
        lazy.layout.shuffle_left(),
        desc="Move window to the left",
    ),
    Key(
        [mod, "shift"],
        "right",
        lazy.layout.shuffle_right(),
        desc="Move window to the right",
    ),
    Key([mod, "shift"], "down", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "up", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key(
        [mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"
    ),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key(
        [mod, "control"],
        "left",
        lazy.layout.grow_left(),
        desc="Grow window to the left",
    ),
    Key(
        [mod, "control"],
        "right",
        lazy.layout.grow_right(),
        desc="Grow window to the right",
    ),
    Key([mod, "control"], "down", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "up", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod, "shift"], "q", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key(
        [mod],
        "t",
        lazy.window.toggle_floating(),
        desc="Toggle floating on the focused window",
    ),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod], "m", lazy.spawn("rofi -show drun"), desc="Apps"),
    Key([mod], "w", lazy.spawn("brave"), desc="Web Browser"),
    Key([mod], "i", lazy.spawn("cursor"), desc="IDE"),
    Key([mod], "e", lazy.spawn("thunar"), desc="File Browser"),
    Key([mod], "v", lazy.spawn("copyq show"), desc="Clipboard"),
    Key([mod], "c", lazy.spawn("gnome-calculator"), desc="Calculator"),
    Key([mod, "shift"], "d", lazy.spawn("discord"), desc="Discord"),
    Key([mod, "shift"], "s", lazy.spawn("steam"), desc="Steam"),
    Key("", "Print", lazy.spawn("flameshot gui"), desc="Screenshot tool"),
    # Monitor switcher - Win+P
    Key(
        [mod],
        "p",
        lazy.function(lambda qtile: cycle_monitors()),
        desc="Cycle monitor configurations",
    ),


    Key(
        [mod, "shift"],
        "p",
        lazy.function(lambda qtile: refresh_monitors()),
        desc="Cycle monitor configurations",
    ),
    Key([mod], "o", lazy.spawn(f"{terminal} -e orgm"), desc="Open orgm in terminal"),



    Key(
        [],
        "XF86AudioRaiseVolume",
        lazy.spawn("pamixer --increase 5"),
        desc="Increase volume",
    ),
    Key(
        [],
        "XF86AudioLowerVolume",
        lazy.spawn("pamixer --decrease 5"),
        desc="Decrease volume",
    ),
    Key(
        [],
        "XF86AudioMute",
        lazy.spawn("pamixer --toggle-mute"),
        desc="Mute/unmute volume",
    ),
    # Change wallpaper randomly
    Key(
        [mod, "shift"],
        "f",
        lazy.spawn(
            "sh -c 'feh --bg-scale \"$(find ~/Pictures -type f | shuf -n 1)\" --bg-scale \"$(find ~/Pictures -type f | shuf -n 1)\"'"
        ),
        desc="Change wallpaper randomly",
    ),
    # Suspend system
    Key([mod, "shift"], "l", lazy.spawn("systemctl suspend"), desc="Suspend system"),
    # Aumentar brillo
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl s +10%"), desc="Increase brightness"),
    
    # Disminuir brillo
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl s 10%-"), desc="Decrease brightness"),
    


]

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )


groups = [
    Group("IDE", layout="max"),
    Group("WEB", layout="columns"),
    Group("AI", layout="columns"),
    Group("CODE", layout="max"),
    Group("CAD", layout="max"),
    Group("DOC", layout="max"),
    Group("VIDEO", layout="max"),
    Group("CHAT", layout="max"),
    Group("MAIL", layout="matrix"),
    Group("GAME", layout="columns"),
]

# groups = [Group(i) for i in "1234567890"]

for i, n in zip(groups, "1234567890"):
    keys.extend(
        [
            # mod + group number = switch to group
            Key(
                [mod],
                str(n),
                lazy.group[i.name].toscreen(),
                desc=f"Switch to group {i.name}",
            ),
            # mod + shift + group number = switch to & move focused window to group
            Key(
                [mod, "shift"],
                str(n),
                lazy.window.togroup(i.name, switch_group=True),
                desc=f"Switch to & move focused window to group {i.name}",
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod + shift + group number = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layout_theme = {
    "border_focus": "#2040ff",
    "border_width": 2,
    "border_normal": "#000000",
    "border_normal_width": 2,
    "single_border_color": "#2040ff",
    "single_border_width": 2,
    "margin": [15, 15, 15, 15],
}

layouts = [
    layout.Columns(**layout_theme),
    layout.Max(margin=[15, 15, 15, 15]),
    # Try more layouts by unleashing below layouts.
    layout.Stack(
        num_stacks=2,
        margin=[10, 10, 10, 10],
        border_width=2,
        border_focus="#2040ff",
        border_normal="#000000",
    ),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    layout.TreeTab(margin=[15, 15, 15, 15]),
    # layout.VerticalTil1e(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="JetBrainsMono Nerd Font",
    fontsize=14,
    padding=4,
)
extension_defaults = widget_defaults.copy()


def triangle_widget_left(fg_color, n=0):
    arrow = ["◀", "▶", "▼", "▲"]
    return {
        # "background": fg_color,
        "foreground": fg_color,
        "padding": 0,
        "margin":0,
        "text": arrow[n],  # Triángulo relleno izquierda
        "font": "JetBrainsMono Nerd Font", 
        "fontsize": 80,
    }

def left_arrow(bg_color, fg_color):
    return widget.TextBox(
        text='\uE0B2',
        padding=0,
        fontsize=25,
        background=bg_color,
        foreground=fg_color)

def right_arrow(bg_color, fg_color):
    return widget.TextBox(
        text='\uE0B0',
        padding=0,
        fontsize=25,
        background=bg_color,
        foreground=fg_color)


color1 = "#ff00ff"
color2 = "#4040f0"
color3 = "#0000ff"
color4 = "#ffff00"
# transparent = "#20202091"
color_gray = "#404040"
color_white = "#ffffff"
color_black = "#000000"
transparent_black = "#00000000"

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(disable_drag=True),

                widget.CurrentLayout(),
                # widget.WindowName(),

                widget.Spacer(
                    expand=True,
                ),
                # Monitor switcher widget
                left_arrow(color_black, color2),
                widget.TextBox(
                    text="🖥",
                    background=color2,
                    foreground=color_white,
                    name="monitor_switcher",
                    # fontsize=24,
                    mouse_callbacks={
                        "Button1": lambda: cycle_monitors(),
                    },
                    padding=5,
                ),
                left_arrow(color2, color_black),

                widget.HDD(
                    device="nvme0n1",
                    format="NVME {HDDPercent}%",
                    padding=5,
                ),
                left_arrow(color_black, color2),
                widget.Memory(
                    # format="MEM {MemUsed} / {MemTotal}",
                    background=color2,
                    foreground=color_white,
                    padding=5,
                ),
                left_arrow(color2, color_black),
                widget.KeyboardLayout(
                    format="{name}",
                    padding=5,
                    foreground="#2280ff",
                    # background="#000000",
                ),
                left_arrow(color_black, color2),
                widget.CPU(
                    format="CPU {load_percent}%",
                    padding=5,
                    background=color2,
                    foreground=color_white,
                ),
                left_arrow(color2, color_black),
                widget.ThermalZone(
                    format="TEMP {temp}°C",
                    padding=5,
                ),
                left_arrow(color_black, color2),

                # widget.Volume(
                #     fmt="VOL: {}",
                #     padding=5,
                # ),
                widget.Battery(
                    background=color2,
                    foreground=color_white,
                    padding=5,
                    discharge_char="Power off",
                    charge_char="Power on",
                    charging_foreground="#2280ff",
                    discharging_foreground="#ff0000",
                    format="{char} {percent:2.0%} BATTERY TIME: {hour:d}:{min:02d}",
                ),
                # left_arrow(color_black, color2),
                # widget.Backlight(
                #     # format="{state}",
                #     padding=5,
                #     foreground="#2280ff",
                # ),
                left_arrow(color2, color_black),
                widget.Systray(icon_size=24, padding=10),
                left_arrow(color_black, color2),
                widget.Clock(format="%I:%M %p %d-%b-%Y", background=color2, foreground=color_white),
                left_arrow(color2, color_black),
                widget.QuickExit(countdown_format="{}", default_text="[ Logout ]"),
            ],
            size=32,
            # opacity=0.9,
            margin=[10, 10, 10, 10],
            
            # background=transparent_black,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
        bottom=bar.Bar(
            [
                widget.TextBox(
                    text="MENU",
                    background=color2,
                    foreground=color_white,
                    name="menu",
                    # fontsize=24,
                    mouse_callbacks={
                        "Button1": lambda: subprocess.Popen(["rofi", "-show", "drun"]),
                    },
                    padding=5,
                ),
                widget.Prompt(),
                # widget.Spacer(
                #     expand=True,
                # ),
                widget.TaskList(
                    # format="{name}",
                    # fontsize=14,
                    expand=True,
                    # foreground=color_white,
                    # background=color2,
                    # max_title_width=350,
                    borderwidth=2,
                    border=color2,  # Color del borde para ventanas activas
                    unfocused_border=color_gray,  # Color del borde para ventanas inactivas
                    highlight_method="border",  # Resaltar con borde
                    rounded=False,  # Sin bordes redondeados
                    margin=3,  # Margen entre tareas
                    spacing=10,  # Espacio entre tareas
                    icon_size=14,
                    # padding=10,
                ),

            ],
            size=32,
            # opacity=0.9,
            margin=[10, 10, 10, 10],
            # background="#20202091",
        ),
        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        x11_drag_polling_rate = 120,
    ),
    Screen(),  # Segunda pantalla sin barras
]

# Drag floating layouts.
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = True
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
        Match(wm_class="Thunar"),
        Match(wm_class="copyq"),
        Match(wm_class="org.gnome.Nautilus"),
        Match(wm_class="blueman-manager"),
        Match(title="Friends List"),
        Match(title="Bluetooth Devices"),
        Match(title="Calculator"),
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = False

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = "Bibata-Modern-Amber"
wl_xcursor_size = 24 

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.

wmname = "qtile"
