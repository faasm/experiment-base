from os.path import dirname, realpath, join

PROJ_ROOT = dirname(dirname(dirname(realpath(__file__))))

BIN_DIR = join(PROJ_ROOT, "bin")
GLOBAL_BIN_DIR = "/usr/local/bin"

AZURE_RESOURCE_GROUP = "faasm"
AZURE_REGION = "eastus"

AZURE_STORAGE_SKU = "Standard_LRS"
AKS_CLUSTER_NAME = "faasm-cluster"

KUBECTL_BIN = join(PROJ_ROOT, "bin", "kubectl")

# ----------------------------
# VM SIZING NOTES
#
# For hacking around, the standard A-series VMs are fine.
# https://docs.microsoft.com/en-us/azure/virtual-machines/av2-series
#
# e.g. Standard_A8_v2: 8 cores, 16GB mem
#
# For single VM benchmarks and cluster experiments, the D-series machines are
# more appropriate as they use higher grade CPUs.
# https://docs.microsoft.com/en-us/azure/virtual-machines/dv3-dsv3-series
#
# e.g. Standard_D16_v2: 16 cores, 64GB mem
# e.g. Standard_D32_v3: 32 cores, 128GB mem

AZURE_VM_ADMIN = "faasm"
AZURE_VM_IMAGE = "UbuntuLTS"
AZURE_STANDALONE_VM_SIZE = "Standard_A8_v2"
AZURE_K8S_VM_SIZE = "Standard_D16_v5"
AKS_CLUSTER_NODE_COUNT = 4

