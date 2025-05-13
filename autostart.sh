#!/bin/bash
xrandr --output eDP-1 --scale 1x1 --output HDMI-1 --off &
xrandr --output eDP-1 --auto --scale 0.85x0.85 --output HDMI-1 --auto --right-of eDP-1 &
xrandr --output eDP-1 --auto --scale 1x1 --output HDMI-1 --auto --right-of eDP-1 &
xrandr --output eDP-1 --off --output HDMI-1 --auto --right-of eDP-1 &
flameshot &
nextcloud &
copyq &
nm-applet &
blueman-applet &
volumeicon &
dunst &
feh --bg-scale ~/Pictures/wallpaper1.jpg &
# feh --bg-scale ~/Pictures/wallpaper2.jpg --screen 1 &
setxkbmap -layout "us,latam" -option "grp:alt_shift_toggle" &
picom --config ~/.config/picom.conf &
xautolock -time 5 -locker "i3lock -n -c 00000000" &
brave-browser &                                                                                              