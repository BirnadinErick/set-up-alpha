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
