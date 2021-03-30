from faasmcli.tasks import ns as faasm_ns
from invoke import Collection

from . import azure
from . import container
from . import covid

ns = Collection(
    azure,
    container,
    covid,
)

ns.add_collection(faasm_ns, name="faasm")
