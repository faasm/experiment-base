from os.path import dirname, realpath, join

PROJ_ROOT = dirname(dirname(dirname(realpath(__file__))))

BIN_DIR = join(PROJ_ROOT, "bin")
GLOBAL_BIN_DIR = "/usr/local/bin"

K9S_VERSION = "0.31.9"

ANSIBLE_DIR = join(PROJ_ROOT, "ansible")
INVENTORY_DIR = join(ANSIBLE_DIR, "inventory")
INVENTORY_FILE = join(INVENTORY_DIR, "vms.ini")

AZURE_RESOURCE_GROUP = "faasm"
AZURE_REGION = "eastus"
AZURE_ACR_NAME = "faasm.azurecr.io"

AZURE_STORAGE_SKU = "Standard_LRS"

KUBECTL_BIN = join(PROJ_ROOT, "bin", "kubectl")
KUBECTL_REMOTE_PORT = 16443
K8S_INGRESS_PORT = 80

# See k8s docs for default nodeport range
# https://kubernetes.io/docs/concepts/services-networking/service/#type-nodeport
K8S_NODEPORT_RANGE = "30000-32767"

AZURE_PUB_SSH_KEY = "~/.ssh/id_rsa.pub"
AZURE_SSH_KEY = "~/.ssh/id_rsa"

FAASM_UPLOAD_PORT = 8002
FAASM_INVOKE_PORT = 8080

# ----------------------------
# VM SIZING NOTES
#
# For hacking around, the standard A-series VMs are fine (although very slow)
# https://docs.microsoft.com/en-us/azure/virtual-machines/av2-series
#
# e.g. Standard_A8_v2: 8 vCPUs, 16GiB
#
# For something a little faster, e.g. testing out experiment configurations,
# a smaller D-series VM works:
#
# e.g. Standard_D8_v5: 8 vCPUs, 28GiB
#
# For single VM benchmarks and cluster experiments, bigger D-series machines
# are more appropriate, BUT, they use hyperthreading and native MT benchmarks
# will not scale smoothly on hyperthreaded cores:
#
# e.g. Standard_D16_v5: 16 vCPUs, 64GiB
# e.g. Standard_D32_v5: 32 vCPUs, 128GiB
#
# Links:
# - D-series:
#       https://docs.microsoft.com/en-us/azure/virtual-machines/dv5-dsv5-series
#
# VM Images: to upgrade a VM image, you can use the following command to check
# for the latest image version available
# az vm image list --all --publisher Canonical \
#   | jq '[.[] | select(.sku=="22_04-lts-gen2")] | max_by(.version)'
# ---------------------------

AZURE_VM_ADMIN = "faasm"
AZURE_VM_IMAGE = "Canonical:0001-com-ubuntu-server-focal:20_04-lts:latest"
AZURE_VM_IMAGE = (
    "Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:22.04.202301140"
)
AZURE_VM_OS_DISK_SIZE = "63"

AZURE_STANDALONE_VM_SIZE = "Standard_DS5_v2"

AZURE_SGX_VM_IMAGE = (
    "Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:22.04.202301140"
)
AZURE_SGX_VM_SIZE = "Standard_DC8ds_v3"

# ----------------------------
# Azure Kubernetes Service (AKS) Cluster
# ----------------------------

AZURE_K8S_CLUSTER_NAME = "faasm-cluster"
AZURE_K8S_VM_SIZE = "Standard_DS5_v2"
AZURE_K8S_NODE_COUNT = 4
AZURE_K8S_REGION = "eastus"
