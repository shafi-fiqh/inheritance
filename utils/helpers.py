"""
Misc helper functions
"""

def is_redundant(case: dict)->bool:
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
    return any([cond1, cond2, cond3, cond4, cond5])


def sisters_with_daughters(case: dict)->bool:
    """
    Reveals whether we have both sisters (full or paternal) and daughters in the case.
    :param case: Dictionary with the inheritors and shares
    :return:
    """
    sisters = ['sister', 'sister_x2', 'paternal_halfsister', 'paternal_halfsister_x2']
    daughters = ['daughter', 'daughter_x2']
    return any([sister in case for sister in sisters]) \
        and any([daughter in case for daughter in daughters])
