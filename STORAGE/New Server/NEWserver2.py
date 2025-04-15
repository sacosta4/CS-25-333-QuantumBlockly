import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from pyqubo import Binary, Spin, UnaryEncInteger
from neal import SimulatedAnnealingSampler  

import json

app = Flask(__name__)
CORS(app)

WORKSPACE_DIR = "workspaces"
os.makedirs(WORKSPACE_DIR, exist_ok=True)

def parse_variables(variable_data):
    expressions = {}
    variables = {}

    for var_name, var_info in variable_data.items():
        var_type = var_info.get("type")

        if var_type == "Binary":
            expr = Binary(var_name)
            variables[var_name] = expr
            expressions[var_name] = expr

        elif var_type == "Spin":
            expr = Spin(var_name)
            variables[var_name] = expr
            expressions[var_name] = expr

        elif var_type == "Array":
            if "shape" not in var_info:
                return jsonify({"error": f"Array variable '{var_name}' must include a 'shape' field."}), 400

            shape = var_info["shape"]
            vartype = var_info.get("vartype", "Binary").lower()
            constructor = Spin if vartype == "spin" else Binary

            if isinstance(shape, int):
                for i in range(shape):
                    label = f"{var_name}_{i}"
                    expr = constructor(label)
                    variables[label] = expr
                    expressions[label] = expr

            elif isinstance(shape, (list, tuple)) and len(shape) == 2:
                rows, cols = shape
                for i in range(rows):
                    for j in range(cols):
                        label = f"{var_name}_{i}_{j}"
                        expr = constructor(label)
                        variables[label] = expr
                        expressions[label] = expr
            else:
                return jsonify({"error": f"Invalid array shape for '{var_name}': {shape}"}), 400

        elif var_type == "Unary":
            if "lower" not in var_info or "upper" not in var_info:
                return jsonify({"error": f"Unary variable '{var_name}' must have both 'lower' and 'upper' specified."}), 400

            lower = var_info["lower"]
            upper = var_info["upper"]
            encoder = UnaryEncInteger(var_name, (lower, upper))
            variables[var_name] = encoder

            n = upper - lower + 1
            bits = []
            for i in range(n):
                label = f"{var_name}[{i}]"
                bit = Binary(label)
                expressions[label] = bit
                bits.append(bit)

            expressions[var_name] = sum(bits)


        else:
            return jsonify({"error": f"Unsupported variable type: {var_type}"}), 400

    return expressions, variables

def parse_constraints(constraint_data, expressions):
    constraints = []

    for constraint in constraint_data:
        lhs_expr = constraint.get("lhs", "0")
        comparison = constraint.get("comparison", "=")
        rhs = constraint.get("rhs", 0)

        try:
            lhs = eval(lhs_expr, {}, expressions)

            if comparison == "=":
                constraints.append(10 * (lhs - rhs) ** 2)
            elif comparison == "<=" or comparison == "≤":
                constraints.append((lhs - rhs) ** 2)
            elif comparison == ">=" or comparison == "≥":
                constraints.append((rhs - lhs) ** 2)
            elif comparison == "!=":
                constraints.append((lhs - rhs) ** 2 * 100)
        except Exception as e:
            return jsonify({"error": f"Invalid constraint expression: {lhs_expr}, {str(e)}"}), 400

     # Enforce unary pattern if needed
    for var_name, expr in expressions.items():
        if '[' not in var_name and any(f"{var_name}[" in key for key in expressions):
            n = sum(1 for key in expressions if key.startswith(f"{var_name}[") and key.endswith(']'))
            for i in range(n - 1):
                a = expressions[f"{var_name}[{i}]"]
                b = expressions[f"{var_name}[{i+1}]"]
                constraints.append(10*(1 - a) * b)
    

    return constraints

def parse_objective(objective_expr, expressions):
    try:
        return eval(objective_expr, {}, expressions)
    except Exception as e:
        return jsonify({"error": f"Invalid objective expression: {objective_expr}, {str(e)}"}), 400

@app.route('/quantum', methods=['POST'])
def calculate():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No JSON data received"}), 400

        expressions, variables = parse_variables(data.get("variables", {}))
        if isinstance(expressions, tuple):
            return expressions

        constraints = parse_constraints(data.get("Constraints", []), expressions)
        if isinstance(constraints, tuple):
            return constraints

        objective = parse_objective(data.get("Objective", "0"), expressions)
        if isinstance(objective, tuple):
            return objective

        qubo_model = sum(constraints) + objective

         # Add unary variable objects to ensure structure is enforced
        for v in variables.values():
            if isinstance(v, UnaryEncInteger):  
                qubo_model += v 


        compiled_qubo = qubo_model.compile()
        qubo, offset = compiled_qubo.to_qubo()
        qubo_str_keys = {str(k): v for k, v in qubo.items()}

        sampler = SimulatedAnnealingSampler()
        response = sampler.sample_qubo(qubo, num_reads=1000)
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
