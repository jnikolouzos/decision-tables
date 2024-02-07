from pydantic import BaseModel

from decision_tables.condition import Condition
from decision_tables.decision import Decision


class Rule(BaseModel):
    table_id: int | None = None
    rule_id: int | None = None
    name: str | None = None
    order: int | None = 999999  # the last rule to be executed
    decision: Decision
    conditions: list[Condition]

    def apply(self, input_object) -> bool:
        for condition in self.conditions:
            if not condition.check(input_object):
                return False
        return True
