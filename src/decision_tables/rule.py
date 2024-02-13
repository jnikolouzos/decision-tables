from pydantic import BaseModel

from decision_tables.condition import Condition
from decision_tables.decision import Decision


# A rule is the entity that binds a set of conditions and the decision if all of them are true.
class Rule(BaseModel):
    table_id: int | None = None
    rule_id: int | None = None
    name: str | None = None
    order: int | None = 999999  # the last rule to be executed
    decision: Decision
    conditions: list[Condition]

    # The method that executes all conditions and checks if all of them are true.
    def apply(self, input_object) -> bool:
        for condition in self.conditions:
            if not condition.check(input_object):
                return False
        return True
