#!/bin/bash

echo "Checking for url_recorder process..."
ps aux | grep url_recorder

echo "Checking for history.txt..."
if [ -f "history.txt" ]; then
    echo "history.txt found. Content:"
    cat history.txt
else
    echo "history.txt not found."
fi

echo "Checking system logs..."
sudo tail -n 100 /var/log/syslog
sudo tail -n 100 /var/log/auth.log

echo "Checking custom logs..."
sudo tail -n 100 url_recorder.log
sudo tail -n 100 url_recorder_error.log

echo "Checking active window title..."
xdotool getwindowfocus getwindowname

echo "Checking clipboard content..."
xclip -o  # or pbpaste on macOS

echo "Checking network connections..."
sudo netstat -tulnp

echo "Checking resource utilization..."
top -n 1 -b | head -n 20