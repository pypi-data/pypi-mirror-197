from typing import TYPE_CHECKING, Any, Callable, Dict

if TYPE_CHECKING:
    from sqlalchemy.types import TypeEngine

    from .schema import Column


def asUDF(output_type: "TypeEngine", *parameters: "Column"):
    """Decorate a function to be usable as a UDF."""

    def decorator(func: Callable):
        return UDF(func, output_type, *parameters)

    return decorator


class UDF:
    """A wrapper class for UDFs to be used in custom signal generation."""

    def __init__(
        self, func: Callable, output_type: "TypeEngine", *parameters: "Column"
    ):
        self.func = func
        self.output_type = output_type
        self.parameters = parameters

    def __call__(
        self, row: Dict[str, Any]
    ) -> Any:  # accepting sqlalchemy Rows as dicts
        params = [row[col.name] for col in self.parameters]
        return self.func(*params)
