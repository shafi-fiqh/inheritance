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
    case = solve_father(case)
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
    male_desc = ['son', 'son_of_son']
    female_desc = ['daughter', 'daughter_x2', 'daughter_of_son', 'daughter_of_son_x2']
    if any([x in case for x in male_desc]):
        case['father']='1/6'
    elif any([x in case for x in female_desc]):
        case['father']='1/6 + A'
    else:
        case['father']='A'
    return case



