import copy
import json
import os

from flask import abort
from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin

import argparse
from app.src.cases_generator import CaseGenerator
from app.src.full_solver import full_solver
from app.src.generate_unsolved_problems import generate_problems_lst
from app.src.solver import solve
from app.utils.helpers import calculate_asl
from app.utils.helpers import calculate_intermittent_asl
from app.utils.helpers import need_final_solver

app = Flask(__name__)
CORS(app)
CASE_GEN = CaseGenerator(
    "config/family_config.csv", filter="config/filter.yml", filter_bool=False
)


@app.route("/solve", methods=["POST"])
@cross_origin()
def solver():
    case = request.json
    if not case:
        abort(400, "Case is empty")

    if not all(inh in CASE_GEN.inheritors for inh in case):
        abort(400, "Inheritors must correspond to the config definition")

    basic_shares_soln = solve(
        case=case,
        descendants=CASE_GEN.descendants,
        mahjoob=CASE_GEN.mahjoob,
        rank=CASE_GEN.rank,
        taseeb=CASE_GEN.taseeb,
    )

    intermediate_shares_soln = calculate_intermittent_asl(case=case)

    solved_case = {
        "basic_shares": basic_shares_soln,
        "intermediate_shares": intermediate_shares_soln,
    }
    if need_final_solver(intermediate_shares_soln):
        solved_case["final_shares"] = calculate_asl(
            full_solver(copy.deepcopy(basic_shares_soln))
        )

    return solved_case


@app.route("/generate_problems", methods=["POST"])
@cross_origin()
def generate_problems():
    problem_specs = request.json

    if not problem_specs:
        abort(400, "The problem specs are empty")

    if int(problem_specs["n_types"]) < 1:
        abort(
            400,
            "The number of inheritors in a problem should be greater than or equal to 1",
        )

    if not (
        set(problem_specs["must_haves"]) - set(problem_specs["not_haves"])
        or set(problem_specs["not_haves"]) - set(problem_specs["must_haves"])
    ):
        abort(
            400,
            "An inheritor cannot be in both the must have and ignore list at the same time",
        )

    if int(problem_specs["n_types"]) < len(problem_specs["must_haves"]):
        abort(
            400,
            "The total number of inheritors in the case should be greater than the number of inheritors who must be "
            "included",
        )

    if len(set(CASE_GEN.inheritors) - set(problem_specs["not_haves"])) == 0:
        abort(
            400,
            "Cannot generate cases where all inheritors have been asked to be excluded",
        )

    cases = generate_problems_lst(
        inheritors=CASE_GEN.inheritors,
        must_haves=problem_specs["must_haves"],
        not_haves=problem_specs["not_haves"],
        n_types=int(problem_specs["n_types"]),
        grand_father_and_siblings=bool(
            problem_specs.get("grand_father_and_siblings", "False")
        ),
    )

    ret = []
    for case in cases:
        case_obj = {}
        case_obj["problem"] = copy.deepcopy(case)
        basic_shares_soln = solve(
            case=case,
            descendants=CASE_GEN.descendants,
            mahjoob=CASE_GEN.mahjoob,
            rank=CASE_GEN.rank,
            taseeb=CASE_GEN.taseeb,
        )
        case_obj["basic_shares"] = basic_shares_soln

        intermediate_shares_soln = calculate_intermittent_asl(case=case)
        case_obj["intermediate_shares"] = intermediate_shares_soln

        if need_final_solver(intermediate_shares_soln):
            case_obj["final_shares"] = calculate_asl(
                full_solver(copy.deepcopy(basic_shares_soln))
            )
        ret.append(case_obj)

    return json.dumps(ret)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run("0.0.0.0", port=port)
