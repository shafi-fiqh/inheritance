import copy
import json
import pdb

from fractions import Fraction


from app.utils.helpers import calculate_intermittent_asl
from app.utils.helpers import need_final_solver


def pytest_generate_tests(metafunc):
    """
    Load the cases in the config
    :return: list of cases
    """
    with open("config/cases.json", "r") as cases_file:
        cases = json.load(cases_file)
    metafunc.parametrize("case", cases)


def test_cases(case):
    case_copy = copy.deepcopy(case)
    intermitten_soln = calculate_intermittent_asl(case_copy["initial_shares"])
    num_x2_inhs = [inh for inh in intermitten_soln["inheritance_pool"] if "x2" in inh]
    universal_heir_lst = [
        inh for inh in case["initial_shares"] if case["initial_shares"][inh] == "U"
    ]
    share_heir_lst = [inh for inh in case['initial_shares'] if "share" in case["initial_shares"][inh]]
    total_shares_case = case['full_shares']['total_shares']
    total_shares_soln = intermitten_soln["share_pool"][intermitten_soln["inheritance_pool"]["total_shares"]]

    if (len(num_x2_inhs) > 0 or (intermitten_soln["share_pool"][intermitten_soln["inheritance_pool"]["remainder"]]> 0) or (len(share_heir_lst) > 0)):
        assert True

    elif len(universal_heir_lst) > 1:
        sum_shares_universal_heir = sum(
            [case["full_shares"][inh] for inh in universal_heir_lst]
        )
        sum_shares_universal_heir_soln = intermitten_soln["share_pool"][
            intermitten_soln["inheritance_pool"][universal_heir_lst[0]]
        ]
        assert Fraction(sum_shares_universal_heir / total_shares_case) == Fraction(
            sum_shares_universal_heir_soln / total_shares_soln
        )
        assert all(
            [
                Fraction(case["full_shares"][inh] / total_shares_case)
                == Fraction(
                    intermitten_soln["share_pool"][
                        intermitten_soln["inheritance_pool"][inh]
                    ]
                    / total_shares_soln
                )
                for inh in case["full_shares"]
                if inh not in universal_heir_lst and inh not in num_x2_inhs
            ]
        )

    else:
        test_val = all(
            [
                case["full_shares"][inh]
                == intermitten_soln["share_pool"][
                    intermitten_soln["inheritance_pool"][inh]
                ]
                for inh in case["full_shares"]
            ]
        )
        assert test_val
