from pydantic import BaseModel

from decision_tables.rule_type import RuleType
from decision_tables.constants import VARIABLE_PREFIX, COMMA, DOT, CHARACTERS_TO_REPLACE_WITH_SPACE, SPACE


class Condition(BaseModel):
    table_id: str | None = None
    condition_id: int | None = None
    rule_type: RuleType
    field: str | None = ''
    value: str | None = ''

    def check(self, input_object) -> bool:
        # I don't need to check anything. Just return True so the rule can return the final value
        if self.rule_type == RuleType.FINALLY:
            return True
        input_value = self.get_input_value(input_object)
        check_value = self.value
        if self.value.startswith(VARIABLE_PREFIX):
            check_value = getattr(input_object, self.value.replace(VARIABLE_PREFIX, ''))
        if self.rule_type == RuleType.EQUAL:
            return str(input_value) == str(check_value)
        elif self.rule_type == RuleType.GREATER:
            return input_value > check_value
        elif self.rule_type == RuleType.GREATER_EQUAL:
            return input_value >= check_value
        elif self.rule_type == RuleType.LESS:
            return input_value < check_value
        elif self.rule_type == RuleType.LESS_EQUAL:
            return input_value <= check_value
        elif self.rule_type == RuleType.NOT_EQUAL:
            return input_value != check_value
        elif self.rule_type == RuleType.CONTAINS:
            return format_str(check_value) in clean_up_str(input_value)
        elif self.rule_type == RuleType.CONTAINS_ANY_OF:
            check_word_in_list = lambda input_string, word_list: any(word in word_list for word in input_string.split())
            return check_word_in_list(clean_up_str(input_value), format_str(check_value).split(COMMA))
        elif self.rule_type == RuleType.DOES_NOT_CONTAIN:
            return format_str(check_value) not in clean_up_str(input_value)
        elif self.rule_type == RuleType.STARTS_WITH:
            return clean_up_str(input_value).startswith(format_str(check_value))
        elif self.rule_type == RuleType.ENDS_WITH:
            return clean_up_str(input_value).endswith(format_str(check_value))
        elif self.rule_type == RuleType.BEFORE:
            return input_value < check_value
        elif self.rule_type == RuleType.AFTER:
            return input_value > check_value
        elif self.rule_type == RuleType.IN_LIST:
            return input_value in check_value.split(COMMA)
        elif self.rule_type == RuleType.NOT_IN_LIST:
            return input_value not in check_value.split(COMMA)
        elif self.rule_type == RuleType.NONE:
            return input_value is None
        elif self.rule_type == RuleType.NOT_NONE:
            return input_value is not None
        return False

    def get_input_value(self, input_object):
        child_object = input_object
        if DOT in self.field:
            for node in self.field.split(DOT):
                child_object = getattr(child_object, node)
            return child_object
        return getattr(input_object, self.field)


# todo I have concerns iw we should clean up the input or not
# It makes it easy to match what we need, but we alter the raw data
# Having them cleaned is not an option because all these characters
# that we remove for comparison are needed in order to be readable
def clean_up_str(input_str):
    for char in CHARACTERS_TO_REPLACE_WITH_SPACE:
        input_str = input_str.replace(char, SPACE)
    return format_str(input_str)


def format_str(input_str):
    return str(input_str.replace('"', '')).lower().strip()
