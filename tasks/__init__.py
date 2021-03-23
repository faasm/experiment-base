from faasmcli.tasks import ns as faasm_ns
from invoke import Collection

from . import azure
from . import container

ns = Collection(
    azure,
    container,
)

ns.add_collection(faasm_ns, name="faasm")
