# Homelab Setup Alpha - Documentation

This directory contains the documentation relating to the design decisions, layout, and configuration of the Homelab Infrastructure-as-Code setup.

## Project Structure & Architecture

The repository is organized following the conventions specified in [AGENTS.md](../AGENTS.md):

- `src/`:
  - `inventory.py`: Defines the target server inventory group `homelab_servers`. By default, this is set to `@localhost` for safe local dry-runs and testing.
  - `deploy.py`: The entrypoint for execution, managing task modularization using relative file inclusions with `local.include`.
  - `group_data/all.py`: Contains variables globally applied to all hosts, such as package manager behavior and system configurations.
  - `tasks/`:
    - `system.py`: Implements package manager updates and upgrades (`apt`). It reads variables like `apt_cache_valid_time` and `apt_upgrade_type` from `group_data/all.py` to maintain modularity and avoid hardcoding values in task files.
    - `security.py`: Hardens the SSH daemon to enforce public key authentication and disable password-based logins.
    - `docker.py`: Installs and configures Docker CE engine, Compose plugin, and manages the daemon state.
    - `stacks.py`: Stub for Docker Compose services.

## Docker Engine Installation (`tasks/docker.py`)

The Docker Engine installation and configuration follow standard, modern security and administrative practices:

1. **Centralized Configuration**: All properties (such as package lists, GPG URLs, repository URLs, and keyring paths) are defined in [`src/group_data/all.py`](../src/group_data/all.py) to prevent hardcoding configuration values inside tasks.
2. **Keyring Directory Management**: Ensures that the `/etc/apt/keyrings/` directory exists with secure ownership (`root:root`) and permissions (`0755`) prior to downloading external keys.
3. **GPG Key Management**: Fetches the official Docker GPG key and writes it securely (`0644`) to `/etc/apt/keyrings/docker.asc` using `apt.key`, avoiding the deprecated `apt-key` tool.
4. **Dynamic Metadata Resolution**: Resolves the CPU architecture (mapping `uname -m` formats such as `x86_64` to Debian architecture strings like `amd64`) and queries target OS release codenames dynamically via `LinuxDistribution` facts.
5. **Apt Repository Configuration**: Integrates the repository using `apt.repo` with proper signature verification linking to the downloaded keyring, setting file permissions securely (`0644`) on the generated `/etc/apt/sources.list.d/docker.list`.
6. **Service Management**: Installs the complete Docker CE suite (including buildx and compose plugins) and ensures the `docker` daemon is enabled at boot and active using `server.service`.

## System Package Updates & Upgrades (`tasks/system.py`)

To ensure standard operations, the update process is designed with the following principles:

1. **Idempotency**: Using built-in high-level `pyinfra.operations.apt` instead of shell commands.
2. **Caching**: We pass `cache_time` parameter to `apt.update` to prevent redownloading repository database indexes during consecutive runs, matching `apt_cache_valid_time` in configuration.
3. **Upgrade Strategy**: Configuration `apt_upgrade_type` controls whether `dist_upgrade` (with intelligent dependency resolver and optional `auto_remove`) or a regular `upgrade` is performed.


## Security Hardening (`tasks/security.py`)

To secure SSH access to the hosts, the SSH daemon configuration is hardened using the following declarative approach:

1. **Centralized Configuration**: All parameters (such as SSH config paths, service name, and authentication modes) are defined in [`src/group_data/all.py`](../src/group_data/all.py) to prevent hardcoding.
2. **Password Authentication Disabling**: Employs `files.line` to set `PasswordAuthentication no`, `KbdInteractiveAuthentication no`, and `ChallengeResponseAuthentication no` in the main configuration file `/etc/ssh/sshd_config`.
3. **Public Key Authentication Enforcement**: Employs `files.line` to set `PubkeyAuthentication yes` in `/etc/ssh/sshd_config`.
4. **Cloud-Init Override Handling**: Dynamically detects the presence of `/etc/ssh/sshd_config.d/50-cloud-init.conf` using a `File` fact and automatically disables password authentication there if present, preventing the default cloud-init overrides on cloud providers.
5. **Conditional Service Reload**: Captures the change state of the files and reloads the SSH daemon service (`ssh`) using `server.service` only when a modification has occurred, ensuring active sessions are not interrupted unnecessarily.

## Offline Wi-Fi Bootstrapping (`src/templates/99-custom-wifi.yaml`)

If the target server is offline and requires Wi-Fi connectivity to connect to the internet (enabling `pyinfra` deployments and package updates), you must bootstrap the network configuration manually before running deployments:

1. **Configure Credentials**: Edit the Wi-Fi credentials in [`src/templates/99-custom-wifi.yaml`](../src/templates/99-custom-wifi.yaml):
   - Replace `TODO_USERNAME` with your WPA2 Enterprise (PEAP) identity.
   - Replace `TODO_PASSWORD` with your password.
2. **Transfer via USB**: Copy the modified `99-custom-wifi.yaml` file to a USB flash drive.
3. **Mount and Copy on the Server**: Plug the USB drive into the offline server, mount it, and copy the configuration file to the correct Netplan path:
   ```bash
   # Find your USB partition (e.g., /dev/sdb1)
   lsblk
   
   # Mount the USB
   sudo mount /dev/sdb1 /mnt
   
   # Copy the file
   sudo cp /mnt/99-custom-wifi.yaml /etc/netplan/99-custom-wifi.yaml
   ```
4. **Set Correct Permissions**: Netplan requires strict file permissions to function. Run:
   ```bash
   sudo chmod 600 /etc/netplan/99-custom-wifi.yaml
   ```
5. **Generate and Apply Configuration**: Run the Netplan commands to generate and apply the new configuration:
   ```bash
   sudo netplan generate
   sudo netplan apply
   ```
6. **Verify Connection**: Once applied, verify that the server has retrieved an IP address on `wlo1` and can connect to the internet (e.g., via `ping -c 3 8.8.8.8`).
