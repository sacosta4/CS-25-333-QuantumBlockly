import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from pyqubo import Binary, Spin
from neal import SimulatedAnnealingSampler  

import json

app = Flask(__name__)
CORS(app)

WORKSPACE_DIR = "workspaces"
os.makedirs(WORKSPACE_DIR, exist_ok=True)

def parse_variables(variable_data):
    variables = {}

    for var_name, var_info in variable_data.items():
        if var_info["type"] == "Binary":
            variables[var_name] = Binary(var_name)
        elif var_info["type"] == "Spin":
            variables[var_name] = Spin(var_name)
        elif var_info["type"] == "Array":
            size = var_info.get("size", 10)
            variables[var_name] = [Binary(f"{var_name}[{i}]") for i in range(size)]
        else:
            return jsonify({"error": f"Unsupported variable type: {var_info['type']}"}), 400
    
    return variables

def parse_constraints(constraint_data, variables):
    constraints = []
    
    for constraint in constraint_data:
        lhs_expr = constraint.get("lhs", "0")
        comparison = constraint.get("comparison", "=")
        rhs = constraint.get("rhs", 0)
        
        try:
            lhs = eval(lhs_expr, {}, variables)

            if comparison == "=":
                constraints.append(10 * (lhs - rhs) ** 2)
            elif comparison == "<=":
                constraints.append((lhs - rhs) ** 2)
            elif comparison == ">=":
                constraints.append((rhs - lhs) ** 2)
            elif comparison == "!=":
                constraints.append((lhs - rhs) ** 2 * 100)
        except Exception as e:
            return jsonify({"error": f"Invalid constraint expression: {lhs_expr}, {str(e)}"}), 400

    return constraints

def parse_objective(objective_expr, variables):
    try:
        return eval(objective_expr, {}, variables)
    except Exception as e:
        return jsonify({"error": f"Invalid objective expression: {objective_expr}, {str(e)}"}), 400

@app.route('/quantum', methods=['POST'])
def calculate():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No JSON data received"}), 400
        
        variables = parse_variables(data.get("variables", {}))
        if isinstance(variables, tuple):
            return variables

        constraints = parse_constraints(data.get("Constraints", []), variables)
        if isinstance(constraints, tuple):
            return constraints
        
        objective = parse_objective(data.get("Objective", "0"), variables)
        if isinstance(objective, tuple):
            return objective
        
        qubo_model = sum(constraints) + objective
        compiled_qubo = qubo_model.compile()
        qubo, offset = compiled_qubo.to_qubo()
        qubo_str_keys = {str(k): v for k, v in qubo.items()}

        sampler = SimulatedAnnealingSampler()
        response = sampler.sample_qubo(qubo, num_reads=10)
        best_sample = list(response.samples())[0]

        solution = None
        for key, value in best_sample.items():
            if value == 1:
                solution = key
                break

        return jsonify({
            'qubo': qubo_str_keys,
            'offset': offset,
            'solution': solution,
            'sample': {k: int(v) for k, v in best_sample.items()}
        }), 200

    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True, port=8000)
