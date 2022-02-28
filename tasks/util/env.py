from os.path import dirname, realpath, join

PROJ_ROOT = dirname(dirname(dirname(realpath(__file__))))

BIN_DIR = join(PROJ_ROOT, "bin")
GLOBAL_BIN_DIR = "/usr/local/bin"

AZURE_RESOURCE_GROUP = "faasm"
AZURE_REGION = "eastus"

AZURE_STORAGE_SKU = "Standard_LRS"

KUBECTL_BIN = join(PROJ_ROOT, "bin", "kubectl")

AZURE_PUB_SSH_KEY = "~/.ssh/id_rsa.pub"
AZURE_SSH_KEY = "~/.ssh/id_rsa"

# ----------------------------
# VM SIZING NOTES
#
# For hacking around, the standard A-series VMs are fine (although very slow)
# https://docs.microsoft.com/en-us/azure/virtual-machines/av2-series
#
# e.g. Standard_A8_v2: 8 cores, 16GB mem
#
# For something a little faster, e.g. testing out experiment configurations,
# a smaller D-series VM works:
#
# e.g. Standard_D8_v5: 8 cores, 28GB mem
#
# For single VM benchmarks and cluster experiments, bigger D-series machines
# are more appropriate (but more expensive).
# https://docs.microsoft.com/en-us/azure/virtual-machines/dv3-dsv3-series
#
# e.g. Standard_D16_v5: 16 cores, 64GB mem
# e.g. Standard_D32_v5: 32 cores, 128GB mem
#
# ---------------------------

AZURE_VM_ADMIN = "faasm"
AZURE_VM_IMAGE = "Canonical:0001-com-ubuntu-server-focal:20_04-lts:latest"

AZURE_STANDALONE_VM_SIZE = "Standard_D8_v5"

AZURE_SGX_VM_IMAGE = "Canonical:UbuntuServer:18_04-lts-gen2:18.04.202109180"
AZURE_SGX_VM_SIZE = "Standard_DC2ds_v3"

# ----------------------------
# Azure Kubernetes Service (AKS) Cluster
# ----------------------------

AZURE_K8S_CLUSTER_NAME = "faasm-cluster"
AZURE_K8S_VM_SIZE = "Standard_D16_v5"
AZURE_K8S_NODE_COUNT = 4
AZURE_K8S_REGION = "eastus"
