import json
from sys import argv

from logical_statement import *

def generate_premises(options_file):


def export_to_willow(premises, file_name):
    final_dict = {}
    nodes = []
    index = 0
    for premise in premises:
        node = {}
        node["id"] = index
        node["text"] = premise.getString()
        node["children"] = []
        if index < len(premises) - 1:
            node["children"].append(index + 1)
        node["decomposition"] = []
        node["premise"] = True
        if index > 0:
            node["parent"] = index - 1
        nodes.append(node)
        index += 1
    options = {}
    options["requireAtomicContradiction"] = True
    options["requireAllBranchesTerminated"] = True
    options["lockedOptions"] = False
    final_dict["nodes"] = nodes
    final_dict["options"] = options

    with open(file_name, "w") as file:
        file.write(json.dumps(final_dict))




if __name__ == "__main__":
    if len(argv) != 2:
        print("Usage: python generator.py <file_name>")
        exit()

    A = Literal("A")
    B = Literal("B")
    C = Literal("C")
    p1 = Biconditional(A, B)
    p2 = Negation(A)
    p3 = Conditional(C, B)
    p4 = C
    
    premises = [p1, p2, p3, p4]

    export_to_willow(premises, argv[1])