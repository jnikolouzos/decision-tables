from decision_tables.condition import Condition
from decision_tables.decision import Decision
from decision_tables.decision_table import DecisionTable
from decision_tables.decision_type import DecisionType
from decision_tables.rule import Rule
from decision_tables.rule_type import RuleType


def public_domain_decision_table():
    rules = list()

    classical_writers = Condition(rule_type=RuleType.CONTAINS_ANY_OF, field='writers', value='Mozart,Beethoven,Bach,Strauss,Verdi,Puccini,Chopin,Wagner,Tchaikovsky,Vivaldi,Brahms,Schubert,Rachmaninoff')
    rules.append(Rule(order=2, decision=Decision(decision_type=DecisionType.BOOLEAN, value=True), conditions=[classical_writers]))

    trad_pd_dp = Condition(rule_type=RuleType.CONTAINS_ANY_OF, field='title', value='Trad,PD,DP')
    rules.append(Rule(order=1, decision=Decision(decision_type=DecisionType.BOOLEAN, value=True), conditions=[trad_pd_dp]))

    finally_condition = Condition(rule_type=RuleType.FINALLY)
    rules.append(Rule(decision=Decision(decision_type=DecisionType.BOOLEAN, value=False), conditions=[finally_condition]))

    return DecisionTable(table_id='check_asset_if_pd', name='Check if asset is Public Domain', rules=rules)


def remix_decision_table_contains_any_of():
    rules = list()

    remix = Condition(rule_type=RuleType.CONTAINS_ANY_OF, field='title', value='mix,remix')
    rules.append(Rule(order=1, decision=Decision(decision_type=DecisionType.BOOLEAN, value=True), conditions=[remix]))

    finally_condition = Condition(rule_type=RuleType.FINALLY)
    rules.append(Rule(decision=Decision(decision_type=DecisionType.BOOLEAN, value=False), conditions=[finally_condition]))

    return DecisionTable(table_id='check_asset_if_remix_contains_any_of', name='Check if asset is Remix', rules=rules)


def remix_decision_table_contains():
    rules = list()

    remix = Condition(rule_type=RuleType.CONTAINS, field='title', value='mix')
    rules.append(Rule(order=1, decision=Decision(decision_type=DecisionType.BOOLEAN, value=True), conditions=[remix]))

    finally_condition = Condition(rule_type=RuleType.FINALLY)
    rules.append(Rule(decision=Decision(decision_type=DecisionType.BOOLEAN, value=False), conditions=[finally_condition]))

    return DecisionTable(table_id='check_asset_if_remix_contains', name='Check if asset is Remix', rules=rules)
