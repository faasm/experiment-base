from invoke import Collection

from . import cluster
from . import monitor
from . import storage
from . import uk8s

ns = Collection(
    cluster,
    monitor,
    storage,
    uk8s,
)
