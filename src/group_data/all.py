"""
Shared configuration variables for the homelab infrastructure.
Applied to all hosts in the inventory.
"""

import getpass

# sudo password for the remote server
# _sudo_user= "be"
_sudo_password = getpass.getpass("Enter sudo password: ")

# Timezone configuration
timezone: str = "Europe/Berlin"

# APT Package Manager configuration
apt_cache_valid_time: int = 3600  # seconds to cache apt repository index updates
apt_upgrade_type: str = "upgrade"  # "dist_upgrade" or "upgrade"
apt_auto_remove: bool = True  # clean up unused dependencies during upgrade

# Docker configuration parameters
# Used by tasks in src/tasks/docker.py
docker_gpg_url: str = "https://download.docker.com/linux/ubuntu/gpg"
docker_repo_url: str = "https://download.docker.com/linux/ubuntu"
docker_keyring_path: str = "/etc/apt/keyrings/docker.asc"
docker_packages: list[str] = [
    "docker-ce",
    "docker-ce-cli",
    "containerd.io",
    "docker-buildx-plugin",
    "docker-compose-plugin",
]
