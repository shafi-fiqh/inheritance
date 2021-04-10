"""
Testing module
"""
import copy
import json

from src.cases_generator import CaseGenerator
from src.full_solver import full_solver
from src.solver import solve
from utils.helpers import calculate_asl


def pytest_generate_tests(metafunc):
    """
    Load the cases in the config
    :return: list of cases
    """
    with open("config/cases.json", "r") as cases_file:
        cases = json.load(cases_file)
    metafunc.parametrize("case", cases)


def test_cases(case):
    """
    Test that the solver returns expected results.
    Cases can be added to the cases.json file.
    Asaba should receive "U", third of remainder is '1/3 remainder'
    Rest are fractions in double quotes or the integer 0 without quotes.
    :return:
    """
    casegen = CaseGenerator(
        "config/family_config.csv", filter="config/filter.yml", filter_bool=False
    )
    case_copy = copy.deepcopy(case)

    for inh in case_copy["initial_shares"]:
        case_copy["initial_shares"][inh] = "0"

    initial_shares_solution = solve(
        case=case_copy["initial_shares"],
        descendants=casegen.descendants,
        mahjoob=casegen.mahjoob,
        rank=casegen.rank,
        taseeb=casegen.taseeb,
    )

    assert all(
        [
            case["initial_shares"][inh] == initial_shares_solution[inh]
            for inh in case["initial_shares"]
        ]
    ), "Case %s failed solver returned %s" % (
        case["initial_shares"],
        initial_shares_solution,
    )


def test_full_solver_cases(case):
    """
    Test that the full solver returns expected results.
    Cases can be added to the cases.json file.
    :return:
    """
    casegen = CaseGenerator(
        "config/family_config.csv", filter="config/filter.yml", filter_bool=False
    )
    case_copy = copy.deepcopy(case)

    initial_shares_solution = solve(
        case=case_copy["initial_shares"],
        descendants=casegen.descendants,
        mahjoob=casegen.mahjoob,
        rank=casegen.rank,
        taseeb=casegen.taseeb,
    )

    asba_radd_copy = copy.copy(initial_shares_solution)
    asba_radd_copy = full_solver(asba_radd_copy)
    full_shares_solution = calculate_asl(asba_radd_copy)

    assert all(
        [
            case["full_shares"][inh] == full_shares_solution[inh]
            for inh in case["full_shares"]
        ]
    ), "Case %s failed solver returned %s" % (case["full_shares"], full_shares_solution)
