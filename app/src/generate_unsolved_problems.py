import json
import itertools
import pandas as pd
import tqdm

from utils.helpers import is_redundant
from utils.helpers import nCr

"""
Generate all possible inheritance scenarios. Consumes a list of all possible
inheritors, list of inheritors that need to be there, list of inheritors that
need to be ignored and the total number of inheritors in a given problem
:param inheritors: List of all possible inheritors
:param must_haves: List of inheritors that the user wants included in all problems
:param not_haves: List of inheritors that the user wants ignored in all problems
:param n_types: number of distinct different types of inheritors.
For example Daughter + Son is considered 2 types.
Daugher x 2 + Son is still considered n_types = 2.
:return: List of JSON objects consisting of inheritance cases to be solved
"""
def generate_problems_lst(inheritors:list, must_haves: list, not_haves: list, n_types: int):
    inheritors = [
        inh
        for inh in inheritors
        if inh not in not_haves and inh not in must_haves
    ]

    generator = itertools.combinations(inheritors, n_types - len(must_haves))
    total_cases = []

    for case in tqdm.tqdm(
        generator,
        total=nCr(n=len(inheritors), r=n_types - len(must_haves)),
    ):
        case = case + tuple(must_haves)
        case = {x: "0" for x in case}
        total_cases.append(case)
    return json.dumps(total_cases)
