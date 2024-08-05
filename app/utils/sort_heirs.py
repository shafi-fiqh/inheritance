def order_dict_by_inhs(inh_dict: dict) -> dict:
    # Determine the first key ('husband' or 'wife')
    first_key = next((key for key in ["husband", "wife"] if key in inh_dict), None)

    # Separate the rest into fixed shares inheritors and universal heir inheritors
    fixed_inh = {
        key: value
        for key, value in inh_dict.items()
        if key != first_key and value != "U"
    }
    universal_inh = {key: value for key, value in inh_dict.items() if value == "U"}

    # Construct the ordered dictionary
    ordered_dict = {}
    if first_key:
        ordered_dict[first_key] = inh_dict[first_key]
    ordered_dict.update(fixed_inh)
    ordered_dict.update(universal_inh)

    return ordered_dict


def order_inhs_according_to_sorted(sorted_inh: dict, unsorted_inh: dict) -> dict:
    # Create a new dictionary with keys from sorted_dict and values from unsorted_dict
    ordered_dict = {
        key: unsorted_inh.get(key) for key in sorted_inh if key in sorted_inh
    }
    return ordered_dict
