from os.path import join

from tasks.util.env import PROJ_ROOT, FAASM_DIR

experiments_version = None
faasm_version = None


def get_version():
    global experiments_version

    ver_file = join(PROJ_ROOT, "VERSION")

    if not experiments_version:
        with open(ver_file, "r") as fh:
            experiments_version = fh.read()
            experiments_version = experiments_version.strip()

    return experiments_version


def get_faasm_version():
    global faasm_version

    ver_file = join(FAASM_DIR, "VERSION")

    if not faasm_version:
        with open(ver_file, "r") as fh:
            faasm_version = fh.read()
            faasm_version = faasm_version.strip()

    return faasm_version
