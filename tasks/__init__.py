from invoke import Collection

from . import azure
from . import container
from . import knative

ns = Collection(
    azure,
    container,
    knative,
)
