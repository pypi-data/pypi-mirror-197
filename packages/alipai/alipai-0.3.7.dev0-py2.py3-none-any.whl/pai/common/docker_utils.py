import io
import json
import logging
import os
import shutil
import socket
import subprocess
import tempfile
import textwrap
import time
from random import randint
from typing import Any, Dict, List, Optional, Union

import docker

logger = logging.getLogger(__name__)

DEFAULT_CONTAINER_WORK_DIR = "/ml/code"
DEFAULT_REQUIREMENTS_PATH = "requirements.txt"


def build_image(
    output_image_uri: str = None,
    base_image: str = None,
    script_dir: str = None,
    entry_point: str = None,
    expose_ports: Optional[List[int]] = None,
    requirements_path: Optional[str] = DEFAULT_REQUIREMENTS_PATH,
    container_work_dir: str = DEFAULT_CONTAINER_WORK_DIR,
    extra_packages: List[str] = None,
):
    """Build a docker image."""

    # use a temporary directory as docker build context.
    temp_dir = tempfile.mkdtemp()
    if script_dir:
        if not os.path.isdir(script_dir):
            raise ValueError("Script source should be a directory.")
        code_dir = os.path.join(temp_dir, "usercode")
        shutil.copytree(script_dir, code_dir)
        # check if the requirements_path is exists.
        if requirements_path and not os.path.exists(
            os.path.join(code_dir, requirements_path)
        ):
            # if the default requirements path is used, do not raise error if the file is not exists.
            if requirements_path == DEFAULT_REQUIREMENTS_PATH:
                pass
            raise ValueError(
                "requirements path is specified but the file is not exists: requirement_path={}.".format(
                    requirements_path
                )
            )
        script_dir = os.path.basename(code_dir)

    dockerfile = _make_dockerfile(
        worker_dir=container_work_dir,
        base_image=base_image,
        script_dir=script_dir,
        entry_point=entry_point,
        requirements_path=requirements_path,
        extra_packages=extra_packages,
        expose_ports=expose_ports,
    )
    print(dockerfile)

    build_command = [
        "docker",
        "build",
        "-t",
        output_image_uri,
        "-f-",
        temp_dir,
    ]
    ret_code = _run_command(build_command, input=dockerfile)
    if ret_code != 0:
        raise RuntimeError(
            "Build Docker container failed: command={} return_code={}".format(
                " ".join(build_command), ret_code
            )
        )
    return output_image_uri


def _run_command(command: List[str], input: Optional[str] = None):
    with subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=False,
        bufsize=1,
    ) as p:
        if input:
            p.stdin.write(input.encode())
        p.stdin.close()
        out = io.TextIOWrapper(p.stdout, newline="", errors="replace")
        for line in out:
            logger.info(line)

    return p.returncode


def _make_dockerfile(
    worker_dir: str,
    base_image: str,
    entry_point: str,
    script_dir: str = None,
    expose_ports: Optional[List[int]] = None,
    requirements_path: Optional[str] = None,
    extra_packages: List[str] = None,
):
    """Make a Dockerfile for building the specific image"""
    # Initialize Dockerfile
    # default_pip_index_url = "https://pypi.tuna.tsinghua.edu.cn/simple"
    default_pip_index_url = "https://mirrors.aliyun.com/pypi/simple/"

    contents = [
        textwrap.dedent(
            """
        FROM {base_image}
        ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

        # Use aliyun pip mirror by default.
        ENV PIP_INDEX_URL={pip_index_url}

        """.format(
                base_image=base_image,
                pip_index_url=default_pip_index_url,
            )
        )
    ]

    # install requirements
    if requirements_path:
        contents.append(
            textwrap.dedent(
                f"""
            ADD {script_dir}/{requirements_path} /tmp/
            RUN python -m pip install --no-cache-dir -r /tmp/{requirements_path}
            """
            )
        )

    # Add source files to the image.
    if script_dir:
        contents.append(
            textwrap.dedent(
                """
                WORKDIR {work_dir}
                ADD {source_dir} {work_dir}
                """.format(
                    work_dir=worker_dir,
                    source_dir=script_dir,
                )
            )
        )

    # install extra_packages:
    if extra_packages:
        for pkg in extra_packages:
            contents.append(
                textwrap.dedent(
                    f"""
                    RUN python -m pip install --no-cache-dir {pkg}
                    """
                )
            )

    # Expose port
    if expose_ports:
        for port in expose_ports:
            contents.append(
                textwrap.dedent(
                    f"""
                    EXPOSE {port}
                    """
                )
            )

    # install container ENTRYPOINT
    if entry_point:
        if entry_point.endswith(".py"):
            # hack: allspark worker exit immediately if it found the parent process
            # is init process (pid=1).
            entry_module = entry_point[:-3].replace("/", ".")
            contents.append(
                textwrap.dedent(
                    """ENTRYPOINT python -m {module}""".format(module=entry_module)
                )
            )
        elif entry_point.endswith(".bash"):
            contents.append(
                textwrap.dedent(
                    """ENTRYPOINT {}""".format(json.dumps(["bash", entry_point]))
                )
            )
        else:
            contents.append(textwrap.dedent("""ENTRYPOINT {}""".format([entry_point])))

    return "\n".join(contents)


class ContainerRun(object):
    """A class represent a container run in local."""

    CONTAINER_STATUS_RUNNING = "running"
    CONTAINER_STATUS_TERMINATED = ["exited", "paused"]

    def __init__(self, container: docker.models.containers.Container, port: int):
        self.container = container
        self.port = port

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def is_running(self):
        return self.container.status == self.CONTAINER_STATUS_RUNNING

    def is_terminated(self):
        return self.container.status in self.CONTAINER_STATUS_TERMINATED

    def wait_for_ready(self, interval=1):
        """Wait util container is ready.

        If a port is specified, wait utils server is ready.

        """
        while True:
            self.container.reload()
            if self.is_running():
                break
            elif self.is_terminated():
                raise RuntimeError(
                    "Container is terminated: id={} status={}".format(
                        self.container.id, self.container.status
                    )
                )
            time.sleep(interval)

        if self.port:
            self._wait_for_serving(interval=interval)

    def _wait_for_serving(self, timeout=20, interval=1):
        start_time = time.time()
        while True:
            try:
                s = socket.create_connection(("127.0.0.1", self.port))
                s.close()
                return
            except socket.error as e:
                elapse = time.time() - start_time
                if elapse > timeout:
                    raise RuntimeError(
                        "Wait for container serving timeout, connection error: %s", e
                    )
                time.sleep(interval)
                continue

    def stop(self):
        self.container.reload()
        if self.is_running():
            self.container.stop()

    def start(self):
        self.container.reload()
        if not self.is_running():
            self.container.start()

    def delete(self):
        if self.is_running():
            self.container.stop()
        self.container.remove()

    def watch(self):
        log_iter = self.container.logs(
            stream=True,
            follow=True,
        )
        for log in log_iter:
            logger.info(log)
        self.container.reload()
        exit_code = self.container.attrs["State"]["ExitCode"]
        if exit_code != 0:
            raise RuntimeError(
                "Container run exited failed: exit_code={}".format(exit_code)
            )


def run_container(
    image_uri: str,
    container_name: str = None,
    port: int = None,
    environment_variables: Dict[str, str] = None,
    command: Union[List[str], str] = None,
    entry_point: Union[List[str], str] = None,
    volumes: Union[Dict[str, Any], List[str]] = None,
) -> ContainerRun:
    client = docker.from_env()
    # use a random host port.
    host_port = randint(50000, 65535)
    container = client.containers.run(
        name=container_name,
        entrypoint=entry_point,
        image=image_uri,
        command=command,
        environment=environment_variables,
        ports={port: host_port} if port else None,
        volumes=volumes,
        detach=True,
    )
    container_run = ContainerRun(
        container=container,
        port=host_port,
    )
    # container_run.wait_for_ready()
    # container_run.config_binding_host_port()
    return container_run


def push_image(image_uri, auth_config: Dict[str, str] = None):
    """Push an image to image registry."""

    client = docker.from_env()
    try:
        iterator = client.api.push(
            image_uri,
            stream=True,
            auth_config=auth_config,
            decode="utf-8",
        )
        log = None
        for log in iterator:
            logger.info(log)
        if log and "errorDetail" in log:
            raise Exception(str(log))
    finally:
        client.close()


def tag_image(source_image, target_image):
    """Create a tag 'target_image' to refer the 'source_image'."""
    command = ["docker", "tag", source_image, target_image]
    return_code = _run_command(command)
    if return_code != 0:
        raise RuntimeError(f"Failed to new image tag. command={command}")
