import json
from sys import argv

def generate_empty_option_file(file_name):
    options = [
        "atomics",
        "consistent",
        "num_premises",
        "max_decomps_in_premise",
        "min_logic_depth",
        "min_and_decomps",
        "min_or_decomps",
        "min_cond_decomps",
        "min_bicond_decomps",
        "min_neg_and_decomps",
        "min_neg_or_decomps",
        "min_neg_cond_decomps",
        "min_neg_bicond_decomps"
    ]

    options_dict = {}
    for option in options:
        options_dict[option] = ""

    with open(file_name, "w") as file:
        file.write(json.dumps(options_dict))


if __name__ == "__main__":
    if len(argv) != 2:
        print("Usage: python options_generator.py <file_name>")
        exit()

    generate_empty_option_file(argv[1])
