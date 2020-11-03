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


def test_regular_remainder():
    sample_case = {
        "wife": "1/8",
        "daughter": "1/2",
        "son_of_son": "A"
    }

    expected = {
        "wife": "1/8",
        "daughter": "1/2",
        "son_of_son": "3/8"
    }

    assert(expected == solve_asaba_shares(sample_case))


def test_father_asaba_no_asaba_share():
    input = {
        "husband": "1/4",
        "mother": "1/6",
        "father": "1/6 + A",
        "daughter": "1/2",
        "daughter_of_son": "1/6"
    }

    expected = {
        "husband": "1/4",
        "mother": "1/6",
        "father": "1/6",
        "daughter": "1/2",
        "daughter_of_son": "1/6"
    }

    assert(expected == solve_asaba_shares(input))


def test_father_asaba():
    input = {
        "husband": "1/4",
        "daughter": "1/2",
        "father": "1/6 + A"
    }

    expected = {
        "husband": "1/4",
        "daughter": "1/2",
        "father": "1/4"
    }

    assert(expected == solve_asaba_shares(input))


def test_multiple_women_asaba():
    input = {
        "wife": "1/8",
        "father": "1/6",
        "daughter_x2": "A",
        "son": "A"
    }

    expected = {
        "wife": "1/8",
        "father": "1/6",
        "daughter_x2": "17/48",
        "son": "17/48"
    }

    assert(expected == solve_asaba_shares(input))


def test_omariyya():
    input = {
        "wife": "1/4",
        "mother": "1/3 remainder",
        "grandmother_mother": "0",
        "father": "A",
        "father_of_father": "0"
    }

    expected = {
        "wife": "1/4",
        "father": "1/2",
        "mother": "1/4",
        "grandmother_mother": "0",
        "father_of_father": "0"
    }

    assert(expected == solve_asaba_shares(input))


def test_grandfather_siblings():
    input = {
        "mother": "1/6",
        "father_of_father": "5/18",
        "sister": "1/2",
        "paternal_halfsister_x2": "A",
        "paternal_halfbrother": "A"
    }

    expected = {
        "mother": "1/6",
        "father_of_father": "5/18",
        "sister": "1/2",
        "paternal_halfsister_x2": "1/36",
        "paternal_halfbrother": "1/36"
    }

    assert(expected == solve_asaba_shares(input))
