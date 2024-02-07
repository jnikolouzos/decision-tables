from decision_tables import decision_tables_handler
from decision_tables.condition import Condition
from decision_tables.decision_type import DecisionType
from decision_tables.exceptions import DecisionTableException
from decision_tables.rule_type import RuleType
from test import virtual_db
from test.recording import Recording

# todo delete me. This is not a test, it's a way for me to call the flow that I need during development.


def print_decision():
    return "with method call"


def test_nested():
    field = "foo.bar.beer.title"
    person = Recording(name="jim", age=38, expected_age=0)
    c = Condition(rule_type=RuleType.EQUAL, field=field, value="A title")
    result = c.get_input_value(person)
    assert c.check(person)
    assert (result == "A title")


def test_contains_any_of():
    c = Condition(rule_type=RuleType.CONTAINS_ANY_OF, field="name", value="foo,bar,beer")
    person = Recording(name="My name is jim and i own a bar that sells whiskey", age=38, expected_age=0)
    assert c.check(person)


if __name__ == "__main__":
    virtual_db.initialize_data()
    dt = decision_tables_handler.get_decision_table('1')
    result = decision_tables_handler.create_feature_flag("matching_app.standalone.enable", value=True)
    assert result.execute().value
    result = decision_tables_handler.create_feature_flag("matching_app.standalone.enable", value=False)
    assert not result.execute().value

    print("done")
