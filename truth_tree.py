from queue import LifoQueue
from logical_statement import *


class TruthTreeStatement:
    def __init__(self, statement):
        self.statement = statement
        self.decomposed = self.statement.getDecomposition() == None
        self.children = []
        self.parent = None

def create_truth_tree_from_premises(premises):
    root = TruthTreeStatement(premises[0])
    prev = root
    for i in range(1, len(premises)):
        node = TruthTreeStatement(premises[i])
        node.parent = prev
        prev.children.append(node)
        prev = node

    decompose_all(root)
    return root

def decompose_all(root):
    stack = LifoQueue()
    stack.put(root)
    while not stack.empty():
        node = stack.get()
        if not node.decomposed:
            decompose(node)
        for child in node.children:
            stack.put(child)

def decompose(node):
    decomposition = node.statement.getDecomposition()
    if decomposition == None:
        return
    
    leaves = gather_leaves(node)
    for leaf in leaves:
        for branch in decomposition:
            root = TruthTreeStatement(branch[0])
            prev = root
            for i in range(1, len(branch)):
                node = TruthTreeStatement(branch[i])
                node.parent = prev
                prev.children.append(node)
                prev = node
            leaf.children.append(root)


def gather_leaves(root):
    leaves = []
    stack = LifoQueue()
    stack.put(root)
    while not stack.empty():
        node = stack.get()
        if len(node.children) == 0:
            leaves.append(node)
        for child in node.children:
            stack.put(child)
    return leaves


def check_for_contradiction(node):
    statement = node.statement
    temp = node.parent
    while not temp == None:
        if temp.statement.getString() == Negation(statement).getString() or Negation(temp.statement).getString() == statement.getString():
            return True
        temp = temp.parent
    return False

def maxmimum_depth_without_contradiction(root):
    if check_for_contradiction(root) or len(root.children) == 0:
        return 1
    max_child_depth = -1
    for child in root.children:
        depth = maxmimum_depth_without_contradiction(child)
        if depth > max_child_depth:
            max_child_depth = depth
    return max_child_depth + (1 if root.statement.getDecomposition() != None else 0)
    