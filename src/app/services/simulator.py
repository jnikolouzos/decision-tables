from typing import Any

from app.services import decision_tables_handler
from schemas.decision_tables.constants import EXPECTED_RESULT


def simulate_decision_table(input_object: Any):
    result = decision_tables_handler.execute_decision_table(input_object.table_id, input_object)
    input_object = input_object._replace(result=result.value)
    assertion = str(getattr(input_object, EXPECTED_RESULT)) == str(result.value)
    input_object = input_object._replace(assertion=assertion)
    return input_object