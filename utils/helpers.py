"""
Misc helper functions
"""
import numpy


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
    cond6 = 'husband' in case and 'wife' in case
    return any([cond1, cond2, cond3, cond4, cond5, cond6])


def sisters_with_daughters(case: dict)->bool:
    """
    Reveals whether we have both sisters (full or paternal) and daughters in the case.
    :param case: Dictionary with the inheritors and shares
    :return:
    """
    sisters = ['sister', 'sister_x2', 'paternal_halfsister', 'paternal_halfsister_x2']
    daughters = ['daughter', 'daughter_x2', 'daughter_of_son', 'daughter_of_son_x2']
    return any([sister in case for sister in sisters]) \
        and any([daughter in case for daughter in daughters])


def is_musharraka(case: dict)->bool:
    """
    Function to determine if the case is a musharraka. Conditions are
    husband in case
    mother or grandmothers in case
    at least 2 maternal siblings
    brother is in the case
    No inheriting branch or father/grandfather. Other asabat are allowed, siblings are allowed.
    :param case:
    :return:
    """
    cond1 = 'husband' in case
    cond2 = 'mother' in case or 'grandmother_father' in case or 'grandmother_mother' in case
    maternal = [inh for inh in case if 'maternal' in inh]
    n_maternal = sum([2  if 'x2' in inh else 1 for inh in maternal])
    cond3 = n_maternal >= 2
    cond4 = 'brother' in case
    inval = ['son', 'son_of_son', 'father', 'father_of_father', 'daughter', 'daughter_x2', 'daughter_of_son', 'daughter_of_son_x2']
    cond5 = all([inh not in case for inh in inval])
    return all([cond1, cond2, cond3, cond4, cond5])


def is_full_sibling(inh: str)->bool:
    """
    Reveals whether the inheritor is a full sibling or not.
    :param inh: string which specifies which inheritor
    :return: A boolean to indicate if it is a full sibling or isn't.
    """
    return inh in ['brother', 'sister', 'sister_x2']


def calculate_share_of_maternal_siblings(maternal_siblings_lst: list)->str:
    """
    Calculates the share of the maternal siblings.
    :param maternal_siblings_lst: list of all maternal siblings in the case
    :return: A string which is the share of the maternal siblings.
    """
    if len(maternal_siblings_lst) == 2 or maternal_siblings_lst[0] == 'maternal_halfsister_x2':
        return '1/3'
    return '1/6'

def is_omariyya(case: dict,
                n_siblings: int)->bool:
    """
    Check if this is a omariyya case or not
    :param case: dictionary containing inheritors
    :param n_siblings: number of siblings in the case
    :return: Boolean indicating whether or not it's a omariyya case
    """
    cond1 = 'husband' in case or 'wife' in case
    cond2 = 'mother' in case
    cond3 = 'father' in case
    omaria_core = ['husband', 'wife', 'mother', 'father']
    cond4 = all([case[inh]== 0 for inh in case if inh not in omaria_core] )
    cond5 = n_siblings < 2
    return all([cond1,cond2,cond3,cond4,cond5])
