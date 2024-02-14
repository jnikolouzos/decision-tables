from typing import Any

from pydantic import BaseModel

from schemas.decision_tables.constants import VARIABLE_PREFIX
from schemas.decision_tables.decision import Decision
from schemas.decision_tables.decision_table_type import DecisionTableType
from schemas.decision_tables.exceptions import DecisionTableException
from schemas.decision_tables.rule import Rule


# The root object that orchestrates all rules.
# It might have one of two types. Decision table or feature flag.
# When it's feature flag, it just returns the boolean value, so you can check if a feature should be enabled or not.
# In case of decision tables, it performs all nessesary checks and returns the decision that meets all conditions.
# Important: Rules are executed based on ordering, so order them properly. This happens because you might want to
# define a lot of sub-sets of conditions and if they are not met, to move up to a more abstract set of rules and end up
# with a final decision (if no rules are met, return "false")
class DecisionTable(BaseModel):
    table_id: str | None = None
    name: str
    decision_table_type: DecisionTableType = DecisionTableType.DECISION_TABLE
    rules: list[Rule]

    # The basic method that is executed for magic to happen.
    def execute(self, input_object: Any = None) -> Decision:
        if DecisionTableType.DECISION_TABLE == self.decision_table_type:
            return self.execute_decision_table(input_object)
        elif DecisionTableType.FEATURE_FLAG == self.decision_table_type:
            return self.check_feature_flag()
        raise DecisionTableException("No decision_table_type defined")

    # This method is the execution of decision tables.
    def execute_decision_table(self, input_object) -> Decision:
        self.rules.sort(key=lambda x: x.order, reverse=False)
        for rule in self.rules:
            if rule.apply(input_object):
                return update_decision_value(rule.decision, input_object)
        raise DecisionTableException("No rules met")

    # This method is the execution of decision tables.
    def check_feature_flag(self) -> Decision:
        return self.rules[0].decision


# If the decision has a variable as return value, it replaces the variable name with the actual value.
def update_decision_value(decision: Decision, input_object: Any) -> Decision:
    if str(decision.value).startswith(VARIABLE_PREFIX):
        decision.value = getattr(input_object, decision.value.replace(VARIABLE_PREFIX, ''))
    return decision
