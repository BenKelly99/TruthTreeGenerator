from logical_statement import *

def generate_all_truth_assignements(atoms):
    if len(atoms) == 0:
        return [{}]
    atom = atoms[0]
    all_except_atom_assignments = generate_all_truth_assignements(atoms[1:])
    all_assignments = []
    for assignment in all_except_atom_assignments:
        true_dict = {atom: True}
        false_dict = {atom: False}
        true_dict.update(assignment)
        false_dict.update(assignment)
        all_assignments.append(true_dict)
        all_assignments.append(false_dict)
    return all_assignments


def are_statements_consistent(statements, atoms):
    #print(statements[0].getString())
    #print(generate_all_truth_assignements(atoms))
    for assignment in generate_all_truth_assignements(atoms):
        consistent = True
        for statement in statements:
            if not statement.evaluate(assignment):
                consistent = False
                break
        if consistent:
            return True
    return False

def is_contradiction(statement, atoms):
    return are_statements_consistent([statement], atoms)