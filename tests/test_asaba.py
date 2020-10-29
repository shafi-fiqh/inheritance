import pytest

from src.full_solver import solve_asaba_shares


def test_asaba_shares_calc():
    sample_case = {
        "husband": "1/4",
        "father": "1/6",
        "mother": "1/6",
        "son": "A",
        "daughter": "A"
    }

    expected = {
        "husband": "1/4",
        "father": "1/6",
        "mother": "1/6",
        "son": "5/18",
        "daughter": "5/36"
    }

    assert(expected == solve_asaba_shares(sample_case))
