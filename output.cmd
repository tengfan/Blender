#!powershell
# This is a powershell script to execute the .exe and save the log in the current directory

del output.log
.\vrpn_print_devices.exe Tracker0@localhost >> output.log