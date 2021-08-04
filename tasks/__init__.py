from faasmcli.tasks import ns as faasm_ns
from invoke import Collection

from . import cluster
from . import covid
from . import storage

ns = Collection(
    cluster,
    covid,
    storage,
)

ns.add_collection(faasm_ns, name="faasm")
