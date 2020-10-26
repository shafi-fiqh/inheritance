"""
Misc helper functions
"""
import math
from fractions import Fraction


def is_redundant(case: dict) -> bool:
    """
    Reveals whether there is a redundancy such as sister and sister_x2
    :param case: Dictionary containing the inheritors and their shares
    :return:
    """
    cond1 = 'sister' in case and 'sister_x2' in case
    cond2 = 'daughter' in case and 'daughter_x2' in case
    cond3 = 'daughter_of_son' in case and 'daughter_of_son_x2' in case
    cond4 = 'paternal_halfsister' in case and 'paternal_halfsister_x2' in case
    cond5 = 'maternal_halfsister' in case and 'maternal_halfsister_x2' in case
    cond6 = 'husband' in case and 'wife' in case
    return any([cond1, cond2, cond3, cond4, cond5, cond6])


def sisters_with_daughters(case: dict) -> bool:
    """
    Reveals whether we have both sisters
    (full or paternal) and daughters in the case.
    :param case: Dictionary with the inheritors and shares
    :return:
    """
    sisters = ['sister', 'sister_x2',
               'paternal_halfsister',
               'paternal_halfsister_x2']
    daughters = ['daughter', 'daughter_x2',
                 'daughter_of_son', 'daughter_of_son_x2']
    return any([sister in case for sister in sisters]) \
        and any([daughter in case for daughter in daughters])


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
    cond1 = 'husband' in case
    cond2 = 'mother' in case or 'grandmother_father' in case \
            or 'grandmother_mother' in case
    maternal = [inh for inh in case if 'maternal' in inh]
    n_maternal = sum([2 if 'x2' in inh else 1 for inh in maternal])
    cond3 = n_maternal >= 2
    cond4 = 'brother' in case
    inval = ['son', 'son_of_son',
             'father', 'father_of_father',
             'daughter', 'daughter_x2',
             'daughter_of_son', 'daughter_of_son_x2']
    cond5 = all([inh not in case for inh in inval])
    return all([cond1, cond2, cond3, cond4, cond5])


def is_full_sibling(inh: str) -> bool:
    """
    Reveals whether the inheritor is a full sibling or not.
    :param inh: string which specifies which inheritor
    :return: A boolean to indicate if it is a full sibling or isn't.
    """
    return inh in ['brother', 'sister', 'sister_x2']


def calculate_share_of_maternal_siblings(maternal_siblings_lst: list) -> str:
    """
    Calculates the share of the maternal siblings.
    :param maternal_siblings_lst: list of all maternal
    siblings in the case
    :return: A string which is the share of the maternal siblings.
    """
    if len(maternal_siblings_lst) == 2 or \
            maternal_siblings_lst[0] == 'maternal_halfsister_x2':
        return '1/3'
    return '1/6'


def is_omariyya(case: dict,
                n_siblings: int) -> bool:
    """
    Check if this is a omariyya case or not
    :param case: dictionary containing inheritors
    :param n_siblings: number of siblings in the case
    :return: Boolean indicating whether or not it's a omariyya case
    """
    cond1 = 'husband' in case or 'wife' in case
    cond2 = 'mother' in case
    cond3 = 'father' in case
    desc = ['son', 'son_of_son',
            'daughter', 'daughter_x2',
            'daughter_of_son', 'daughter_of_son_x2']
    cond4 = all([inh not in case for inh in desc])
    cond5 = n_siblings < 2
    return all([cond1, cond2, cond3, cond4, cond5])


def is_akdariyya(case: dict) -> bool:
    """
    Check if this is an akdariyya problem
    :param case:
    :return:
    """
    cond1 = 'husband' in case
    cond2 = ('sister' in case and 'brother' not in case) or \
            ('paternal_halfsister' in case and
             'paternal_halfbrother' not in case)
    cond3 = 'mother' in case
    invalidators = ['daughter', 'daughter_x2', 'daughter_of_son',
                    'daughter_of_son_x2']
    cond4 = all([inh not in case for inh in invalidators])
    return all([cond1, cond2, cond3, cond4])


def nCr(n, r):
    f = math.factorial
    return f(n) / f(r) / f(n - r)


def calculate_remainder_grandfather(case: dict) -> Fraction:
    """
    Calculate the remainder from the forood of the case.
    :param case:
    :return:
    """
    inheritors_not_in_scope = ['father_of_father', 'brother', 'sister',
                               'sister_x2', 'paternal_halfsister',
                               'paternal_halfsister_x2']

    scope = {x: case[x] for x in case if x not in inheritors_not_in_scope}
    fard_basic = [share for share in scope.values() if share in
                  ['1/8', '1/4', '1/2', '1/6', '1/3', '2/3']]
    shares = sum(Fraction(share) for share in fard_basic)
    if 'share 1/3' in case.values():
        shares += Fraction('1/3')
    if 'share 1/6' in case.values():
        shares += Fraction('1/6')
    return Fraction('1') - shares


def solve_grandfather_no_siblings(case: dict, descendants: dict) -> dict:
    if any([descendants[inh] == 'M' for inh in case]):
        case['father_of_father'] = '1/6'
    # Check for any female descendants
    elif any([descendants[inh] == 'F' for inh in case]):
        case['father_of_father'] = '1/6 + A'
    else:
        case['father_of_father'] = 'A'
    return case


def solve_akdariya(case: dict) -> dict:
    sister = 'paternal_halfsister'
    if 'sister' in case:
        sister = 'sister'
    case['mother'] = '6/27'
    case['husband'] = '9/27'
    case['father_of_father'] = '8/27'
    case[sister] = '4/27'
    return case


def solve_grandfather_brother(case: dict, taseeb: dict) -> dict:
    case['brother'] = 'A'
    for inheritor in taseeb['brother']:
        if inheritor in case:
            case[inheritor] = 'A'
    return case


def solve_grandfather_sister(case: dict, remainder: Fraction,
                             best: Fraction) -> dict:
    if 'sister' in case:
        base = Fraction('1/2')
        sister = 'sister'
    else:
        base = Fraction('2/3')
        sister = 'sister_x2'

    sister_share = max(Fraction('0'), remainder - best)
    if sister_share > base:
        sister_share = base
    for inh in case:
        if 'paternal' in inh:
            case[inh] = 'A'

    case[sister] = str(sister_share)
    return case


def solve_grandfather_paternal_halfbrother(case: dict, taseeb: dict) -> dict:
    case['paternal_halfbrother'] = 'A'
    for inheritor in taseeb['paternal_halfbrother']:
        if inheritor in case:
            case[inheritor] = 'A'
    return case


def solve_grandfather_paternal_halfsister(case: dict) -> dict:
    if 'paternal_halfsister' in case:
        case['paternal_halfsister'] = 'A'
    else:
        case['paternal_halfsister_x2'] = 'A'
    return case
