from app.services import decision_tables_handler
from tests.mocking import samples

db = {}

# todo add a real db.


def initialize_data():
    pd = samples.public_domain_decision_table()
    db[pd.table_id] = samples.public_domain_decision_table()

    remix_contains = samples.remix_decision_table_contains()
    db[remix_contains.table_id] = remix_contains

    remix_contains_any = samples.remix_decision_table_contains_any_of()
    db[remix_contains_any.table_id] = remix_contains_any

    standalone_enable = decision_tables_handler.create_feature_flag("matching_app.standalone.flag", value=True)
    standalone_enable.table_id = standalone_enable.name
    db[standalone_enable.table_id] = standalone_enable

    standalone_disable = decision_tables_handler.create_feature_flag("matching_app.flagging.flag", value=False)
    standalone_disable.table_id = standalone_disable.name
    db[standalone_disable.table_id] = standalone_disable
