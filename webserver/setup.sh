python3 service_generator.py
cp ZoomSignWebserver.service /lib/systemd/system/ZoomSignWebserver.service
sudo chmod 644 /lib/systemd/system/ZoomSignWebserver.service

sudo systemctl daemon-reload
sudo systemctl enable ZoomSignWebserver.service

echo "Reboot your Pi to check if the service is enabled!"