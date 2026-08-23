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

homepage_dir = f"{stacks_dir}/homepage"

# 4. Ensure the Homepage stack directory exists
files.directory(
    name="Ensure Homepage stack directory exists",
    path=homepage_dir,
    present=True,
    mode="0775",
    user=deploy_user,
    group="docker",
)

# 5. Copy the Homepage docker-compose.yaml file to the target
files.put(
    name="Upload Homepage docker-compose.yaml",
    src=os.path.join(os.path.dirname(__file__), "..", "templates", "homepage", "docker-compose.yaml"),
    dest=f"{homepage_dir}/docker-compose.yaml",
    mode="0664",
    user=deploy_user,
    group="docker",
)

# 6. Synchronize the Homepage config directory to the target
files.sync(
    name="Sync Homepage config directory",
    src=os.path.join(os.path.dirname(__file__), "..", "templates", "homepage", "config"),
    dest=f"{homepage_dir}/config",
    user=deploy_user,
    group="docker",
    mode="0664",
    dir_mode="0775",
    delete=True,
)

# 7. Deploy the Homepage stack
docker.compose(
    name="Deploy Homepage stack using docker compose",
    project_directory=homepage_dir,
    project_name="homepage",
    present=True,
)

