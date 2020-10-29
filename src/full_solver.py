from fractions import Fraction

from utils.helpers import sum_of_inheriting_shares


def solve_regular_asaba_shares(case: dict, asaba_inh: list,
                               asaba_share: Fraction) -> dict:
    asaba_normalize_for_inh = {}
    for inh in asaba_inh:
        if inh in ['daughter_x2', 'daughter_of_son_x2', 'sister_x2',
                   'paternal_halfsister_x2']:
            asaba_normalize_for_inh[inh] = 2

        if inh in ['daughter', 'daughter_of_son', 'sister',
                   'paternal_halfsister']:
            asaba_normalize_for_inh[inh] = 1
        else:
            asaba_normalize_for_inh[inh] = 2

    num_asaba_inheritors = sum(asaba_normalize_for_inh.values())

    for inh in asaba_inh:
        inh_normalized_share = Fraction('{num}/{den}'.format(
                                        num=asaba_normalize_for_inh[inh],
                                        den=num_asaba_inheritors)) \
                               * asaba_share

        case[inh] = str(inh_normalized_share)

    return case


def solve_grandfather_or_father_asaba_shares(case: dict,
                                             sum_of_shares: Fraction) -> dict:

    sum_of_shares += Fraction('1/6')

    print('sum_of_shares: {}'.format(sum_of_shares))

    inheriting_ancestor = 'father' if 'father' in case else 'father_of_father'

    if sum_of_shares >= 1:
        case[inheriting_ancestor] = str(Fraction('1/6'))

    else:
        case[inheriting_ancestor] = str(Fraction('1/6') + 1 - sum_of_shares)

    return case


def solve_asaba_shares(case: dict) -> dict:
    """
    Calculate the numerical shares of each Asaba inheritor
    :param case: dictionary of inheritors and shares
    :return: dictionary representing the inheritors and respective shares.
    """

    inheriting_shares = case.values()
    if 'A' not in inheriting_shares and '1/6 + A' not in inheriting_shares:
        return case

    asaba_inh = [inh for inh in case if case[inh] == 'A']
    sum_of_shares = sum_of_inheriting_shares(case)

    if len(asaba_inh) > 0:
        return solve_regular_asaba_shares(case, asaba_inh, 1 - sum_of_shares)

    return solve_grandfather_or_father_asaba_shares(case, sum_of_shares)
