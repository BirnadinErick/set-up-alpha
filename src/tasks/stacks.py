"""
Docker Compose service stack management.
Deploys and manages self-hosted services using docker.compose operations.
References templates in `src/templates/`.
"""

import os

from pyinfra import host
from pyinfra.operations import docker, files

# Retrieve configuration parameters from host.data
deploy_user: str = host.data.get("deploy_user", "be")
stacks_dir: str = host.data.get("stacks_dir", "/opt/stacks")

dozzle_dir = f"{stacks_dir}/dozzle"

# 1. Ensure the Dozzle stack directory exists
files.directory(
    name="Ensure Dozzle stack directory exists",
    path=dozzle_dir,
    present=True,
    mode="0775",
    user=deploy_user,
    group="docker",
)

# 2. Copy the docker-compose.yaml file to the target
files.put(
    name="Upload Dozzle docker-compose.yaml",
    src=os.path.join(os.path.dirname(__file__), "..", "templates", "dozzle", "docker-compose.yaml"),
    dest=f"{dozzle_dir}/docker-compose.yaml",
    mode="0664",
    user=deploy_user,
    group="docker",
)

# 3. Deploy the Dozzle stack
docker.compose(
    name="Deploy Dozzle stack using docker compose",
    project_directory=dozzle_dir,
    project_name="dozzle",
    present=True,
)
