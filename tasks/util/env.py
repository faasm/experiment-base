from os.path import dirname, realpath

PROJ_ROOT = dirname(dirname(dirname(realpath(__file__))))
FAASM_DIR = "{}/faasm".format(PROJ_ROOT)
