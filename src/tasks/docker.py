"""
Docker CE engine and Compose plugin installation task.
Converts shell repository setup commands to declarative pyinfra operations.
References configuration parameters defined in `src/group_data/all.py`.
"""

from pyinfra import host
from pyinfra.facts.server import Arch, LinuxDistribution
from pyinfra.operations import apt, files, server

# 1. Retrieve configurations from host.data (with defaults defined in src/group_data/all.py)
docker_gpg_url: str = host.data.get(
    "docker_gpg_url", "https://download.docker.com/linux/ubuntu/gpg"
)
docker_repo_url: str = host.data.get(
    "docker_repo_url", "https://download.docker.com/linux/ubuntu"
)
docker_keyring_path: str = host.data.get(
    "docker_keyring_path", "/etc/apt/keyrings/docker.asc"
)
docker_packages: list[str] = host.data.get(
    "docker_packages",
    [
        "docker-ce",
        "docker-ce-cli",
        "containerd.io",
        "docker-buildx-plugin",
        "docker-compose-plugin",
    ],
)
cache_time: int = host.data.get("apt_cache_valid_time", 3600)

# 2. Gather architecture mapping to support Debian/Ubuntu specific names.
# uname -m (pyinfra server.Arch) returns x86_64 or aarch64, but Docker repos use amd64 or arm64.
ARCH_MAP = {
    "x86_64": "amd64",
    "aarch64": "arm64",
    "armv7l": "armhf",
}
raw_arch = host.get_fact(Arch)
arch = ARCH_MAP.get(raw_arch, raw_arch)

# 3. Gather OS release/distribution details (specifically codename)
distro = host.get_fact(LinuxDistribution)
codename = (
    distro.get("release_meta", {}).get("UBUNTU_CODENAME")
    or distro.get("release_meta", {}).get("VERSION_CODENAME")
    or distro.get("codename")
)
if not codename:
    raise ValueError("Could not determine the Linux distribution codename.")

# 4. Ensure prerequisites are installed
apt.packages(
    name="Install prerequisites for Docker repository",
    packages=["ca-certificates", "curl"],
    _sudo=True,
)

# 5. Create /etc/apt/keyrings directory with correct mode and ownership
files.directory(
    name="Ensure /etc/apt/keyrings directory exists",
    path="/etc/apt/keyrings",
    present=True,
    mode="0755",
    user="root",
    group="root",
    _sudo=True,
)

# 6. Add Docker's official GPG key
apt.key(
    name="Add Docker's official GPG key",
    src=docker_gpg_url,
    # pyrefly: ignore [unexpected-keyword]
    dest=docker_keyring_path,
    _sudo=True,
)

# 7. Explicitly set permissions/ownership on the GPG key file
files.file(
    name="Set permissions for Docker GPG key",
    path=docker_keyring_path,
    user="root",
    group="root",
    mode="0644",
    _sudo=True,
)

# 8. Add the Docker APT repository using the correct architecture and codename
apt.repo(
    name="Add Docker's official APT repository",
    src=f"deb [arch={arch} signed-by={docker_keyring_path}] {docker_repo_url} {codename} stable",
    filename="docker",
    _sudo=True,
)

# 9. Explicitly set permissions/ownership on the repository file
files.file(
    name="Set permissions for Docker repository source file",
    path="/etc/apt/sources.list.d/docker.list",
    user="root",
    group="root",
    mode="0644",
    _sudo=True,
)
apt.update(
    cache_time=cache_time,
    _sudo=True,
)

# 10. Install Docker Engine and plugins
apt.packages(
    name="Install Docker Engine packages",
    packages=docker_packages,
    _sudo=True,
)

# 11. Ensure Docker service is enabled and running
server.service(
    name="Ensure Docker service is running and enabled",
    service="docker",
    running=True,
    enabled=True,
    _sudo=True,
)
