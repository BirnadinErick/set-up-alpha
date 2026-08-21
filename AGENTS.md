# pyinfra Homelab Infrastructure as Code - Agent Guidelines

## Context & Architecture
This repository contains a declarative infrastructure-as-code setup using `pyinfra` to configure fresh Ubuntu Server installations and manage self-hosted Docker services.

### Project Layout

Every app project should resice under src-directory
- `src/`:  
    - `inventory.py`: Target hosts, SSH connection parameters, and group definitions.
    - `deploy.py`: Main deployment entrypoint importing task modules in execution order.
    - `group_data/all.py`: Shared configuration variables (paths, usernames, timezone, common package lists).
    - `tasks/`:
    - `system.py`: Base packages, user management, sudoers, timezone, and kernel parameters.
    - `security.py`: SSH hardening, UFW firewall rules, and automatic security updates.
    - `docker.py`: Docker CE engine, Compose plugin installation, and service configuration.
    - `stacks.py`: Docker Compose directory layout, compose files, env files, and container lifecycle.
    - `templates/`: Jinja2 templates for system configs and service environments.
    - `files/`: Static configuration files and Docker compose definitions.
- `docs`: directory for saving documents related to the project.
---

## Agent Instructions & Coding Rules

### 1. Operation Idempotency
- Always prefer high-level `pyinfra.operations` (e.g., `apt.packages`, `files.template`, `server.service`, `files.directory`) over raw shell commands (`server.shell`).
- Never use non-idempotent raw shell commands unless no built-in operation exists. When raw shell is necessary, use check commands (`server.shell` with condition parameters or custom guard logic) to prevent unnecessary execution.
- Maintain immutability and predictability across successive runs.

### 2. Configuration Standards
- Avoid hardcoded values in task files. Store all hostnames, paths, user IDs, and environment-specific parameters in `group_data/` or host data files.
- Keep secrets and API keys outside git tracking. Use environment variables or an external secret vault/env template. If you need to store secrets, edit the env files in .env
- Ensure all created directories and synchronized files explicitly define permissions (`mode`) and ownership (`user`, `group`).

### 3. Docker Service Management
- Standardize all Docker service directories under a single base directory in the home directory of the user "be" (e.g., `/home/be/<service-name>/`).
- Place `docker-compose.yml` and `.env` files into their respective service directory using `files.put` or `files.template`.
- Use standard compose commands (`docker compose up -d --remove-orphans`) to manage container state so unchanged containers are automatically skipped.

### 4. Code Style & Conventions
- Use Python 3.10+ features with clean type annotations where helpful.
- Keep responses, documentation, and task scripts simple, structured, and modular.
- Do not add extraneous dependencies or wrapper scripts beyond `pyinfra`.
- Always add or update the docs direcotry with proper reasioning why some decisions were made.
- Keep the documentation up to date with the latest changes.
- Always explain your reasoning in the docstrings and comments.
- Always use relative file paths for referencing project files and directories in documentation, markdown files, and code comments.

---

## Verification & Execution Commands
- Preview planned changes without applying:
  ```bash
  uvx pyinfra inventory.py deploy.py --dry -vv
  ```

  DON'T run this command unless explicitly asked for. Usually just edit the files and let me know and I will run it.