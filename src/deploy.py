"""
Main deployment entrypoint for pyinfra.
Runs both system bootstrapping and user-space stack deployment.
"""

import os

from pyinfra import local

# Get the directory of this file
deploy_dir = os.path.dirname(os.path.abspath(__file__))

# 1. Run system bootstrapping operations (privileged)
local.include(os.path.join(deploy_dir, "deploy_system.py"))

# 2. Run user-space Docker stack management (unprivileged)
local.include(os.path.join(deploy_dir, "deploy_stacks.py"))
