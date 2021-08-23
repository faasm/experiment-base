from invoke import Collection

from . import cluster
from . import covid
from . import lammps
from . import storage

ns = Collection(
    cluster,
    covid,
    lammps,
    storage,
)
