import os
import subprocess

interpreter = subprocess.run(["whereis", "flask"], stdout=subprocess.PIPE, text=True)
dir = os.getcwd()

service = f"""
[Unit]
Description=ZoomSignWebserver
After=multi-user.target

[Service]
type=idle
ExecStartPre=cd {os.getcwd()}/
ExecStart={interpreter.stdout.strip()} run --host=0.0.0.0

[Install]
WantedBy=multi-user.target
"""

with open("ZoomSignWebserver.service", "w+") as file:
    file.write(service)

print("Generated service file.")