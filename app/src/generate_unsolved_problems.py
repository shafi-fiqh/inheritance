import json
import itertools
import tqdm

from utils.helpers import nCr


UNIVERSAL_HEIRS = [
    "son",
    "son_of_son",
    "father",
    "father_of_father",
    "brother",
    "paternal_halfbrother",
    "nephew_brother",
    "nephew_paternal_halfbrother",
    "fathers_brother",
    "fathers_paternal_halfbrother",
    "son_of_fathers_brother",
    "son_of_fathers_paternal_halfbrother",
    "atiq",
    "mutiqa",
]


def keep_asaba_at_end(case: tuple) -> dict:
    taseeb_in_case = set([inh for inh in UNIVERSAL_HEIRS if inh in case])
    remaining_inh = set(case) - taseeb_in_case
    return list(remaining_inh) + list(taseeb_in_case)


def generate_problems_lst(
    inheritors: list,
    must_haves: list,
    not_haves: list,
    n_types: int,
    grand_father_and_siblings: bool,
):
    inheritors = [
        inh for inh in inheritors if inh not in not_haves and inh not in must_haves
    ]

    generator = itertools.combinations(inheritors, n_types - len(must_haves))
    total_cases = []
    grandfather = "father_of_father"
    siblings = [
        "brother",
        "paternal_halfbrother",
        "sister",
        "sister_x2",
        "paternal_halfsister",
        "paternal_halfsister_x2",
    ]

    for case in tqdm.tqdm(
        generator,
        total=nCr(n=len(inheritors), r=n_types - len(must_haves)),
    ):
        if (
            not grand_father_and_siblings
            and any([sibling in case for sibling in siblings])
            and grandfather in case
        ):
            continue
        case = case + tuple(must_haves)
        case = keep_asaba_at_end(case)
        case = {x: "0" for x in case}
        total_cases.append(case)
    return total_cases
