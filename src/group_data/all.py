"""
Shared configuration variables for the homelab infrastructure.
Applied to all hosts in the inventory.
"""

import getpass
import os
import sys

# Deploy user and stacks directory configurations
deploy_user: str = "be"
stacks_dir: str = "/opt/stacks"

# sudo password for the remote server
# Only prompt for sudo password if we are running system bootstrapping operations.
# We check if we are doing a stacks-only deployment (e.g. deploy_stacks.py is in the arguments).
is_stacks_only = any(arg.endswith(("deploy_stacks.py", "stacks.py")) for arg in sys.argv)

_sudo_password = None
if not is_stacks_only:
    _sudo_password = os.environ.get("SUDO_PASSWORD") or getpass.getpass("Enter sudo password: ")

# Timezone configuration
timezone: str = "Europe/Berlin"

# SSH configuration parameters
ssh_config_path: str = "/etc/ssh/sshd_config"
ssh_cloud_init_config_path: str = "/etc/ssh/sshd_config.d/50-cloud-init.conf"
ssh_service_name: str = "ssh"
ssh_password_authentication: str = "no"
ssh_pubkey_authentication: str = "yes"
ssh_kbd_interactive_authentication: str = "no"

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
