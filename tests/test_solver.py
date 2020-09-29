"""
Testing module
"""
import copy
import json
import pytest

from src.cases_generator import CaseGenerator
from src.solver import solve


def pytest_generate_tests(metafunc):
    """
    Load the cases in the config
    :return: list of cases
    """
    with open('config/cases.json', 'r') as cases_file:
        cases = json.load(cases_file)
    metafunc.parametrize('case', cases)


def test_cases(case):
    """
    Test that the solver returns expected results.
    Cases can be added to the cases.json file.
    Asaba should receive "A", third of remainder is '1/3 remainder'
    Rest are fractions in double quotes or the integer 0 without quotes.
    :return:
    """
    casegen = CaseGenerator('config/family_config.csv')
    case_copy = copy.copy(case)
    assert all([case[inh] == solve(case=case_copy,
                                   descendants=casegen.descendants,
                                   mahjoob=casegen.mahjoob,
                                   rank=casegen.rank,
                                   taseeb=casegen.taseeb)[inh]
                for inh in case]), \
        'Case %s failed solver returned %s' % (case, case_copy)
