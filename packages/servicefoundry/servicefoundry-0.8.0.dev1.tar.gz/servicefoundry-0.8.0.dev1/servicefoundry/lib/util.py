import os
from typing import TypeVar

from servicefoundry.lib.const import (
    SFY_DEBUG_ENV_KEY,
    SFY_EXPERIMENTAL_ENV_KEY,
    SFY_INTERNAL_ENV_KEY,
)

# TODO: Move type casting downwards into `ServiceFoundrySession` and `ServiceFoundryServiceClient`
# TODO: Abstract duplicated code across resolving different entities
T = TypeVar("T")


def is_debug_env_set() -> bool:
    return True if os.getenv(SFY_DEBUG_ENV_KEY) else False


def is_experimental_env_set() -> bool:
    # TODO (chiragjn): one of these need to be removed
    return (
        True
        if os.getenv(SFY_EXPERIMENTAL_ENV_KEY) or os.getenv(SFY_INTERNAL_ENV_KEY)
        else False
    )
