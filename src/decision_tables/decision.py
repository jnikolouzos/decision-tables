from typing import Any

from pydantic import BaseModel

from decision_tables.decision_type import DecisionType


# The decision that is returned when all conditions of a rule are met.
# The decision has a type so that the caller will know how to handle the returned value.
# For example, we might have numeric, boolean, string or even a method name or code snippet.
# Of course, primitive types are safer that method names and snippets. They can cause interesting errors on runtime.
class Decision(BaseModel):
    table_id: str | None = None
    decision_id: int | None = None
    decision_type: DecisionType
    value: Any
