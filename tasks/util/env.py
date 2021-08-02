from os.path import dirname, realpath, join

PROJ_ROOT = dirname(dirname(dirname(realpath(__file__))))
FAASM_DIR = "{}/faasm".format(PROJ_ROOT)

AZURE_RESOURCE_GROUP = "faasm"
AZURE_REGION = "eastus"

AZURE_STORAGE_SKU = "Standard_LRS"
AZURE_VM_SIZE = "Standard_DS2_v2"

AKS_CLUSTER_NAME = "faasm-cluster"
AKS_CLUSTER_NODE_COUNT = 2

KUBECTL_BIN = join(PROJ_ROOT, "bin", "kubectl")
