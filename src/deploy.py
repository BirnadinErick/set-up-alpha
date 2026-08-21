"""
Main deployment entrypoint for pyinfra.
Imports task modules in execution order.
"""

import os

from pyinfra import local

# Get the directory of deploy.py
deploy_dir = os.path.dirname(os.path.abspath(__file__))

# 1. System task (includes apt update/upgrade)
local.include(os.path.join(deploy_dir, "tasks", "system.py"))

# 2. Security hardening tasks (placeholder stub)
# local.include(os.path.join(deploy_dir, "tasks", "security.py"))

# 3. Docker configuration tasks
local.include(os.path.join(deploy_dir, "tasks", "docker.py"))

# 4. Service stacks lifecycle (placeholder stub)
# local.include(os.path.join(deploy_dir, "tasks", "stacks.py"))
