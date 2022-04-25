from os.path import exists
from subprocess import run

from tasks.util.env import (
    INVENTORY_FILE,
    ANSIBLE_DIR,
)


def check_inventory():
    if not exists(INVENTORY_FILE):
        print("Must set up inventory file at {}".format(INVENTORY_FILE))
        raise RuntimeError("No inventory file found")

    return INVENTORY_FILE


def run_ansible_playbook(playbook):
    check_inventory()

    cmd = ["ansible-playbook", "-i {}".format(INVENTORY_FILE), playbook]
    cmd = " ".join(cmd)
    print(cmd)

    run(cmd, shell=True, check=True, cwd=ANSIBLE_DIR)
