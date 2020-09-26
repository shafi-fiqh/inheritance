"""
Testing module
"""
import copy
import pytest
import json

from src.cases_generator import CaseGenerator
from src.solver import solve

def test_cases():
    with open('config/cases.json', 'r') as cases_file:
        cases = json.load(cases_file)
    casegen = CaseGenerator('config/family_config.csv')
    print('cases = ', cases)
    for case in cases:
        case_copy = copy.copy(case)
        assert all([case[inh] == solve(case=case_copy,
                                       descendants=casegen.descendants,
                                       mahjoob=casegen.mahjoob,
                                       rank=casegen.rank,
                                       taseeb=casegen.taseeb)[inh] for inh in case]), 'Case %s failed solver returned %s' % (case, case_copy)

