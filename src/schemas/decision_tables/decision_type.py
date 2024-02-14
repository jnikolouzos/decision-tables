from enum import Enum


# This is needed so the caller can now somehow how to use the result.
class DecisionType(Enum):
    STRING = 1
    METHOD_NAME = 2
    BOOLEAN = 3