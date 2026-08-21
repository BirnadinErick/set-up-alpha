# Setup Alpha

> this repo contains code to automate setting up the homeserver
> and managing the state of the homeserver

Currently, ´pyinfra´ powers the state management. pyinfra was chose over
ansible, due to my preference of code over YAML configs.

That is the only reason for this choice over ansible, and other available
solutions seem overkill for personal use.

The code does following:

- installs and updates the system
- creates snapshot before update and add it to the grub menu
- creates directory for docker files
- runs docker compose
- configures the network

## Development

Since the server is already running, the plan is to first mirror the server
now and then keeps on iterating the code.

Planned phases:

- Installed packages and updates
- Docker
- Tunnels Cloudflare+Tailscale
- Dazzle
- Webmin
- Homepage
- Adguard
- Immich
- Jellyfin

## Remarks

- needs to figure out a way to observe the server
