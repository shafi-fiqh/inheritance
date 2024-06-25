"""
This module is to be used to generate inheritance cases.
Configuration files specify the base set of inheritors to permute.
Number of different types of inheritors passed as a parameter.
Saving the cases to a csv is an option.
"""

import argparse
import ast
import copy
import itertools
import logging
import os

import coloredlogs
import pandas as pd
import tqdm
import yaml

from app.src.full_solver import full_solver
from app.src.solver import solve
from app.utils.helpers import calculate_asl, is_redundant, nCr


class CaseGenerator:
    """
    The parent case generation class.
    Can generate inheritance cases from a config
    and save them.
    """

    def __init__(self, config: str, filter: str, filter_bool=False) -> None:
        """
        Initialize the list of inheritors.
        This can increase to more sophisticated levels in the future.
        :param config: Comma separated file containing the inheritors.
        """
        inheritors_df = pd.read_csv(config)
        inheritors_df = inheritors_df[inheritors_df.Ignore == 0]
        inheritors_df.Asaba = inheritors_df.Asaba.apply(ast.literal_eval)
        inheritors_df.blocked_by = inheritors_df.blocked_by.apply(ast.literal_eval)
        self.inheritors = list(inheritors_df["Inheritor"])
        self.descendants = pd.Series(
            inheritors_df.descendant.values, index=inheritors_df.Inheritor
        ).to_dict()
        self.rank = pd.Series(
            inheritors_df.Asaba_Rank.values, index=inheritors_df.Inheritor
        ).to_dict()
        self.taseeb = pd.Series(
            inheritors_df.Asaba.values, index=inheritors_df.Inheritor
        ).to_dict()
        self.mahjoob = pd.Series(
            inheritors_df.blocked_by.values, index=inheritors_df.Inheritor
        ).to_dict()
        self.n_types = 0
        self.generator = None
        self.must_have = []
        if filter_bool:
            with open(filter) as filter_file:
                filter_dict = yaml.load(filter_file, Loader=yaml.FullLoader)
            self.must_have = filter_dict["must_have"]
            self.ignore = filter_dict["ignore"]
            self.inheritors = [
                inh
                for inh in self.inheritors
                if inh not in self.ignore and inh not in self.must_have
            ]

    def generate_cases(self, n_types: int) -> itertools.combinations:
        """
        Generator object for inheritance cases to be solved.
        :param n_types: number of distinct different types of inheritors.
        For example Daughter + Son is considered 2 types.
        Daugher x 2 + Son is still considered n_types = 2.
        :return: Generator object for inheritane cases with the specified types
        """
        logging.info("Generating cases for cases with %s types of inheritors", n_types)
        self.n_types = n_types
        assert self.n_types > len(
            self.must_have
        ), "Number of types must be greater than the must have list of inheritors"
        self.generator = itertools.combinations(
            self.inheritors, n_types - len(self.must_have)
        )
        return self.generator

    def save_cases(self, output: str, chunk_size: int) -> None:
        """
        Append cases to an output file.
        We will yield and append cases one by one to the file,
        to avoid memory issues,
        as the permutation space can get quite large.
        :param output: string for the csv filepath
        :return: None
        """
        columns = ["Case", "Asaba_Rad", "Full_Case"]
        base = pd.DataFrame(columns=columns)
        logging.info("Saving output to %s, %s rows at a time", output, chunk_size)
        base.to_csv(output, index=False)
        n_cases = 0
        for case in tqdm.tqdm(
            self.generator,
            total=nCr(n=len(self.inheritors), r=self.n_types - len(self.must_have)),
        ):
            case = tuple(case) + tuple(self.must_have)
            if not is_redundant(case):
                # Later to be filled by the solver
                case = {x: "0" for x in case}
                solve(
                    case=case,
                    descendants=self.descendants,
                    mahjoob=self.mahjoob,
                    rank=self.rank,
                    taseeb=self.taseeb,
                )
                case_copy = copy.copy(case)
                full_solver(case_copy)
                full_case = calculate_asl(case=case_copy)
                temp = pd.DataFrame(
                    {
                        "Case": [case],
                        "Asaba_Rad": [case_copy],
                        "Full_case": [full_case],
                    }
                )
                base = base._append(temp)  # type: ignore
                n_cases += 1
                if n_cases % chunk_size == 0:
                    base.to_csv(output, mode="a", index=False, header=False)
                    base = pd.DataFrame(columns=columns)
        # Add the remainder to the csv,
        # unless it stopped exactly on a chunk_size multiple.
        if n_cases % chunk_size != 0:
            base.to_csv(output, mode="a", index=False, header=False)


def set_logging():
    """
    Defines a basic logger
    :return:
    """
    logging.getLogger(__name__)
    coloredlogs.install(level="DEBUG")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Case generator parameters")
    parser.add_argument(
        "--config",
        type=str,
        required=True,
        help="Path to the csv file " "containing the list of inheritors",
    )
    parser.add_argument(
        "--n_types",
        type=int,
        required=True,
        help="Size of the inheritance cases " "generated by type of inheritor.",
    )
    parser.add_argument(
        "--output",
        type=str,
        required=True,
        help="Output filename for the generated cases",
    )
    parser.add_argument(
        "--filter", type=str, required=True, help="Path to the filter yml"
    )
    set_logging()
    args = parser.parse_args()
    casegen = CaseGenerator(config=args.config, filter=args.filter)
    casegen.generate_cases(n_types=args.n_types)
    casegen.save_cases(output=os.path.join("output", args.output), chunk_size=10000)
