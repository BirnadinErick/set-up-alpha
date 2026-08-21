"""
System-level configuration and package management task for pyinfra.
Updates system packages and configures base settings.
"""
from pyinfra import host
from pyinfra.operations import apt

# Retrieve configuration parameters from host.data (with sensible defaults)
cache_time: int = host.data.get("apt_cache_valid_time", 3600)
upgrade_type: str = host.data.get("apt_upgrade_type", "upgrade")
auto_remove: bool = host.data.get("apt_auto_remove", True)

# 1. Update apt repositories (equivalent to apt-get update)
# Using cache_time avoids redundant requests during consecutive runs
apt.update(
    name="Update APT repositories",
    cache_time=cache_time,
    _sudo=True,
)

# 2. Upgrade all packages
if upgrade_type == "dist_upgrade":
    apt.dist_upgrade(
        name="Upgrade system packages (dist-upgrade)",
        auto_remove=auto_remove,
        _sudo=True,
    )
elif upgrade_type == "upgrade":
    apt.upgrade(
        name="Upgrade system packages",
        _sudo=True,
    )
