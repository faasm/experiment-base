from invoke import Collection

from . import batch
from . import cluster
from . import k8s
from . import monitor
from . import storage
from . import uk8s
from . import vm

ns = Collection(
    batch,
    cluster,
    k8s,
    monitor,
    storage,
    uk8s,
    vm,
)
