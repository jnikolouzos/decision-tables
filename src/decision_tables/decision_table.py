from typing import Any

from pydantic import BaseModel

from decision_tables import decision_table_type
from decision_tables.constants import VARIABLE_PREFIX
from decision_tables.decision import Decision
from decision_tables.decision_table_type import DecisionTableType
from decision_tables.exceptions import DecisionTableException
from decision_tables.rule import Rule


class DecisionTable(BaseModel):
    table_id: str | None = None
    name: str
    decision_table_type: DecisionTableType = DecisionTableType.DECISION_TABLE
    rules: list[Rule]

    def execute(self, input_object: Any = None) -> Decision:
        if DecisionTableType.DECISION_TABLE == self.decision_table_type:
            return self.execute_decision_table(input_object)
        elif DecisionTableType.FEATURE_FLAG == self.decision_table_type:
            return self.check_feature_flag()
        raise DecisionTableException("No decision_table_type defined")

    def execute_decision_table(self, input_object) -> Decision:
        self.rules.sort(key=lambda x: x.order, reverse=False)
        for rule in self.rules:
            if rule.apply(input_object):
                return update_decision_value(rule.decision, input_object)
        raise DecisionTableException("No rules met")

    def check_feature_flag(self) -> Decision:
        return self.rules[0].decision


def update_decision_value(decision: Decision, input_object: Any) -> Decision:
    if str(decision.value).startswith(VARIABLE_PREFIX):
        decision.value = getattr(input_object, decision.value.replace(VARIABLE_PREFIX, ''))
    return decision
