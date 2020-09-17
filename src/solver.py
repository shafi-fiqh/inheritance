"""
Collection of functions to solve for various inheritors.
The function should take a tuple of inheritors, and return some shares.
"""

def solve(case: dict,
          descendants:dict) -> dict:
    """
    This is the master solver. Individual inheritor solvers added to this
    incrementally.
    :param case: dictionary of inheritors and shares
    :param descendants: dictionary mapping inheritor name to whether
    or not they're a male/female descendant
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
    if 'son' in case or 'daughter_x2' in case:
        case[inh] = 0
    elif 'son_of_son' in case:
        case[inh] = 'A'
    elif 'daughter' in case:
        case[inh] = '1/6'
    else:
        case[inh] = share
    return case
