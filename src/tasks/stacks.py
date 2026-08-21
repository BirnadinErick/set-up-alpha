"""
Docker Compose service stack management.
Deploys and manages self-hosted services using docker.compose operations.
References templates in `src/templates/`.
"""

import os

from pyinfra.operations import docker, files

# 1. Ensure the base stacks directory exists in the home directory of user 'be'
# files.directory(
#     name="Ensure /home/be/stacks directory exists",
#     path="/home/be/stacks",
#     present=True,
#     mode="0755",
#     user="be",
#     group="be",
# )

# 2. Ensure the Dozzle stack directory exists
files.directory(
    name="Ensure Dozzle stack directory exists",
    path="/home/be/dozzle",
    present=True,
    mode="0755",
    user="be",
    group="be",
)

# 3. Copy the docker-compose.yaml file to the target
files.put(
    name="Upload Dozzle docker-compose.yaml",
    src=os.path.join(os.path.dirname(__file__), "..", "templates", "dozzle", "docker-compose.yaml"),
    dest="/home/be/dozzle/docker-compose.yaml",
    mode="0644",
    user="be",
    group="be",
)

# 4. Deploy the Dozzle stack
docker.compose(
    name="Deploy Dozzle stack using docker compose",
    project_directory="/home/be/dozzle",
    project_name="dozzle",
    present=True,
)

