sudo chmod +x disable-led.sh
sudo cp disable-led.service /etc/systemd/system/disable-led.service
sudo cp kasa-dimmer.service /etc/systemd/system/kasa-dimmer.service
sudo systemctl enable kasa-dimmer.service
sudo systemctl enable disable-led.service
