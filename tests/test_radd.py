import pytest

from src.full_solver import solve_radd


def test_no_spouse():
    input = {
        'daughter': '1/2',
        'grandmother_mother': '1/6'
    }

    expected_output = {
        'daughter': '3/4',
        'grandmother_mother': '1/4'
    }

    assert(solve_radd(input) == expected_output)


def test_with_spouse():
    input = {
        'wife': '1/8',
        'daughter': '1/2',
        'mother': '1/6'
    }

    expected_output = {
        'wife': '1/8',
        'daughter': '21/32',
        'mother': '7/32'
    }

    assert(solve_radd(input) == expected_output)
