from os.path import join
from subprocess import run

from invoke import task
from tasks.util.env import PROJ_ROOT
from tasks.util.version import get_version, get_faasm_version

EXPERIMENT_BASE_IMAGE_NAME = "experiment-base"


def _get_docker_tag(img_name):
    ver = get_version()
    return "faasm/{}:{}".format(img_name, ver)


def _build_container(name, nocache=False, push=False):
    tag_name = _get_docker_tag(name)
    faasm_ver = get_faasm_version()

    if nocache:
        no_cache_str = "--no-cache"
    else:
        no_cache_str = ""

    dockerfile = join(PROJ_ROOT, "docker", "{}.dockerfile".format(name))

    build_cmd = [
        "docker build",
        no_cache_str,
        "-t {}".format(tag_name),
        "-f {}".format(dockerfile),
        "--build-arg FAASM_VERSION={}".format(faasm_ver),
        ".",
    ]
    build_cmd = " ".join(build_cmd)

    print(build_cmd)
    run(build_cmd, shell=True, check=True, env={"DOCKER_BUILDKIT": "1"})

    if push:
        push_image(name)


def push_image(name):
    tag_name = _get_docker_tag(name)

    cmd = "docker push {}".format(tag_name)
    print(cmd)
    run(cmd, shell=True, check=True)


@task
def build(ctx, nocache=False, push=False):
    """
    Build current version of the base experiment container.
    """
    _build_container(EXPERIMENT_BASE_IMAGE_NAME, nocache=nocache, push=push)


@task
def push(ctx):
    """
    Push current version of the base experiment container.
    """
    push_image(EXPERIMENT_BASE_IMAGE_NAME)
