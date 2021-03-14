import json
import itertools
import pandas as pd
import tqdm

from utils.helpers import is_redundant
from utils.helpers import nCr


def generate_problems_lst(
    inheritors: list, must_haves: list, not_haves: list, n_types: int
):
    inheritors = [
        inh for inh in inheritors if inh not in not_haves and inh not in must_haves
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
