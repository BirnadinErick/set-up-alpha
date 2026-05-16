
echo "Installing Docker..."
sudo dnf install -y docker docker-compose
sudo systemctl enable --now docker
sudo usermod -aG docker $USER
echo "Added $USER to docker group. You may need to log out and log back in for this to take effect."