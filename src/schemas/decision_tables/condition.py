from pydantic import BaseModel

from schemas.decision_tables.condition_type import ConditionType
from schemas.decision_tables.constants import VARIABLE_PREFIX, COMMA, DOT, CHARACTERS_TO_REPLACE_WITH_SPACE, SPACE


# The condition that needs to be met in order to have a valid rule.
# The concept is that if you want to check if a person is adult, you create a condition like "age GREATER_EQUAL 18".
# Nested properties are also supported with dot notation i.e. "family.father.age"
# Dynamic values are also supported on the same input object. For example, you could have a condition like
# "person.age EQUAL $person.expected_age". $ is used to define that this value is dynamic
class Condition(BaseModel):
    id: int | None = None
    rule_type: ConditionType
    field: str | None = ''
    value: str | None = ''

    # The basic method that is executed to check a condition.
    def check(self, input_object) -> bool:
        # No need to check anything. Just return True so the rule can return the final value
        if self.rule_type == ConditionType.FINALLY:
            return True
        input_value = self.get_input_value(input_object)
        check_value = self.value
        if self.value.startswith(VARIABLE_PREFIX):
            check_value = self.get_value(input_object)
        if self.rule_type == ConditionType.EQUAL:
            return str(input_value) == str(check_value)
        elif self.rule_type == ConditionType.GREATER:
            return input_value > check_value
        elif self.rule_type == ConditionType.GREATER_EQUAL:
            return input_value >= check_value
        elif self.rule_type == ConditionType.LESS:
            return input_value < check_value
        elif self.rule_type == ConditionType.LESS_EQUAL:
            return input_value <= check_value
        elif self.rule_type == ConditionType.NOT_EQUAL:
            return input_value != check_value
        elif self.rule_type == ConditionType.CONTAINS:
            return format_str(check_value) in clean_up_str(input_value)
        elif self.rule_type == ConditionType.CONTAINS_ANY_OF:
            check_word_in_list = lambda input_string, word_list: any(word in word_list for word in input_string.split())
            return check_word_in_list(clean_up_str(input_value), format_str(check_value).split(COMMA))
        elif self.rule_type == ConditionType.DOES_NOT_CONTAIN:
            return format_str(check_value) not in clean_up_str(input_value)
        elif self.rule_type == ConditionType.STARTS_WITH:
            return clean_up_str(input_value).startswith(format_str(check_value))
        elif self.rule_type == ConditionType.ENDS_WITH:
            return clean_up_str(input_value).endswith(format_str(check_value))
        elif self.rule_type == ConditionType.BEFORE:
            return input_value < check_value
        elif self.rule_type == ConditionType.AFTER:
            return input_value > check_value
        elif self.rule_type == ConditionType.IN_LIST:
            return input_value in check_value.split(COMMA)
        elif self.rule_type == ConditionType.NOT_IN_LIST:
            return input_value not in check_value.split(COMMA)
        elif self.rule_type == ConditionType.NONE:
            return input_value is None
        elif self.rule_type == ConditionType.NOT_NONE:
            return input_value is not None
        return False

    def _get_dynamic_value(self, input_object, field_name):
        child_object = input_object
        field = getattr(self, field_name)
        if DOT in field:
            for node in field.split(DOT):
                child_object = getattr(child_object, node)
            return child_object
        return getattr(input_object, self.field)

    # Check if the input field is dot notated and return the value
    def get_input_value(self, input_object):
        return self._get_dynamic_value(input_object, "field")

    # Check if the value is dot notated and return the value
    def get_value(self, input_object):
        return self._get_dynamic_value(input_object, "value").replace(VARIABLE_PREFIX, '')


# todo I have concerns iw we should clean up the input or not
# It makes it easy to match what we need, but we alter the raw data
# Having them cleaned is not an option because all these characters
# that we remove for comparison are needed in order to be readable
def clean_up_str(input_str):
    for char in CHARACTERS_TO_REPLACE_WITH_SPACE:
        input_str = input_str.replace(char, SPACE)
    return format_str(input_str)


# It simplifies the string comparison,
def format_str(input_str):
    return str(input_str.replace('"', '')).lower().strip()
