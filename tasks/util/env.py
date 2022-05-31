from os.path import dirname, realpath, join

PROJ_ROOT = dirname(dirname(dirname(realpath(__file__))))

BIN_DIR = join(PROJ_ROOT, "bin")
GLOBAL_BIN_DIR = "/usr/local/bin"

# Note - this must match the version used by Faasm
KNATIVE_VERSION = "1.1.0"
K9S_VERSION = "0.24.15"

ANSIBLE_DIR = join(PROJ_ROOT, "ansible")
INVENTORY_DIR = join(ANSIBLE_DIR, "inventory")
INVENTORY_FILE = join(INVENTORY_DIR, "vms.ini")

AZURE_RESOURCE_GROUP = "faasm"
AZURE_REGION = "eastus"

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
# Non-hyper-threaded machines include older D-series and newer H-series
# machines:
#
# e.g. Standard_H16: 16 vCPUs, 112GiB
# e.g. Standard_D5_v2: 16 vCPUs, 56GiB
#
# Links:
# - Newer D-series: https://docs.microsoft.com/en-us/azure/virtual-machines/dv5-dsv5-series
# - Older D-series (no HT): https://docs.microsoft.com/en-us/azure/virtual-machines/dv2-dsv2-series
# - H-series (no HT): https://docs.microsoft.com/en-us/azure/virtual-machines/h-series
# ---------------------------

AZURE_VM_ADMIN = "faasm"
AZURE_VM_IMAGE = "Canonical:0001-com-ubuntu-server-focal:20_04-lts:latest"

AZURE_STANDALONE_VM_SIZE = "Standard_DS5_v2"

AZURE_SGX_VM_IMAGE = "Canonical:UbuntuServer:18_04-lts-gen2:18.04.202109180"
AZURE_SGX_VM_SIZE = "Standard_DC4ds_v3"

# ----------------------------
# Azure Kubernetes Service (AKS) Cluster
# ----------------------------

AZURE_K8S_CLUSTER_NAME = "faasm-cluster"
AZURE_K8S_VM_SIZE = "Standard_DS5_v2"
AZURE_K8S_NODE_COUNT = 4
AZURE_K8S_REGION = "eastus"
