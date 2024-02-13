from enum import Enum


# The different types of conditions available to build the rules.
class ConditionType(Enum):
    EQUAL = 1  # simple equality check
    GREATER = 2  # if the input value is greater than comparison value
    GREATER_EQUAL = 3  # if the input value is greater or equal to the comparison value
    LESS = 4   # if the input value is less than comparison value
    LESS_EQUAL = 5  # if the input value is less or equal to comparison value
    NOT_EQUAL = 6  # if the input value is not equal to comparison value
    CONTAINS = 7  # if the input string value contains comparison value
    CONTAINS_ANY_OF = 8  # if the input string value contains any of the values in comparison value list
    DOES_NOT_CONTAIN = 9  # if the input string value does not contain the comparison value
    STARTS_WITH = 10  # if the input string value starts with comparison value
    ENDS_WITH = 11  # if the input string value ends with comparison value
    BEFORE = 12  # if the input date value is before the comparison value
    AFTER = 13  # if the input date value is after the comparison value
    IN_LIST = 14  # if the input value is in comparison value list
    NOT_IN_LIST = 15  # if the input value is not in comparison value list
    NONE = 16  # if the input value is None
    NOT_NONE = 17  # if the input value is not None
    FINALLY = 18  # This is always true. It can be used if no rules met. If you don't use it and no rule is true, it will throw an error
