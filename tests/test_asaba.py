import os
import sys

topdir = os.path.join(os.path.dirname(__file__), "..", "app")
sys.path.append(topdir)

from app.src.full_solver import solve_asaba_shares


def test_asaba_shares_calc():
    sample_case = {
        "husband": "1/4",
        "father": "1/6",
        "mother": "1/6",
        "son": "U",
        "daughter": "U",
    }

    expected = {
        "husband": "1/4",
        "father": "1/6",
        "mother": "1/6",
        "son": "5/18",
        "daughter": "5/36",
    }
    solve_asaba_shares(sample_case)
    assert expected == sample_case


def test_regular_remainder():
    sample_case = {"wife": "1/8", "daughter": "1/2", "son_of_son": "U"}

    expected = {"wife": "1/8", "daughter": "1/2", "son_of_son": "3/8"}
    solve_asaba_shares(sample_case)
    assert expected == sample_case


def test_father_asaba_no_asaba_share():
    input = {
        "husband": "1/4",
        "mother": "1/6",
        "father": "1/6 + U",
        "daughter": "1/2",
        "daughter_of_son": "1/6",
    }

    expected = {
        "husband": "1/4",
        "mother": "1/6",
        "father": "1/6",
        "daughter": "1/2",
        "daughter_of_son": "1/6",
    }
    solve_asaba_shares(input)
    assert expected == input


def test_father_asaba():
    input = {"husband": "1/4", "daughter": "1/2", "father": "1/6 + U"}

    expected = {"husband": "1/4", "daughter": "1/2", "father": "1/4"}
    solve_asaba_shares(input)
    assert expected == input


def test_multiple_women_asaba():
    input = {"wife": "1/8", "father": "1/6", "daughter_x2": "U", "son": "U"}

    expected = {"wife": "1/8", "father": "1/6", "daughter_x2": "17/48", "son": "17/48"}
    solve_asaba_shares(input)
    assert expected == input


def test_omariyya():
    input = {
        "wife": "1/4",
        "mother": "1/3 remainder",
        "grandmother_mother": "0",
        "father": "U",
        "father_of_father": "0",
    }

    expected = {
        "wife": "1/4",
        "father": "1/2",
        "mother": "1/4",
        "grandmother_mother": "0",
        "father_of_father": "0",
    }
    solve_asaba_shares(input)
    assert expected == input


def test_grandfather_siblings():
    input = {
        "mother": "1/6",
        "father_of_father": "5/18",
        "sister": "1/2",
        "paternal_halfsister_x2": "U",
        "paternal_halfbrother": "U",
    }

    expected = {
        "mother": "1/6",
        "father_of_father": "5/18",
        "sister": "1/2",
        "paternal_halfsister_x2": "1/36",
        "paternal_halfbrother": "1/36",
    }
    solve_asaba_shares(input)
    assert expected == input
