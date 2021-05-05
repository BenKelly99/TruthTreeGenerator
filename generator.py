import json
import random
from sys import argv

from logical_statement import *

def random_opperation(num, p1, p2):
    if num == 0 :
        return And(p1, p2)
    if num == 1 :
        return Negation(p1)
    if num == 2 :
        return Or(p1, p2)
    if num == 3 :
        return Conditional(p1, p2)
    if num == 4 :
        return Biconditional(p1, p2)


def generate_premises(options_file):
    f = open(options_file,)
    data = json.load(f)

    atomics = int(data["atomics"])
    consistent = data["consistent"]
    num_premises = int(data["num_premises"])
    num_decompositons = int(data["num_decompositons"])

    min_branches = data["minimum_branches"]
    and_decomps = data["min_and_decomps"]
    or_decomps = data["min_or_decomps"]
    cond_decomps = data["min_cond_decomps"]
    bicond_decomps = data["min_bicond_decomps"]
    neg_and_decomps = data["min_neg_and_decomps"]
    neg_or_decomps = data["min_neg_or_decomps"]
    neg_cond_decomps = data["min_neg_cond_decomps"]
    neg_bicond_decomps = data["min_neg_bicond_decomps"]



    literals = []
    for x in range(atomics):
        literals.append(Literal(chr(65+x)))

    premises = []
    for x in range(num_premises):
        p1 = random.choice(literals)
        p2 = random.choice(literals)

        while p1 == p2:
            p2 = random.choice(literals)

        for y in range(random.randrange(0,num_decompositons,1)):
            p1 = random_opperation(random.choice([0,1,2,3,4]), p1, p2)
            p2 = random.choice(literals)

        premises.append(p1)

    return premises


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
    if len(argv) != 3:
        print("Usage: python generator.py <options_file_name> <file_name>")
        exit()


    # A = Literal("A")
    # B = Literal("B")
    # C = Literal("C")
    # p1 = Biconditional(A, B)
    # p2 = Negation(A)
    # p3 = Conditional(C, B)
    # p4 = C

    # premises = [p1, p2, p3, p4]

    premises = generate_premises(argv[1])

    export_to_willow(premises, argv[2])
