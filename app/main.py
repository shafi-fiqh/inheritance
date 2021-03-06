import copy

from flask import abort
from flask import Flask
from flask import request

from src.cases_generator import CaseGenerator
from src.full_solver import full_solver
from src.generate_unsolved_problems import generate_problems_lst
from src.solver import solve
from utils.helpers import calculate_asl
from utils.helpers import calculate_intermittent_asl
from utils.helpers import need_final_solver

app = Flask(__name__)
CASE_GEN = CaseGenerator(
    "config/family_config.csv", filter="config/filter.yml", filter_bool=False
)


@app.route("/solve", methods=["POST"])
def solver():
    case = request.json

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


@app.route("/full_solver", methods=["POST"])
def complete_solver():
    case = request.json

    if not all(inh in CASE_GEN.inheritors for inh in case):
        abort(400, "Inheritors must correspond to the config definition")

    return full_solver(case)


@app.route("/asl_shares", methods=["POST"])
def asl_shares():
    case = request.json

    if not all(inh in CASE_GEN.inheritors for inh in case):
        abort(400, "Inheritors must correspond to the config definition")

    return calculate_asl(case)


@app.route("/generate_problems", methods=["POST"])
def generate_problems():
    problem_specs = request.json

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

    return generate_problems_lst(
        inheritors=CASE_GEN.inheritors,
        must_haves=problem_specs["must_haves"],
        not_haves=problem_specs["not_haves"],
        n_types=int(problem_specs["n_types"]),
        grand_father_and_siblings=bool(
            problem_specs.get("grand_father_and_siblings", "False")
        ),
    )


if __name__ == "__main__":
    app.run("0.0.0.0")
