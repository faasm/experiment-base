from os.path import join

from tasks.util.env import PROJ_ROOT


def _read_ver_file(file_path):
    with open(file_path, "r") as fh:
        ver = fh.read()
        ver = ver.strip()

    return ver


def get_version():
    return _read_ver_file(join(PROJ_ROOT, "VERSION"))


def get_k8s_version():
    return _read_ver_file(join(PROJ_ROOT, "K8S_VERSION"))
