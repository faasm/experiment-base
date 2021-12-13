from invoke import Collection

from . import cluster
from . import covid
from . import kernels
from . import lammps
from . import monitor
from . import storage
from . import uk8s

ns = Collection(
    cluster,
    covid,
    kernels,
    lammps,
    monitor,
    storage,
    uk8s,
)
