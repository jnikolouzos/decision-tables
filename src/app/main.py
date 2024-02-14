from fastapi import FastAPI

from schemas.decision_tables.decision_table import DecisionTable
from tests.mocking.recording import Recording
from tests.mocking.virtual_db import initialize_data
from app.services import decision_tables_handler

app = FastAPI()
initialize_data()


@app.post("/execute-decision-table")
def execute_decision_table(table_id: str, recording: Recording):
    return decision_tables_handler.execute_decision_table(table_id, recording)


@app.get("/check-feature-flag/{table_id}")
def check_feature_flag(table_id: str):
    return decision_tables_handler.check_feature_flag(table_id)


@app.get("/get-all-decision-tables")
def get_all_decision_tables():
    return decision_tables_handler.get_all_decision_tables()


@app.get("/get-decision-table-ids")
def get_decision_table_ids():
    return decision_tables_handler.get_decision_table_ids()


@app.get("/get-feature-flag-ids")
def get_feature_flag_ids():
    return decision_tables_handler.get_feature_flag_ids()


@app.get("/get-decision-table/{table_id}")
def get_decision_table(table_id: str):
    return decision_tables_handler.get_decision_table(table_id)


@app.post("/insert-decision-table/")
def insert_decision_table(decision_table: DecisionTable):
    return decision_tables_handler.insert_decision_table(decision_table)


@app.put("/update-decision-table/{table_id}")
def update_decision_table(table_id: str, decision_table: DecisionTable):
    return decision_tables_handler.update_decision_table(table_id, decision_table)


@app.delete("/delete-decision-table/{table_id}")
def delete_decision_table(table_id: str):
    return decision_tables_handler.delete_decision_table(table_id)
