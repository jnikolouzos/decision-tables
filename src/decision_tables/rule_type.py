from enum import Enum


class RuleType(Enum):
    EQUAL = 1
    GREATER = 2
    GREATER_EQUAL = 3
    LESS = 4
    LESS_EQUAL = 5
    NOT_EQUAL = 6
    CONTAINS = 7
    CONTAINS_ANY_OF = 8
    DOES_NOT_CONTAIN = 9
    STARTS_WITH = 10
    ENDS_WITH = 11
    BEFORE = 12
    AFTER = 13
    IN_LIST = 14
    NOT_IN_LIST = 15
    NONE = 16
    NOT_NONE = 17
    FINALLY = 18
