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
    - `security.py`: Stub for future security hardening (SSH keys, firewall setup).
    - `docker.py`: Stub for Docker runtime configuration.
    - `stacks.py`: Stub for Docker Compose services.

## System Package Updates & Upgrades (`tasks/system.py`)

To ensure standard operations, the update process is designed with the following principles:

1. **Idempotency**: Using built-in high-level `pyinfra.operations.apt` instead of shell commands.
2. **Caching**: We pass `cache_time` parameter to `apt.update` to prevent redownloading repository database indexes during consecutive runs, matching `apt_cache_valid_time` in configuration.
3. **Upgrade Strategy**: Configuration `apt_upgrade_type` controls whether `dist_upgrade` (with intelligent dependency resolver and optional `auto_remove`) or a regular `upgrade` is performed.

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
