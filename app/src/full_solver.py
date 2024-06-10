from fractions import Fraction

from app.utils.helpers import calc_num_siblings
from app.utils.helpers import calc_share_radd_total
from app.utils.helpers import is_radd
from app.utils.helpers import is_omariyya
from app.utils.helpers import sum_of_inheriting_shares
from app.utils.helpers import solve_asaba_omariyya


def full_solver(case: dict) -> dict:
    """
    This is the final solver. In this step we solve for Asaba, Radd and
    find the Asl (base shares) of the problem and finally assign integers to
    each inheritor.
    :param case: dictionary of inheritors and shares
    :return: case with shares filled
    """
    if "U" in case.values() or "1/6 + U" in case.values():
        case = solve_asaba_shares(case)

    elif is_radd(case):
        case = solve_radd(case)

    return case


def solve_regular_asaba_shares(
    case: dict, asaba_inh: list, asaba_share: Fraction
) -> dict:
    n_siblings = calc_num_siblings(case)
    if is_omariyya(case, n_siblings):
        return solve_asaba_omariyya(case)

    asaba_normalize_for_inh = {}
    for inh in asaba_inh:
        if inh in [
            "daughter_x2",
            "daughter_of_son_x2",
            "sister_x2",
            "paternal_halfsister_x2",
        ]:
            asaba_normalize_for_inh[inh] = 2

        if inh in ["daughter", "daughter_of_son", "sister", "paternal_halfsister"]:
            asaba_normalize_for_inh[inh] = 1
        else:
            asaba_normalize_for_inh[inh] = 2

    num_asaba_inheritors = sum(asaba_normalize_for_inh.values())

    for inh in asaba_inh:
        inh_normalized_share = (
            Fraction(
                "{num}/{den}".format(
                    num=asaba_normalize_for_inh[inh], den=num_asaba_inheritors
                )
            )
            * asaba_share
        )

        case[inh] = str(inh_normalized_share)

    return case


def solve_grandfather_or_father_asaba_shares(
    case: dict, sum_of_shares: Fraction
) -> dict:
    sum_of_shares += Fraction("1/6")

    inheriting_ancestor = "father" if "father" in case else "father_of_father"

    if sum_of_shares >= 1:
        case[inheriting_ancestor] = str(Fraction("1/6"))

    else:
        case[inheriting_ancestor] = str(Fraction("1/6") + 1 - sum_of_shares)

    return case


def solve_asaba_shares(case: dict) -> dict:
    """
    Calculate the numerical shares of each Asaba inheritor
    :param case: dictionary of inheritors and shares
    :return: dictionary representing the inheritors and respective shares.
    """

    asaba_inh = [inh for inh in case if case[inh] == "U" or case[inh] == "1/6 + U"]
    sum_of_shares = sum_of_inheriting_shares(case)

    if len(asaba_inh) > 0:
        return solve_regular_asaba_shares(case, asaba_inh, 1 - sum_of_shares)

    return solve_grandfather_or_father_asaba_shares(case, sum_of_shares)


def solve_radd(case: dict) -> dict:
    """
    Calculate the distribution of the remainder of shares if there's any left
    :param case: dictionary of inheritors and shares
    :return: dictionary representing the inheritors and respective shares.
    """
    share_fractions = ["share 1/3", "share 1/6"]

    sum_eligible_inh = sum(
        [
            Fraction(case[inh])
            for inh in case
            if inh not in ["husband", "wife"] and case[inh] not in share_fractions
        ]
    )

    sum_of_share_inh, share_inh = calc_share_radd_total(case)

    if sum_of_share_inh is not None:
        sum_eligible_inh += sum_of_share_inh

    scaled_inh = {
        inh: Fraction(case[inh]) / sum_eligible_inh
        for inh in case
        if inh not in ["husband", "wife"] and case[inh] not in share_fractions
    }

    share_scaled_inh = {}
    if share_inh is not None:
        for inh in share_inh:
            share_scaled_inh[inh] = Fraction(share_inh[inh]) / sum_eligible_inh

    remainder = 1 - sum(
        [Fraction(case[inh]) for inh in case if case[inh] not in share_fractions]
    )

    if sum_of_share_inh is not None:
        remainder -= sum_of_share_inh

    for inh in scaled_inh:
        case[inh] = str(Fraction(case[inh]) + scaled_inh[inh] * remainder)

    for inh in share_scaled_inh:
        case[inh] = "share {}".format(
            str(Fraction(share_inh[inh]) + share_scaled_inh[inh] * remainder)
        )

    return case
