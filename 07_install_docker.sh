#!/usr/bin/env  bash
sudo dnf config-manager addrepo --from-repofile=https://download.docker.com/linux/fedora/docker-ce.repo
sudo dnf -y install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo systemctl enable --now docker

# add $USER to docker grp
sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker
