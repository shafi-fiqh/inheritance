"""
Testing module
"""
import pytest
import json

from src.cases_generator import CaseGenerator
from src.solver import solve

def test_cases():
    with open('config/cases.json', 'r') as cases_file:
        cases = json.load(cases_file)
    casegen = CaseGenerator('config/family_config.csv')
    for case in cases:
        assert all([case[inh] == solve(case=case,
                                       descendants=casegen.descendants,
                                       mahjoob=casegen.mahjoob,
                                       rank=casegen.rank,
                                       taseeb=casegen.taseeb)[inh] for inh in case]), 'Case %s failed' % case

