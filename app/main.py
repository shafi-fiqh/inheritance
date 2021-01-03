from flask import Flask
from flask import request

from src.cases_generator import CaseGenerator
from src.full_solver import full_solver
from src.solver import solve
from utils.helpers import calculate_asl

app = Flask(__name__)
CASE_GEN = CaseGenerator(
    "config/family_config.csv", filter="config/filter.yml", filter_bool=False
)


@app.route("/solve", methods=["POST"])
def initial_solver():
    case = request.json

    if not all(inh in CASE_GEN.inheritors for inh in case):
        abort(400, "Inheritors must correspond to the config definition")

    return solve(
        case=case,
        descendants=CASE_GEN.descendants,
        mahjoob=CASE_GEN.mahjoob,
        rank=CASE_GEN.rank,
        taseeb=CASE_GEN.taseeb,
    )


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
