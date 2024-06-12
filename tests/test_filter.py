"""
Testing module
"""

import os
import ast
import pandas as pd
import yaml

from app.src.cases_generator import CaseGenerator


def test_filter():
    """
    Test that the solver returns expected results.
    Cases can be added to the cases.json file.
    Asaba should receive "U", third of remainder is '1/3 remainder'
    Rest are fractions in double quotes or the integer 0 without quotes.
    :return:
    """
    casegen = CaseGenerator(
        config="config/family_config.csv", filter="config/filter.yml", filter_bool=True
    )
    casegen.generate_cases(n_types=4)
    casegen.save_cases(output=os.path.join("output", "test.csv"), chunk_size=10000)

    with open("config/filter.yml") as filter_file:
        filter_dict = yaml.load(filter_file, Loader=yaml.FullLoader)
    must_have = filter_dict["must_have"]
    ignore = filter_dict["ignore"]
    frame = pd.read_csv("output/test.csv")
    inheritors = frame["Case"].apply(ast.literal_eval)
    inheritors = list(inheritors)
    assert [
        x in inh for inh in inheritors for x in must_have
    ], "Filter failed, missing must have inheritors"
    assert [
        x not in inh for inh in inheritors for x in ignore
    ], "Filter failed ignored inheritors present"
