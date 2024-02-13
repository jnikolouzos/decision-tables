import os

from decision_tables import simulator
from decision_tables.constants import CSV
from test import virtual_db

# todo remove local path
SIMULATION_DIR = '../../simulations'


def test_generate_csv():
    generated_csv = simulator.generate_csv('check_asset_if_pd')
    expected_csv = 'title;writers;expected_result;result;assertion\n'
    expected_columns = set(sorted(expected_csv.split(';')))
    csv_columns = set(sorted(generated_csv.split(';')))
    assert (expected_columns == csv_columns)


def test_simulation(file_path: str, file_name: str):
    simulator.simulate_decision_table(file_path, file_name)


# Setup results dir
def setup_results_dir():
    results_path = os.path.join(SIMULATION_DIR, 'results')
    try:
        # delete all files
        for f in os.listdir(results_path):
            os.remove(os.path.join(results_path, f))
        # delete the directory
        os.removedirs(results_path)
    except FileNotFoundError:
        pass
    os.mkdir(results_path)


# Executes all simulation csv
def run_all_simulations():
    simulations = [f for f in os.listdir(SIMULATION_DIR) if f.endswith(CSV)]
    for simulation in simulations:
        test_simulation(SIMULATION_DIR, simulation)


if __name__ == "__main__":
    virtual_db.initialize_data()
    test_generate_csv()

    setup_results_dir()
    run_all_simulations()
