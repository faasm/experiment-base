from faasmcli.tasks import ns as faasm_ns
from invoke import Collection

from . import azure
from . import container
from . import plot

ns = Collection(
    azure,
    container,
    plot,
)

ns.add_collection(faasm_ns, name="faasm")
