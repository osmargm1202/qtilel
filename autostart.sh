#!/bin/bash
python3 monitor_cycle.py first_time
flameshot &
nextcloud &
copyq &
nm-applet &
blueman-applet &
volumeicon &
dunst &
feh --bg-scale ~/Pictures/wallpaper1.jpg --bg-scale ~/Pictures/wallpaper3.jpg &
# feh --bg-scale ~/Pictures/wallpaper2.jpg --screen 1 &
setxkbmap -layout "us,latam" -option "grp:alt_shift_toggle" &
picom --config ~/.config/picom.conf &
xautolock -time 5 -locker "i3lock -n -c 00000000" &
brave-browser &                                                                                              