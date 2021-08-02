from faasmcli.tasks import ns as faasm_ns
from invoke import Collection

from . import cluster
from . import container
from . import covid
from . import storage

ns = Collection(
    cluster,
    container,
    covid,
    storage,
)

ns.add_collection(faasm_ns, name="faasm")
