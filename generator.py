import json
import random
import distutils.util

from sys import argv

from logical_statement import *
from utils import are_statements_consistent
from truth_tree import *

def random_opperation(num, p1, p2):
    if num == 0 :
        return And(p1, p2)
    if num == 1 :
        return Or(p1, p2)
    if num == 2 :
        return Conditional(p1, p2)
    if num == 3 :
        return Biconditional(p1, p2)
    if num == 4 :
        return Negation(And(p1, p2))
    if num == 5 :
        return Negation(Or(p1, p2))
    if num == 6 :
        return Negation(Conditional(p1, p2))
    if num == 7 :
        return Negation(Biconditional(p1, p2))


def generate_premises(options_file):
    f = open(options_file,)
    data = json.load(f)

    atomics = int(data["atomics"])
    consistent = bool(distutils.util.strtobool(data["consistent"]))
    num_premises = int(data["num_premises"])
    num_decompositons = int(data["num_decompositons"])

    min_depth = int(data["min_logic_depth"])
    and_decomps = int(data["min_and_decomps"])
    or_decomps = int(data["min_or_decomps"])
    cond_decomps = int(data["min_cond_decomps"])
    bicond_decomps = int(data["min_bicond_decomps"])
    neg_and_decomps = int(data["min_neg_and_decomps"])
    neg_or_decomps = int(data["min_neg_or_decomps"])
    neg_cond_decomps = int(data["min_neg_cond_decomps"])
    neg_bicond_decomps = int(data["min_neg_bicond_decomps"])

    possible_decomps = ([0] * and_decomps) + ([1] * or_decomps) + ([2] * cond_decomps) + ([3] * bicond_decomps) + ([4] * neg_and_decomps) + ([5] * neg_or_decomps) + ([6] * neg_cond_decomps) + ([7] * neg_bicond_decomps)

    atoms = []
    literals = []
    for x in range(atomics):
        atoms.append("" + (chr(65+x)))
        literals.append(Literal(chr(65+x)))
        literals.append(Negation(Literal(chr(65+x))))
    premises = []
    for x in range(num_premises):
        first = True
        new_premises = premises
        final_premise = None
        max_branch_length = -1
        while first or (not x == num_premises - 1 and not are_statements_consistent(new_premises, atoms)) or (x == num_premises - 1 and (not are_statements_consistent(new_premises, atoms) == consistent)) or max_branch_length < min_depth:
            first = False
            available_statements = []
            decomp_num = random.randrange(1,num_decompositons, 1)
            operation_count = 0
            while True:
                if operation_count + len(available_statements) > decomp_num:
                    break
                available = available_statements + literals
                p1 = random.choice(available)
                if len(available) > 2:
                    available.remove(p1)
                p2 = random.choice(available)
                if len(possible_decomps) > 0:
                    operation = random.choice(possible_decomps)
                    possible_decomps.remove(operation)
                else:
                    operation = random.randrange(0, 8, 1)
                premise = random_opperation(operation, p1, p2)
                available_statements.append(premise)
                if p1 in available_statements:
                    available_statements.remove(p1)
                if (not p1 == p2) and (p2 in available_statements):
                    available_statements.remove(p2)
                operation_count += 1
            final_premise = available_statements[0]
            for i in range(1, len(available_statements)):
                operation = random.randrange(0, 8, 1)
                final_premise = random_opperation(operation, final_premise, available_statements[i])
            new_premises = premises.copy()
            new_premises.append(final_premise)
            tree_version = create_truth_tree_from_premises(new_premises)
            max_branch_length = maxmimum_depth_without_contradiction(tree_version)
        premises.append(final_premise)
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
