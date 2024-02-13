from decision_tables.condition import Condition
from decision_tables.decision import Decision
from decision_tables.decision_table import DecisionTable
from decision_tables.decision_table_type import DecisionTableType
from decision_tables.decision_type import DecisionType
from decision_tables.exceptions import DecisionTableException
from decision_tables.rule import Rule
from decision_tables.condition_type import ConditionType
from test import virtual_db

# todo this is a temporary wrapper of how to call basic function.
# we need to rewrite it when we have DB, etc


def execute_decision_table(table_id: str, input_object):
    if table_id in virtual_db.db:
        return virtual_db.db[table_id].execute(input_object)
    raise DecisionTableException(f"Table with id {table_id} does not exist")


def insert_decision_table(decision_table: DecisionTable):
    virtual_db.db[decision_table.table_id] = decision_table
    return decision_table


def update_decision_table(table_id: str, decision_table: DecisionTable):
    virtual_db.db[table_id] = decision_table
    return decision_table


def get_decision_table(table_id: str):
    if table_id in virtual_db.db:
        return virtual_db.db[table_id]
    return DecisionTableException(f"Table with id {table_id} does not exist")


def get_decision_tables():
    return virtual_db.db


def delete_decision_table(table_id):
    if table_id in virtual_db.db:
        virtual_db.db.pop(table_id)
        return f"Table with id {table_id} deleted successfully"
    raise DecisionTableException(f"Table with id {table_id} does not exist")


def create_feature_flag(table_name: int, value: bool = True):
    rules = list()
    conditions = list()
    conditions.append(Condition(rule_type=ConditionType.FINALLY, field="", value=""))
    rules.append(
        Rule(order=1, decision=Decision(decision_type=DecisionType.BOOLEAN, value=value), conditions=conditions))
    decision_table = DecisionTable(table_id=table_name, name=table_name, decision_table_type=DecisionTableType.FEATURE_FLAG, rules=rules)
    virtual_db.db[decision_table.table_id] = decision_table
    return decision_table


def check_feature_flag(table_id):
    if table_id in virtual_db.db:
        return virtual_db.db[table_id].execute().value
    raise DecisionTableException(f"Feature flag with id {table_id} does not exist")
