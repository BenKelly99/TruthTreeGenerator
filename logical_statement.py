from abc import ABC, abstractmethod

class LogicalStatement(ABC):
    @abstractmethod
    def evaluate(self, truth_assignment):
        pass

    @abstractmethod
    def getDecomposition(self):
        pass

    @abstractmethod
    def getString(self):
        pass

class BinaryStatement(LogicalStatement):
    def __init__(self, leftOperand, rightOperand, operator):
        self.leftOperand = leftOperand
        self.rightOperand = rightOperand
        self.operator = operator

    @abstractmethod
    def evaluate(self, truth_assignment):
        pass

    @abstractmethod
    def getDecomposition(self):
        pass

    def getString(self):
        return "(" + self.leftOperand.getString() + " " + self.operator + " " + self.rightOperand.getString() + ")"


class UnaryStatement(LogicalStatement):
    def __init__(self, operand, operator):
        self.operand = operand
        self.operator = operator

    @abstractmethod
    def evaluate(self, truth_assignment):
        pass

    @abstractmethod
    def getDecomposition(self):
        pass

    def getString(self):
        return self.operator + self.operand.getString()

class Literal(LogicalStatement):
    def __init__(self, literal):
        self.literal = literal

    def evaluate(self, truth_assignment):
        return truth_assignment[self.literal]

    def getDecomposition(self):
        return self

    def getString(self):
        return self.literal

class Negation(UnaryStatement):
    def __init__(self, operand):
        UnaryStatement.__init__(self, operand, "¬")
    
    def evaluate(self, truth_assignment):
        return not self.operand.evaluate(truth_assignment)

    def getDecomposition(self):
        if isinstance(self.operand, Literal):
            return self
        elif isinstance(self.operand, Negation):
            return self.operand.operand
        elif isinstance(self.operand, And):
            return [[Negation(self.operand.leftOperand)], [Negation(self.operand.leftOperand)]]
        elif isinstance(self.operand, Or):
            return [[Negation(self.operand.leftOperand), Negation(self.operand.leftOperand)]]
        elif isinstance(self.operand, Conditional):
            return [[self.operand.leftOperand, Negation(self.operand.leftOperand)]]
        elif isinstance(self.operand, Biconditional):
            return [[self.leftOperand, Negation(self.rightOperand)], [Negation(self.leftOperand), self.rightOperand]]

class And(BinaryStatement):
    def __init__(self, leftOperand, rightOperand):
        BinaryStatement.__init__(self, leftOperand, rightOperand, "∧")
    
    def evaluate(self, truth_assignment):
        return self.leftOperand.evaluate(truth_assignment) and self.rightOperand.evaluate(truth_assignment)

    def getDecomposition(self):
        return [[self.leftOperand, self.rightOperand]]

class Or(BinaryStatement):
    def __init__(self, leftOperand, rightOperand):
        BinaryStatement.__init__(self, leftOperand, rightOperand, "∨")
    
    def evaluate(self, truth_assignment):
        return self.leftOperand.evaluate(truth_assignment) or self.rightOperand.evaluate(truth_assignment)

    def getDecomposition(self):
        return [[self.leftOperand], [self.rightOperand]]

class Conditional(BinaryStatement):
    def __init__(self, leftOperand, rightOperand):
        BinaryStatement.__init__(self, leftOperand, rightOperand, "→")
    
    def evaluate(self, truth_assignment):
        return (not self.leftOperand.evaluate(truth_assignment)) or self.rightOperand.evaluate(truth_assignment)

    def getDecomposition(self):
        return [[Negation(self.leftOperand)], [self.rightOperand]]

class Biconditional(BinaryStatement):
    def __init__(self, leftOperand, rightOperand):
        BinaryStatement.__init__(self, leftOperand, rightOperand, "↔")
    
    def evaluate(self, truth_assignment):
        return self.leftOperand.evaluate(truth_assignment) == self.rightOperand.evaluate(truth_assignment)

    def getDecomposition(self):
        return [[self.leftOperand, self.rightOperand], [Negation(self.leftOperand), Negation(self.rightOperand)]]

if __name__ == "__main__":
    A = Literal("A")
    B = Literal("B")
    C = Literal("C")
    l1 = And(A, B)
    l2 = Or(B, C)
    l3 = Conditional(l1, l2)
    l4 = Conditional(Negation(A), Negation(l2))
    lFinal = And(l3, l4)
    print(lFinal.getString())
    truth_assignment = {}
    truth_assignment["A"] = False
    truth_assignment["B"] = True
    truth_assignment["C"] = False
    #print(lFinal.evaluate(truth_assignment))
