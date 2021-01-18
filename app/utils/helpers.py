"""
Misc helper functions
"""
import copy
import math
from typing import Tuple
from typing import Union

from fractions import Fraction


def is_redundant(case: dict) -> bool:
    """
    Reveals whether there is a redundancy such as sister and sister_x2
    :param case: Dictionary containing the inheritors and their shares
    :return:
    """
    cond1 = "sister" in case and "sister_x2" in case
    cond2 = "daughter" in case and "daughter_x2" in case
    cond3 = "daughter_of_son" in case and "daughter_of_son_x2" in case
    cond4 = "paternal_halfsister" in case and "paternal_halfsister_x2" in case
    cond5 = "maternal_halfsister" in case and "maternal_halfsister_x2" in case
    cond6 = "husband" in case and "wife" in case
    return any([cond1, cond2, cond3, cond4, cond5, cond6])


def sisters_with_daughters(case: dict) -> bool:
    """
    Reveals whether we have both sisters
    (full or paternal) and daughters in the case.
    :param case: Dictionary with the inheritors and shares
    :return:
    """
    sisters = ["sister", "sister_x2", "paternal_halfsister", "paternal_halfsister_x2"]
    daughters = ["daughter", "daughter_x2", "daughter_of_son", "daughter_of_son_x2"]
    return any([sister in case for sister in sisters]) and any(
        [daughter in case for daughter in daughters]
    )


def is_musharraka(case: dict) -> bool:
    """
    Function to determine if the case is a musharraka.
    Conditions are husband in case
    mother or grandmothers in case
    at least 2 maternal siblings
    brother is in the case
    No inheriting branch or father/grandfather.
    Other asabat are allowed, siblings are allowed.
    :param case:
    :return:
    """
    cond1 = "husband" in case
    cond2 = (
        "mother" in case or "grandmother_father" in case or "grandmother_mother" in case
    )
    maternal = [inh for inh in case if "maternal" in inh]
    n_maternal = sum([2 if "x2" in inh else 1 for inh in maternal])
    cond3 = n_maternal >= 2
    cond4 = "brother" in case
    inval = [
        "son",
        "son_of_son",
        "father",
        "father_of_father",
        "daughter",
        "daughter_x2",
        "daughter_of_son",
        "daughter_of_son_x2",
    ]
    cond5 = all([inh not in case for inh in inval])
    return all([cond1, cond2, cond3, cond4, cond5])


def is_full_sibling(inh: str) -> bool:
    """
    Reveals whether the inheritor is a full sibling or not.
    :param inh: string which specifies which inheritor
    :return: A boolean to indicate if it is a full sibling or isn't.
    """
    return inh in ["brother", "sister", "sister_x2"]


def calculate_share_of_maternal_siblings(maternal_siblings_lst: list) -> str:
    """
    Calculates the share of the maternal siblings.
    :param maternal_siblings_lst: list of all maternal
    siblings in the case
    :return: A string which is the share of the maternal siblings.
    """
    if (
        len(maternal_siblings_lst) == 2
        or maternal_siblings_lst[0] == "maternal_halfsister_x2"
    ):
        return "1/3"
    return "1/6"


def calc_num_siblings(case: dict) -> int:
    siblings_dict = {}
    for inh in case:
        if "brother" in inh or "sister" in inh:
            if "x2" in inh:
                siblings_dict[inh] = 2
            else:
                siblings_dict[inh] = 1
    return sum([siblings_dict[inh] for inh in siblings_dict])


def is_omariyya(case: dict, n_siblings: int) -> bool:
    """
    Check if this is a omariyya case or not
    :param case: dictionary containing inheritors
    :param n_siblings: number of siblings in the case
    :return: Boolean indicating whether or not it's a omariyya case
    """
    cond1 = "husband" in case or "wife" in case
    cond2 = "mother" in case
    cond3 = "father" in case
    desc = [
        "son",
        "son_of_son",
        "daughter",
        "daughter_x2",
        "daughter_of_son",
        "daughter_of_son_x2",
    ]
    cond4 = all([inh not in case for inh in desc])
    cond5 = n_siblings < 2
    return all([cond1, cond2, cond3, cond4, cond5])


def is_akdariyya(case: dict) -> bool:
    """
    Check if this is an akdariyya problem
    :param case:
    :return:
    """
    cond1 = "husband" in case
    cond2 = ("sister" in case and "brother" not in case) or (
        "paternal_halfsister" in case and "paternal_halfbrother" not in case
    )
    cond3 = "mother" in case
    invalidators = ["daughter", "daughter_x2", "daughter_of_son", "daughter_of_son_x2"]
    cond4 = all([inh not in case for inh in invalidators])
    return all([cond1, cond2, cond3, cond4])


def nCr(n, r):
    f = math.factorial
    return f(n) / f(r) / f(n - r)


def sum_of_inheriting_shares(scope: dict) -> Fraction:

    fard_basic = [
        share
        for share in scope.values()
        if share not in ["share 1/3", "share 1/6", "1/3 remainder", "A", "1/6 + A"]
    ]
    shares = sum(Fraction(share) for share in fard_basic)
    if "share 1/3" in scope.values():
        shares += Fraction("1/3")
    if "share 1/6" in scope.values():
        shares += Fraction("1/6")

    return shares


def calculate_remainder_grandfather(case: dict) -> Fraction:
    """
    Calculate the remainder from the forood of the case.
    :param case:
    :return:
    """
    inheritors_not_in_scope = [
        "father_of_father",
        "brother",
        "sister",
        "sister_x2",
        "paternal_halfsister",
        "paternal_halfsister_x2",
    ]

    scope = {x: case[x] for x in case if x not in inheritors_not_in_scope}

    return 1 - sum_of_inheriting_shares(scope)


def least_common_multiple(rationals):
    denominators = [r.denominator for r in rationals]

    lcm = denominators[0]
    if len(rationals) == 1:
        return lcm
    for d in denominators[1:]:
        lcm = lcm // math.gcd(lcm, d) * d

    return lcm


def calculate_asl(case: dict) -> dict:
    """
    Calculate the base of the problem and the shares
    :param case:
    :return:
    """
    full_case = copy.copy(case)
    maternal = {
        "maternal_halfbrother": 1,
        "maternal_halfsister": 1,
        "maternal_halfsister_x2": 2,
    }
    siblings = {"brother": 1, "sister": 1, "sister_x2": 2}
    total_maternal = sum(maternal[inh] for inh in full_case if inh in maternal)

    if is_musharraka(case):
        total_maternal += sum(siblings[inh] for inh in full_case if inh in siblings)

    mat_in_case = [inh for inh in maternal if inh in full_case]
    if total_maternal > 1 and full_case[mat_in_case[0]][:5] == "share":
        for inh in maternal:
            if inh in full_case:
                full_case[inh] = (
                    Fraction(full_case[inh].split(" ")[1])
                    * maternal[inh]
                    / total_maternal
                )
        if is_musharraka(case):
            for inh in siblings:
                if inh in full_case:
                    full_case[inh] = (
                        Fraction(full_case[inh].split(" ")[1])
                        * siblings[inh]
                        / total_maternal
                    )

    if (
        "grandmother_father" in full_case
        and "grandmother_mother" in case
        and full_case["grandmother_father"][:5] == "share"
    ):
        full_case["grandmother_father"] = (
            Fraction(full_case["grandmother_father"].split(" ")[1]) / 2
        )
        full_case["grandmother_mother"] = (
            Fraction(full_case["grandmother_mother"].split(" ")[1]) / 2
        )

    if "mother" in full_case and full_case["mother"] == "1/3 remainder":
        remainder = "1/2" if "husband" in case else "3/4"
        full_case["mother"] = Fraction(1, 3) * Fraction(remainder)

    full_case = {inh: Fraction(full_case[inh]) for inh in full_case}
    x2 = [inh for inh in full_case if "x2" in inh]

    for inh in x2:
        share = full_case[inh]
        share = share / 2
        name = inh[:-3]
        full_case.pop(inh)
        full_case[name + "_1"] = share
        full_case[name + "_2"] = share

    rationals = [full_case[inh] for inh in full_case if full_case[inh] > 0]
    lcm = least_common_multiple(rationals)

    for inh in full_case:
        if full_case[inh] > 0:
            full_case[inh] = int(
                lcm / full_case[inh].denominator * full_case[inh].numerator
            )
        else:
            full_case[inh] = 0

    full_case["total_shares"] = int(sum(full_case[inh] for inh in full_case))
    return full_case


def is_radd(case: dict) -> bool:
    share_fractions = ["share 1/3", "share 1/6"]
    sum_of_shares = sum(
        [Fraction(share) for share in case.values() if share not in share_fractions]
    )

    if "share 1/3" in case.values():
        sum_of_shares += Fraction("1/3")
    if "share 1/6" in case.values():
        sum_of_shares += Fraction("1/6")

    return sum_of_shares < 1


def calc_share_radd_total(
    case: dict,
) -> Tuple[Union[Fraction, None], Union[dict, None]]:
    if "share 1/3" not in case.values() and "share 1/6" not in case.values():
        return None, None

    sum_of_shares = 0
    share_inh = {}
    if "share 1/3" in case.values():
        sum_of_shares += Fraction("1/3")

    if "share 1/6" in case.values():
        sum_of_shares += Fraction("1/6")

    for inh in case:
        if "share" in case[inh]:
            share_inh[inh] = case[inh].split(" ")[1]

    return sum_of_shares, share_inh


def solve_asaba_omariyya(case: dict) -> dict:
    shares = {
        "wife": {"father": "1/2", "mother": "1/4"},
        "husband": {"father": "1/3", "mother": "1/6"},
    }

    for spouse in shares:
        if spouse in case:
            for inh in shares[spouse]:
                case[inh] = shares[spouse][inh]

    return case
