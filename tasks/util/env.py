from os.path import dirname, realpath, join

PROJ_ROOT = dirname(dirname(dirname(realpath(__file__))))

BIN_DIR = join(PROJ_ROOT, "bin")
GLOBAL_BIN_DIR = "/usr/local/bin"

AZURE_RESOURCE_GROUP = "faasm"
AZURE_REGION = "eastus"

AZURE_STORAGE_SKU = "Standard_LRS"
AKS_CLUSTER_NAME = "faasm-cluster"

# 4 4-core machines: kernels, lammps, and migration experiment w/ 4 parallel functions
# AZURE_VM_SIZE = "Standard_D4_v5"
# AKS_CLUSTER_NODE_COUNT = 4

# 2 8-core machines: migration experiment w/ 8 parallel functions
# AZURE_VM_SIZE = "Standard_D8_v5"
# AKS_CLUSTER_NODE_COUNT = 2

# 1 16-core machine: LULESH experiment
AZURE_VM_SIZE = "Standard_D16_v5"
AKS_CLUSTER_NODE_COUNT = 4

KUBECTL_BIN = join(PROJ_ROOT, "bin", "kubectl")
