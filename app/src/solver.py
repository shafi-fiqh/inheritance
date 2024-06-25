"""
Collection of functions to solve for various inheritors.
The function should take a tuple of inheritors, and return some shares.
"""

from fractions import Fraction

from app.utils.helpers import (
    calc_num_siblings,
    calculate_remainder_grandfather,
    calculate_share_of_maternal_siblings,
    is_akdariyya,
    is_full_sibling,
    is_musharraka,
    is_omariyya,
    sisters_with_daughters,
)


def solve(
    case: dict, descendants: dict, mahjoob: dict, rank: dict, taseeb: dict
) -> None:
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

    """
    solve_father(case=case, descendants=descendants)
    solve_husband(case=case, descendants=descendants)
    solve_wife(case=case, descendants=descendants)
    solve_daughter(case=case)
    solve_granddaughter(case=case)
    solve_full_sister(case=case, mahjoob=mahjoob)
    solve_paternal_sister(case=case, mahjoob=mahjoob)
    solve_grandmother(case=case, mahjoob=mahjoob)
    solve_mother(case=case)
    solve_maternal_siblings(case=case, mahjoob=mahjoob)
    solve_asaba(case=case, rank=rank, taseeb=taseeb)
    solve_omariyya(case=case)
    solve_grandfather(case=case, descendants=descendants, taseeb=taseeb)
    # Add more here as we create more partial solvers


def solve_father(case: dict, descendants: dict) -> None:
    """
    Solve only for the father's share if he exists
    :param case: dictionary of inheritors and shares
    :param descendants: dictionary mapping inheritor name to whether
    or not they're a male/female descendant

    """
    if "father" not in case:
        return
    # Check for any male descendants
    if any([descendants[inh] == "M" for inh in case]):
        case["father"] = "1/6"
    # Check for any female descendants
    elif any([descendants[inh] == "F" for inh in case]):
        case["father"] = "1/6 + U"
    else:
        case["father"] = "U"


def solve_husband(case: dict, descendants: dict) -> None:
    """
    Solve only for the father's share if he exists
    :param case: dictionary of inheritors and shares
    :param descendants: dictionary mapping inheritor name to whether
    or not they're a male/female descendant

    """
    if "husband" not in case:
        return
    male_female_lookup = {"M": 0, "F": 0}
    if any([descendants[inh] in male_female_lookup for inh in case]):
        case["husband"] = "1/4"
    else:
        case["husband"] = "1/2"


def solve_wife(case: dict, descendants: dict) -> None:
    """
    Solve only for the father's share if he exists
    :param case: dictionary of inheritors and shares
    :param descendants: dictionary mapping inheritor name to whether
    or not they're a male/female descendant

    """
    if "wife" not in case:
        return
    male_female_lookup = {"M": 0, "F": 0}
    if any([descendants[inh] in male_female_lookup for inh in case]):
        case["wife"] = "1/8"
    else:
        case["wife"] = "1/4"


def solve_daughter(case: dict) -> None:
    """
    Solve only for the daughter's share if she exists
    :param case: dictionary of inheritors and shares

    """
    if "daughter" not in case and "daughter_x2" not in case:
        return
    inh = "daughter"
    share = "1/2"
    if "daughter_x2" in case:
        inh = "daughter_x2"
        share = "2/3"
    if "son" in case:
        case[inh] = "U"
    else:
        case[inh] = share


def solve_full_sister(case: dict, mahjoob: dict) -> None:
    """
    Solve only for the sister's share if she exists or is not blocked
    :param case: dictionary of inheritors and shares
    :param mahjoob: dictionary of inheritors and blockers

    """

    if "sister" not in case and "sister_x2" not in case:
        return

    if any(blocker in case for blocker in mahjoob["sister"]):
        return

    if sisters_with_daughters(case):
        return

    if "sister" in case:
        case["sister"] = "1/2"

    if "sister_x2" in case:
        case["sister_x2"] = "2/3"


def solve_granddaughter(case: dict) -> None:
    """
    Solve only for the daughter's share if she exists
    :param case: dictionary of inheritors and shares

    """
    if "daughter_of_son" not in case and "daughter_of_son_x2" not in case:
        return
    inh = "daughter_of_son"
    share = "1/2"
    if "daughter_of_son_x2" in case:
        inh = "daughter_of_son_x2"
        share = "2/3"
    if "son" in case:
        case[inh] = "0"
    elif "son_of_son" in case:
        case[inh] = "U"
    elif "daughter_x2" in case:
        case[inh] = "0"
    elif "daughter" in case:
        case[inh] = "1/6"
    else:
        case[inh] = share


def solve_paternal_sister(case: dict, mahjoob: dict) -> None:
    """
    Solve only for the paternal sister's share if she exists or is not blocked
    :param case: dictionary of inheritors and shares
    :param mahjoob: dictionary of inheritors and blockers

    """

    if "paternal_halfsister" not in case and "paternal_halfsister_x2" not in case:
        return

    if any(blocker in case for blocker in mahjoob["paternal_halfsister"]):
        return

    if sisters_with_daughters(case):
        return

    paternal_sister_in_case = [
        inh for inh in case if "paternal_halfsister" in inh
    ].pop()

    if paternal_sister_in_case == "paternal_halfsister":
        case[paternal_sister_in_case] = "1/2"

    if paternal_sister_in_case == "paternal_halfsister_x2":
        case[paternal_sister_in_case] = "2/3"

    if "sister" in case:
        case[paternal_sister_in_case] = "1/6"


def solve_grandmother(case: dict, mahjoob: dict) -> None:
    """
    Solve for maternal siblings.

    :param case: dictionary of inheritors and shares
    :param mahjoob: dictionary of inheritors and blockers

    """
    if not any(
        grandma in case for grandma in ["grandmother_mother", "grandmother_father"]
    ):
        return

    if (
        not any(blocker in case for blocker in mahjoob["grandmother_father"])
        and "grandmother_mother" in case
        and "grandmother_father" in case
    ):
        case["grandmother_mother"] = "share 1/6"
        case["grandmother_father"] = "share 1/6"
        return

    if (
        not any(blocker in case for blocker in mahjoob["grandmother_father"])
        and "grandmother_father" in case
    ):
        case["grandmother_father"] = "1/6"

    if (
        not any(blocker in case for blocker in mahjoob["grandmother_mother"])
        and "grandmother_mother" in case
    ):
        case["grandmother_mother"] = "1/6"


def solve_maternal_siblings(case: dict, mahjoob: dict) -> None:
    """
    Solve for maternal siblings.

    :param case: dictionary of inheritors and shares
    :param mahjoob: dictionary of inheritors and blockers

    """
    # Mahjoob for maternal siblings is common for brother or sister
    relatives_who_block_maternal_siblings = mahjoob["maternal_halfbrother"]

    if any(relative in case for relative in relatives_who_block_maternal_siblings):
        return

    maternal_siblings_in_case = [inh for inh in case if "maternal" in inh]

    if len(maternal_siblings_in_case) > 0:
        maternal_sibling_share = calculate_share_of_maternal_siblings(
            maternal_siblings_in_case
        )

        if (
            len(maternal_siblings_in_case) == 2
            or maternal_siblings_in_case[0] == "maternal_halfsister_x2"
        ):
            maternal_sibling_share = "share {}".format(maternal_sibling_share)

        for maternal_sibling in maternal_siblings_in_case:
            case[maternal_sibling] = maternal_sibling_share


def solve_asaba(case: dict, rank: dict[str, float], taseeb: dict) -> None:
    """
    Solve for asaba inheritors except for the father/grandfather.

    :param case:
    :param fard_asaba:
    :param rank:
    :param taseeb: Dictionary containing the list of
    inheritors who become asaba if this inheritor is present.

    """
    case_ranks = {inh: rank[inh] for inh in case if rank[inh] > 0}
    if sisters_with_daughters(case=case):
        if "sister" in case:
            case_ranks["sister"] = 5.5
        if "sister_x2" in case:
            case_ranks["sister_x2"] = 5.5
        if "paternal_halfsister" in case:
            case_ranks["paternal_halfsister"] = 6.5
        if "paternal_halfsister_x2" in case:
            case_ranks["paternal_halfsister_x2"] = 6.5
    if not case_ranks:
        return
    closest = min(case_ranks, key=lambda k: case_ranks[k])

    # Father is a special case to be handled in another function
    if closest != "father" and closest != "father_of_father":
        case[closest] = "U"
        for inheritor in taseeb[closest]:
            if inheritor in case:
                case[inheritor] = "U"

    # Musharraka is a special case
    if is_full_sibling(closest) and is_musharraka(case):
        maternal_siblings_in_case = [inh for inh in case if "maternal" in inh]
        maternal_sibling_share = calculate_share_of_maternal_siblings(
            maternal_siblings_in_case
        )
        case[closest] = "share {}".format(maternal_sibling_share)
        for inheritor in taseeb[closest]:
            if inheritor in case:
                case[inheritor] = "share {}".format(maternal_sibling_share)


def solve_mother(case: dict) -> None:
    """
    Solve for the mother
    :param case:

    """
    if "mother" not in case:
        return
    siblings_dict = {}
    for inh in case:
        if "brother" in inh or "sister" in inh:
            if "x2" in inh:
                siblings_dict[inh] = 2
            else:
                siblings_dict[inh] = 1
    n_siblings = sum([siblings_dict[inh] for inh in siblings_dict])
    far_warith = False
    for inh in case:
        if "son" in inh or "daughter" in inh:
            far_warith = True
    if far_warith or n_siblings >= 2:
        case["mother"] = "1/6"
    else:
        case["mother"] = "1/3"


def solve_omariyya(case: dict) -> None:
    """
    Solve for the 2 omariyan cases.
    :param case:

    """
    n_siblings = calc_num_siblings(case)
    if is_omariyya(case=case, n_siblings=n_siblings):
        case["mother"] = "1/3 remainder"


def solve_grandfather_no_siblings(case: dict, descendants: dict) -> None:
    if any([descendants[inh] == "M" for inh in case]):
        case["father_of_father"] = "1/6"
    # Check for any female descendants
    elif any([descendants[inh] == "F" for inh in case]):
        case["father_of_father"] = "1/6 + U"
    else:
        case["father_of_father"] = "U"


def solve_akdariya(case: dict) -> None:
    sister = "paternal_halfsister"
    if "sister" in case:
        sister = "sister"
    case["mother"] = "6/27"
    case["husband"] = "9/27"
    case["father_of_father"] = "8/27"
    case[sister] = "4/27"


def solve_grandfather_brother(case: dict, taseeb: dict) -> None:
    case["brother"] = "U"
    for inheritor in taseeb["brother"]:
        if inheritor in case:
            case[inheritor] = "U"


def solve_grandfather_sister(case: dict, remainder: Fraction, best: Fraction) -> None:
    if "sister" in case:
        base = Fraction("1/2")
        sister = "sister"
    else:
        base = Fraction("2/3")
        sister = "sister_x2"

    sister_share = max(Fraction("0"), remainder - best)
    if sister_share > base:
        sister_share = base
    for inh in case:
        if "paternal" in inh:
            case[inh] = "U"

    case[sister] = str(sister_share)


def solve_grandfather_paternal_halfbrother(case: dict, taseeb: dict) -> None:
    case["paternal_halfbrother"] = "U"
    for inheritor in taseeb["paternal_halfbrother"]:
        if inheritor in case:
            case[inheritor] = "U"


def solve_grandfather_paternal_halfsister(case: dict) -> None:
    if "paternal_halfsister" in case:
        case["paternal_halfsister"] = "U"
    else:
        case["paternal_halfsister_x2"] = "U"


def solve_grandfather(case: dict, descendants: dict, taseeb: dict) -> None:
    """
    Solve for the grandfather
    :param case:

    """
    if "father_of_father" not in case:
        return
    if "father" in case:
        return
    brothers = {"brother": 1, "paternal_halfbrother": 1}
    sisters = {
        "sister": 1,
        "sister_x2": 2,
        "paternal_halfsister": 1,
        "paternal_halfsister_x2": 2,
    }

    n_brothers = sum(brothers[warith] for warith in case if warith in brothers)
    n_sisters = sum(sisters[warith] for warith in case if warith in sisters)

    if n_brothers == 0 and n_sisters == 0:
        return solve_grandfather_no_siblings(case, descendants)

    if is_akdariyya(case):
        return solve_akdariya(case)

    remainder = calculate_remainder_grandfather(case)
    n_siblings = Fraction(1 + n_brothers + 0.5 * n_sisters)
    best = max(remainder / 3, Fraction("1/6"), remainder / n_siblings)

    case["father_of_father"] = str(best)

    if "brother" in case:
        return solve_grandfather_brother(case, taseeb)

    if "sister" in case or "sister_x2" in case:
        return solve_grandfather_sister(case, remainder, best)

    if "paternal_halfbrother" in case:
        return solve_grandfather_paternal_halfbrother(case, taseeb)

    if "paternal_halfsister" or "paternal_halfsister_x2" in case:
        return solve_grandfather_paternal_halfsister(case)
