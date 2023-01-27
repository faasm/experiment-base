from invoke import Collection

from . import cluster
from . import format_code
from . import k8s
from . import monitor
from . import storage
from . import uk8s
from . import vm

ns = Collection(
    cluster,
    format_code,
    k8s,
    monitor,
    storage,
    uk8s,
    vm,
)
