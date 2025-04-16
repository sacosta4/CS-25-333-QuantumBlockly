import requests
import json
import os
import re

SERVER_URL = "http://127.0.0.1:8000/quantum"
TEST_CASES_DIR = os.path.dirname(os.path.abspath(__file__))

def load_test_case(filename):
    """Loads a test case JSON file from the same directory."""
    file_path = os.path.join(TEST_CASES_DIR, filename)

    if not os.path.exists(file_path):
        print(f"Error: Test case file '{filename}' not found.")
        return None

    with open(file_path, "r") as f:
        return json.load(f)

def send_request(test_case_file):
    """Loads JSON from a file and sends it to the server."""
    test_input = load_test_case(test_case_file)

    if test_input is None:
        return

    response = requests.post(SERVER_URL, json=test_input)

    if response.status_code == 200:
        data = response.json()

        print("\n=== Server Response ===")
        print("Offset:", data.get("offset"))
        print("Solution:", data.get("solution"))

        return_expr = data.get("return_expr")
        evaluated_return = data.get("return")

        print("Return Expression:", return_expr)
        if return_expr:
            substituted_expr = return_expr

            # Use substituted_values directly from server (includes score, chance, etc.)
            substitution_map = {k: str(v) for k, v in data.get("substituted_values", {}).items()}

            # Replace longest keys first to avoid overlap issues
            for var in sorted(substitution_map, key=len, reverse=True):
                substituted_expr = re.sub(rf"\b{re.escape(var)}\b", substitution_map[var], substituted_expr)

            print("Substituted Expression:", substituted_expr)

        print("Return Value:", evaluated_return)

        print("\nSolved Sample:")
        sample = data.get("sample", {})
        for var, val in sample.items():
            print(f"  {var} = {val}")

    else:
        print("\n=== Server Error ===")
        print("Status Code:", response.status_code)
        try:
            print("Details:", response.json())
        except Exception:
            print("Raw Response:", response.text)


if __name__ == "__main__":
    test_file = input("Enter the test case filename: ")
    send_request(test_file)
