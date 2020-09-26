"""
Collection of functions to solve for various inheritors.
The function should take a tuple of inheritors, and return some shares.
"""
from utils.helpers import calculate_share_of_maternal_siblings
from utils.helpers import is_full_sibling
from utils.helpers import is_musharika
from utils.helpers import sisters_with_daughters

def solve(case: dict,
          descendants:dict,
          mahjoob:dict,
          rank: dict,
          taseeb: dict) -> dict:
    """
    This is the master solver. Individual inheritor solvers added to this
    incrementally.
    :param case: dictionary of inheritors and shares
    :param descendants: dictionary mapping inheritor name to whether
    or not they're a male/female descendant
    :param mahjoob: dictionary mapping inheritor name to a list of inheritors
    that would block this inheritor if present
    :param rank: asaba ranking in the hierarchy
    :param taseeb: Dictionary mapping each inheritor to a list of inheritors
    that would take asaba if he is present.
    :return: case with shares filled
    """
    case = solve_father(case=case,
                        descendants=descendants)
    case = solve_husband(case=case,
                         descendants=descendants)
    case = solve_wife(case=case,
                      descendants=descendants)
    case = solve_daughter(case=case)
    case = solve_granddaughter(case=case)
    case = solve_grandmother(case=case, mahjoob=mahjoob)
    case = solve_maternal_siblings(case=case, mahjoob=mahjoob)
    case = solve_asaba(case=case,
                       rank=rank,
                       taseeb=taseeb)
    #Add more here as we create more partial solvers
    return case

def solve_father(case: dict,
                 descendants: dict)->dict:
    """
    Solve only for the father's share if he exists
    :param case: dictionary of inheritors and shares
    :param descendants: dictionary mapping inheritor name to whether
    or not they're a male/female descendant
    :return: string representing the fraction or asaba.
    """
    if 'father' not in case:
        return case
    #Check for any male descendants
    if any([descendants[inh] == 'M' for inh in case]):
        case['father']='1/6'
    #Check for any female descendants
    elif any([descendants[inh] == 'F' for inh in case]):
        case['father'] = '1/6 + A'
    else:
        case['father'] = 'A'
    return case

def solve_husband(case: dict,
                 descendants: dict)->dict:
    """
    Solve only for the father's share if he exists
    :param case: dictionary of inheritors and shares
    :param descendants: dictionary mapping inheritor name to whether
    or not they're a male/female descendant
    :return: string representing the fraction.
    """
    if 'husband' not in case:
        return case
    male_female_lookup={'M':0, 'F':0}
    if any([descendants[inh] in male_female_lookup for inh in case]):
        case['husband'] = '1/4'
    else:
        case['husband'] = '1/2'
    return case

def solve_wife(case: dict,
               descendants: dict)->dict:
    """
    Solve only for the father's share if he exists
    :param case: dictionary of inheritors and shares
    :param descendants: dictionary mapping inheritor name to whether
    or not they're a male/female descendant
    :return: string representing the fraction.
    """
    if 'wife' not in case:
        return case
    male_female_lookup={'M':0, 'F':0}
    if any([descendants[inh] in male_female_lookup for inh in case]):
        case['wife'] = '1/8'
    else:
        case['wife'] = '1/4'
    return case

def solve_daughter(case: dict)->dict:
    """
    Solve only for the daughter's share if she exists
    :param case: dictionary of inheritors and shares
    :return: string representing the fraction.
    """
    if 'daughter' not in case and 'daughter_x2' not in case:
        return case
    inh = 'daughter'
    share = '1/2'
    if 'daughter_x2' in case:
        inh = 'daughter_x2'
        share = '2/3'
    if 'son' in case:
        case[inh] = 'A'
    else:
        case[inh] = share
    return case

def solve_granddaughter(case: dict)->dict:
    """
    Solve only for the daughter's share if she exists
    :param case: dictionary of inheritors and shares
    :return: string representing the fraction.
    """
    if 'daughter_of_son' not in case and 'daughter_of_son_x2' not in case:
        return case
    inh='daughter_of_son'
    share='1/2'
    if 'daughter_of_son_x2' in case:
        inh = 'daughter_of_son_x2'
        share = '2/3'
    if 'son' in case:
        case[inh] = 0
    elif 'son_of_son' in case:
        case[inh] = 'A'
    elif 'daughter_x2' in case:
        case[inh] = 0
    elif 'daughter' in case:
        case[inh] = '1/6'
    else:
        case[inh] = share
    return case

def solve_grandmother(case:dict, mahjoob:dict)->dict:
    """
    Solve for maternal siblings.

    :param case: dictionary of inheritors and shares
    :param mahjoob: dictionary of inheritors and blockers
    :return: string representing the fraction.
    """
    if not(any(grandma in case for grandma in ['grandmother_mother', 'grandmother_father'])):
        return case

    if not(any(blocker in case for blocker in mahjoob['grandmother_father'])):
        case['grandmother_father'] = '1/6'

    if not(any(blocker in case for blocker in mahjoob['grandmother_mother'])):
        case['grandmother_mother'] = '1/6'

    return case

def solve_maternal_siblings(case: dict, mahjoob:dict) -> dict:
    """
    Solve for maternal siblings.

    :param case: dictionary of inheritors and shares
    :param mahjoob: dictionary of inheritors and blockers
    :return: string representing the fraction.
    """
    #Mahjoob for maternal siblings is common for brother or sister
    relatives_who_block_maternal_siblings = mahjoob['maternal_halfbrother']

    if any(relative in case for relative in relatives_who_block_maternal_siblings):
        return case

    maternal_siblings_in_case = [inh for inh in case if 'maternal' in inh]

    if len(maternal_siblings_in_case) > 0:
        maternal_sibling_share = calculate_share_of_maternal_siblings(maternal_siblings_in_case)
        for maternal_sibling in maternal_siblings_in_case:
            case[maternal_sibling] = maternal_sibling_share

    return case

def solve_asaba(case: dict,
                rank: dict,
                taseeb: dict) -> dict:
    """
    Solve for asaba inheritors except for the father/grandfather.

    :param case:
    :param fard_asaba:
    :param rank:
    :param taseeb: Dictionary containing the list of
    inheritors who become asaba if this inheritor is present.
    :return:
    """
    case_ranks = {inh: rank[inh] for inh in case if rank[inh] > 0}
    if sisters_with_daughters(case=case):
        if 'sister' in case:
            case_ranks['sister'] = 5.5
        if 'sister_x2' in case:
            case_ranks['sister_x2'] = 5.5
        if 'paternal_halfsister' in case:
            case_ranks['paternal_halfsister'] = 6.5
        if 'paternal_halfsister_x2' in case:
            case_ranks['paternal_halfsister_x2'] = 6.5
    if not case_ranks:
        return case
    closest = min(case_ranks, key=case_ranks.get)

    #Father is a special case to be handled in another function
    if closest != 'father':
        case[closest] = 'A'
        for inheritor in taseeb[closest]:
            if inheritor in case:
                case[inheritor] = 'A'

    #Musharika is a special case
    if is_full_sibling(closest) and is_musharika(case):
        maternal_siblings_in_case = [inh for inh in case if 'maternal' in inh]
        maternal_sibling_share = calculate_share_of_maternal_siblings(maternal_siblings_in_case)
        case[closest] = maternal_sibling_share
        for inheritor in taseeb[closest]:
            if inheritor in case:
                case[inheritor] = maternal_sibling_share

    return case
