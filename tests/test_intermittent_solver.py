from utils.helpers import calculate_intermittent_asl
from utils.helpers import need_final_solver


def test_regular_shares():
    input_share = {'husband': "1/4", 'daughter': "1/2"}
    expected_output = {
        'inheritance_pool': {
            'husband': 'pool_1',
            'daughter': 'pool_2',
            'remainder': 'pool_3',
            'total_shares': 'pool_4'
        },
        'share_pool': {
            'pool_1': 1,
            'pool_2': 2,
            'pool_3': 1,
            'pool_4': 4
        }
    }
    actual_output = calculate_intermittent_asl(input_share)
    assert need_final_solver(actual_output) is True
    assert actual_output == expected_output


def test_regular_asaba_shares():
    input_share = {"daughter": "A", "father": "1/6", "son": "A"}
    expected_output = {
        'inheritance_pool': {
            'father': 'pool_1',
            'son': 'pool_2',
            'daughter': 'pool_2',
            'remainder': 'pool_3',
            'total_shares': 'pool_4'
        },
        'share_pool': {
            'pool_1': 1,
            'pool_2': 5,
            'pool_3': 0,
            'pool_4': 6
        }
    }
    actual_output = calculate_intermittent_asl(input_share)
    assert need_final_solver(actual_output) is True
    assert actual_output == expected_output


def test_maternal_grandmother_shares():
    input_share = {"maternal_halfbrother": "share 1/3", "maternal_halfsister": "share 1/3",
                   "grandmother_mother": "share 1/6", "grandmother_father": "share 1/6", "son_of_son": "A"}
    expected_output = {
        'inheritance_pool': {
            'maternal_halfbrother': 'pool_1',
            'maternal_halfsister': 'pool_1',
            'grandmother_mother': 'pool_2',
            'grandmother_father': 'pool_2',
            'son_of_son': 'pool_3',
            'remainder': 'pool_4',
            'total_shares': 'pool_5'
        },
        'share_pool': {
            'pool_1': 2,
            'pool_2': 1,
            'pool_3': 3,
            'pool_4': 0,
            'pool_5': 6
        }
    }
    actual_output = calculate_intermittent_asl(input_share)
    assert need_final_solver(actual_output) is True
    assert actual_output == expected_output


def test_father_asaba():
    input_share = {"daughter": "1/2", "father": "1/6 + A"}
    expected_output = {
        'inheritance_pool': {
            'daughter': 'pool_1',
            'father': 'pool_2',
            'remainder': 'pool_3',
            'total_shares': 'pool_4'
        },
        'share_pool': {
            'pool_1': 1,
            'pool_2': 1,
            'pool_3': 0,
            'pool_4': 2
        }
    }
    actual_output = calculate_intermittent_asl(input_share)
    assert need_final_solver(actual_output) is False
    assert actual_output == expected_output


def test_awl_needs_final_solver():
    input_share = {
        "husband": "1/4",
        "daughter_x2": "2/3",
        "mother": "1/6",
        "father_of_father": "1/6",
        "brother": "A"
    }

    actual_output = calculate_intermittent_asl(input_share)
    assert need_final_solver(actual_output) is True
