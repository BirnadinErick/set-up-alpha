"""
System bootstrapping operations (requires sudo).
"""

import os

from pyinfra import local

# Get the directory of this file
deploy_dir = os.path.dirname(os.path.abspath(__file__))

# 1. System task (includes apt update/upgrade)
local.include(os.path.join(deploy_dir, "tasks", "system.py"))

# 2. Security hardening tasks
local.include(os.path.join(deploy_dir, "tasks", "security.py"))

# 3. Docker configuration tasks
local.include(os.path.join(deploy_dir, "tasks", "docker.py"))
