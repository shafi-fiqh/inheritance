from app.utils.sort_heirs import order_dict_by_inhs, order_inhs_according_to_sorted


def test_order_dict_by_keys():
    data_dict = {
        "daughter": "U",
        "father": "1/6",
        "mother": "1/6",
        "sister": "0",
        "husband": "1/4",
        "brother": "0",
        "son": "U",
    }

    expected_order = {
        "husband": "1/4",
        "father": "1/6",
        "mother": "1/6",
        "sister": "0",
        "brother": "0",
        "daughter": "U",
        "son": "U",
    }

    result = order_dict_by_inhs(data_dict)
    assert result == expected_order


def test_order_dict_according_to_sorted():
    unsorted_dict = {
        "daughter": "U",
        "father": "1/6",
        "mother": "1/6",
        "sister": "0",
        "husband": "1/4",
        "brother": "0",
        "son": "U",
    }

    sorted_dict = {
        "husband": "1/4",
        "father": "1/6",
        "mother": "1/6",
        "sister": "0",
        "brother": "0",
        "daughter": "U",
        "son": "U",
    }

    result = order_inhs_according_to_sorted(sorted_dict, unsorted_dict)
    assert result == sorted_dict
