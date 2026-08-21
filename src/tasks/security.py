"""
Security hardening tasks (SSH, UFW, automatic updates).
Configures SSH daemon settings to disable password authentication
and only allow public key authentication.
"""

from pyinfra import host
from pyinfra.facts.files import File
from pyinfra.operations import files, server

# 1. Retrieve SSH configurations from host.data (with fallback defaults)
# Configuration parameters are defined in src/group_data/all.py
ssh_config_path: str = host.data.get("ssh_config_path", "/etc/ssh/sshd_config")
ssh_cloud_init_config_path: str = host.data.get(
    "ssh_cloud_init_config_path", "/etc/ssh/sshd_config.d/50-cloud-init.conf"
)
ssh_service_name: str = host.data.get("ssh_service_name", "ssh")
ssh_password_authentication: str = host.data.get("ssh_password_authentication", "no")
ssh_pubkey_authentication: str = host.data.get("ssh_pubkey_authentication", "yes")
ssh_kbd_interactive_authentication: str = host.data.get(
    "ssh_kbd_interactive_authentication", "no"
)

# Track changes to conditionally reload SSH service to apply changes
ssh_changed = False

# 2. Configure PasswordAuthentication in sshd_config
change_password_auth = files.line(
    name="Set PasswordAuthentication in sshd_config",
    path=ssh_config_path,
    replace=f"PasswordAuthentication {ssh_password_authentication}",
    line="^#?PasswordAuthentication .*",
    _sudo=True,
)
if change_password_auth.will_change:
    ssh_changed = True

# 3. Configure PubkeyAuthentication in sshd_config
change_pubkey_auth = files.line(
    name="Set PubkeyAuthentication in sshd_config",
    path=ssh_config_path,
    line="^#?PubkeyAuthentication .*",
    replace=f"PubkeyAuthentication {ssh_pubkey_authentication}",
    _sudo=True,
)
if change_pubkey_auth.will_change:
    ssh_changed = True

# 4. Configure KbdInteractiveAuthentication in sshd_config
change_kbd_interactive_auth = files.line(
    name="Set KbdInteractiveAuthentication in sshd_config",
    path=ssh_config_path,
    line="^#?KbdInteractiveAuthentication .*",
    replace=f"KbdInteractiveAuthentication {ssh_kbd_interactive_authentication}",
    _sudo=True,
)
if change_kbd_interactive_auth.will_change:
    ssh_changed = True

# 5. Configure ChallengeResponseAuthentication in sshd_config
change_challenge_response_auth = files.line(
    name="Set ChallengeResponseAuthentication in sshd_config",
    path=ssh_config_path,
    line="^#?ChallengeResponseAuthentication .*",
    replace=f"ChallengeResponseAuthentication {ssh_kbd_interactive_authentication}",
    _sudo=True,
)
if change_challenge_response_auth.will_change:
    ssh_changed = True

# 6. Check and handle cloud-init SSH configuration override if present
# Some environments (like cloud-init default setups) overwrite settings in sshd_config.d
if host.get_fact(File, path=ssh_cloud_init_config_path):
    change_cloud_init = files.line(
        name="Disable PasswordAuthentication in 50-cloud-init.conf override",
        path=ssh_cloud_init_config_path,
        line="^#?PasswordAuthentication .*",
        replace=f"PasswordAuthentication {ssh_password_authentication}",
        _sudo=True,
    )
    if change_cloud_init.will_change:
        ssh_changed = True

# 7. Reload SSH service if configuration changed
if ssh_changed:
    server.service(
        name="Reload SSH service",
        service=ssh_service_name,
        reloaded=True,
        _sudo=True,
    )
