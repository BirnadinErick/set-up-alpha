"""
Target hosts, SSH connection parameters, and group definitions for pyinfra.
"""

# Define target hosts
# To run on a remote server:
# homelab_servers = [
#     ("192.168.1.100", {"ssh_user": "ubuntu", "ssh_key": "~/.ssh/id_rsa"})
# ]
#
# For default/safe execution, we target @localhost.
homelab_servers = [("homeserver")]
