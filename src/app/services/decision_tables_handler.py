from schemas.decision_tables.condition import Condition
from schemas.decision_tables.decision import Decision
from schemas.decision_tables.decision_table import DecisionTable
from schemas.decision_tables.decision_table_type import DecisionTableType
from schemas.decision_tables.decision_type import DecisionType
from schemas.decision_tables.exceptions import DecisionTableException
from schemas.decision_tables.rule import Rule
from schemas.decision_tables.condition_type import ConditionType
from tests.mocking import virtual_db


# todo this is a temporary wrapper of how to call basic function.
# we need to rewrite it when we have DB, etc


def execute_decision_table(table_id: str, input_object) -> Decision:
    if table_id in virtual_db.db:
        return virtual_db.db[table_id].execute(input_object)
    raise DecisionTableException(f"Table with id {table_id} does not exist")


def insert_decision_table(decision_table: DecisionTable) -> DecisionTable:
    virtual_db.db[decision_table.table_id] = decision_table
    return decision_table


def update_decision_table(table_id: str, decision_table: DecisionTable) -> DecisionTable:
    virtual_db.db[table_id] = decision_table
    return decision_table


def get_decision_table(table_id: str) -> DecisionTable:
    if table_id in virtual_db.db:
        return virtual_db.db[table_id]
    return DecisionTableException(f"Table with id {table_id} does not exist")


def get_all_decision_tables() -> dict[DecisionTable]:
    return virtual_db.db


def filter_decision_table_ids(decision_table_type: DecisionTableType):
    # filtered_objects = filter(lambda x: x.decision_table_type == decision_table_type, list(virtual_db.db))
    filtered_objects = dict(filter(lambda item: item[1].decision_table_type == decision_table_type, virtual_db.db.items()))
    return list(filtered_objects)


def get_decision_table_ids():
    return filter_decision_table_ids(DecisionTableType.DECISION_TABLE)


def get_feature_flag_ids():
    return filter_decision_table_ids(DecisionTableType.FEATURE_FLAG)


def delete_decision_table(table_id):
    if table_id in virtual_db.db:
        virtual_db.db.pop(table_id)
        return f"Table with id {table_id} deleted successfully"
    raise DecisionTableException(f"Table with id {table_id} does not exist")


def create_feature_flag(table_name: int, value: bool = True) -> DecisionTable:
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
