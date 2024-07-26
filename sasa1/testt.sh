#!/bin/bash

# Open the first terminal window and run the first set of commands
gnome-terminal -- bash -c "cd /home/oem/sasa && python3 RobotControllerGUI.py; exec bash"

# Open the second terminal window and run the second set of commands
gnome-terminal -- bash -c "cd /home/oem/sasa1 && python3 RobotControllerGUI.py; exec bash"

