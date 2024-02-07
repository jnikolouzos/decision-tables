from typing import Any

from pydantic import BaseModel

from decision_tables.decision_type import DecisionType


class Decision(BaseModel):
    table_id: str | None = None
    decision_id: int | None = None
    decision_type: DecisionType
    value: Any
