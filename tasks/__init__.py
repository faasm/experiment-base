from invoke import Collection

from . import cluster
from . import covid
from . import lammps
from . import storage
from . import uk8s

ns = Collection(
    cluster,
    covid,
    lammps,
    storage,
    uk8s,
)
