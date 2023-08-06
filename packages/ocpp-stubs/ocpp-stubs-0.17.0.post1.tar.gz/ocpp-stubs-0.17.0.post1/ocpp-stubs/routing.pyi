import sys

if sys.version_info >= (3, 10):
    from typing import Callable, ParamSpec, TypeVar
else:
    from typing_extensions import Callable, ParamSpec, TypeVar

from ocpp.v16.enums import Action as V16Action
from ocpp.v201.enums import Action as V201Action

P = ParamSpec("P")
T = TypeVar("T")

# This returns a function decorator that has the same type as the decorated function.
# The returned function will have the same argument types and return value,
# this is why ParamSpec and TypeVar are used.
def on(
    action: V16Action | V201Action,
    *,
    skip_schema_validation: bool = False,
) -> Callable[[Callable[P, T]], Callable[P, T]]: ...

def after(action: V16Action | V201Action) -> Callable[[Callable[P, T]], Callable[P, T]]: ...
