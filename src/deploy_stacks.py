"""
User-space Docker stack management (unprivileged).
"""

import os

from pyinfra import local

# Get the directory of this file
deploy_dir = os.path.dirname(os.path.abspath(__file__))

# 1. Service stacks lifecycle
local.include(os.path.join(deploy_dir, "tasks", "stacks.py"))
