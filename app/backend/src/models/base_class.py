import re
from typing import Any

from sqlalchemy.orm import as_declarative, declared_attr


@as_declarative()
class Base:
    id: Any
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        # CamelCase -> snake_case
        table_name = "_".join(re.split(r"(?<=\w)(?=[A-Z])", cls.__name__)).lower()
        # Adding 's' to form plural
        return f"{table_name}s"
