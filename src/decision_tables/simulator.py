import os
from collections import namedtuple
import csv

from decision_tables import decision_tables_handler
from decision_tables.constants import ASSERTION, RESULT, EXPECTED_RESULT, DELIMITER, LINE, CSV, SUFFIX, VARIABLE_PREFIX
from test import virtual_db

schema = []

# todo this files has poor design. It need a refactoring so that input, execution and output can be decoupled.
# In the future, we will want to pass files uploaded by UI and not local files.
# We might also need to show the results on UI table and not on a csv.


def append_to_result_csv(file_path, file_name: str, row):
    output_file_name = file_name.replace(CSV, '') + SUFFIX
    output_file = os.path.join(file_path, 'results', output_file_name)
    with open(output_file, 'a') as csv_file:
        csv_file.write(row)


def simulate_decision_table(file_path: str, file_name: str):
    data = parse_csv(file_path, file_name)
    for input_object in data:
        result = decision_tables_handler.execute_decision_table(input_object.table_id, input_object)
        input_object = input_object._replace(result=result.value)
        assertion = str(getattr(input_object, EXPECTED_RESULT)) == str(result.value)
        input_object = input_object._replace(assertion=assertion)
        write_result_row(file_path, file_name, input_object)


def write_result_row(file_path, file_name: str, input_object):
    row = ''
    for column in schema:
        row += str(getattr(input_object, column)) + DELIMITER
    row += LINE
    append_to_result_csv(file_path, file_name, row)


def parse_csv(file_path: str, file_name:str):
    with open(os.path.join(file_path, file_name), 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter=DELIMITER)
        header = next(reader)
        write_result_headers(file_path, file_name, header)
        Row = namedtuple('InputObject', header)
        data = [Row(*row) for row in reader]
    return data


def write_result_headers(file_path: str, file_name: str, header):
    header_row = ''
    # init the global variable in case of multiple calls
    globals()['schema'] = []
    for column in header:
        schema.append(column)
        header_row += column + DELIMITER
    header_row += LINE
    append_to_result_csv(file_path, file_name, header_row)


def generate_csv(table_id: str):
    dt = virtual_db.db[table_id]
    unique_attributes = get_unique_attributes(dt)
    csv_output = ''
    for attribute in unique_attributes:
        # In case of FINALLY we don't have a field name it will create empty column
        if attribute:
            csv_output += attribute + DELIMITER
    csv_output += EXPECTED_RESULT + DELIMITER + RESULT + DELIMITER + ASSERTION + LINE
    return csv_output


def get_unique_attributes(dt):
    attributes = []
    for rule in dt.rules:
        for condition in rule.conditions:
            attributes.append(condition.field)
            if condition.value.startswith(VARIABLE_PREFIX):
                attributes.append(condition.value.replace(VARIABLE_PREFIX, ''))
    unique_attributes = list(dict.fromkeys(attributes))
    return unique_attributes
