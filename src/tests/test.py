from app.services import decision_tables_handler
from schemas.decision_tables.condition import Condition
from schemas.decision_tables.condition_type import ConditionType
from tests.mocking import virtual_db
from tests.mocking.recording import Recording

# todo delete me. This is not a tests, it's a way for me to call the flow that I need during development.


def print_decision():
    return "with method call"


def test_nested():
    field = "foo.bar.beer.title"
    person = Recording(name="jim", age=38, expected_age=0)
    c = Condition(rule_type=ConditionType.EQUAL, field=field, value="A title")
    result = c.get_input_value(person)
    assert c.check(person)
    assert (result == "A title")


def test_contains_any_of():
    c = Condition(rule_type=ConditionType.CONTAINS_ANY_OF, field="name", value="foo,bar,beer")
    person = Recording(name="My name is jim and i own a bar that sells whiskey", age=38, expected_age=0)
    assert c.check(person)


if __name__ == "__main__":
    virtual_db.initialize_data()

    dt = decision_tables_handler.get_decision_table('check_asset_if_pd')
    pd_song = Recording(title='Requiem', artists='Wiener Philharmoniker, Bruno Walter', writers='Wolfgang Amadeus Mozart')
    assert dt.execute(pd_song).value
    non_pd_song = Recording(title='Hello', artists='Adele', writers='Adele,Greg Kurstin')
    assert not dt.execute(non_pd_song).value

    result = decision_tables_handler.create_feature_flag("matching_app.standalone.flag", value=True)
    assert result.execute().value
    result = decision_tables_handler.create_feature_flag("matching_app.flagging.flag", value=False)
    assert not result.execute().value

    print("done")
