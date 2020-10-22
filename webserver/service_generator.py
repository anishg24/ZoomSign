import os
import subprocess

interpreter = subprocess.run(["whereis", "python3"], stdout=subprocess.PIPE, text=True)
dir = os.getcwd()

service = f"""
[Unit]
Description=ZoomSignWebserver
After=multi-user.target

[Service]
type=idle
ExecStart={interpreter.stdout.strip()} {os.getcwd()}/app.py

[Install]
WantedBy=multi-user.target
"""

with open("ZoomSignWebserver.service", "w+") as file:
    file.write(service)

print("Generated service file.")