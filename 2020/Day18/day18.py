class Operation:
    def Apply(self, lhs, rhs):
        pass
class Addition(Operation):
    def Apply(self, lhs, rhs):
        return lhs+rhs
class Multiplication(Operation):
    def Apply(self, lhs, rhs):
        return lhs*rhs

class Expression:
    def __init__(self):
        self.subExpressions = []
        self.operations = []
        
    def EvaluateLinear(self):
        arguments = []
        for exp in self.subExpressions:
            arguments.append(exp.EvaluateLinear())
            
        currentVal = arguments[0]
        for i in range(len(self.operations)):
            op = self.operations[i]
            currentVal = op.Apply(currentVal, arguments[i+1])
        return currentVal
        
    def EvaluateAddThenMult(self):
        arguments = []
        for exp in self.subExpressions:
            arguments.append(exp.EvaluateAddThenMult())
            
        foundAnAddition = True
        
        newArguments = arguments[:]
        newOperations = self.operations[:]
        while foundAnAddition:   
            foundAnAddition = False
            for i in range(len(newOperations)):
                op = newOperations[i]
                if isinstance(op, Addition):
                    foundAnAddition = True
                    sum = op.Apply(newArguments[i], newArguments[i+1])
                    del newOperations[i]
                    del newArguments[i:i+2]
                    newArguments.insert(i, sum)
                    foundAnAddition = True
                    break
                    
        currentVal = newArguments[0]
        for i in range(len(newOperations)):
            op = newOperations[i]
            currentVal = op.Apply(currentVal, newArguments[i+1])
        return currentVal
        
        
class ConstantExpression(Expression):
    def __init__(self):
        self.value = 0
    def EvaluateLinear(self):
        return self.value
    def EvaluateAddThenMult(self):
        return self.value
            
def ParseExpressionFromTokens(tokens):
    if len(tokens)==1:
        exp = ConstantExpression()
        exp.value = int(tokens[0])
        return exp
    else:
        exp = Expression()
        
        depth = 0
        subExpStartIdx = 0
        for tokenIdx in range(len(tokens)):
            token = tokens[tokenIdx]
            if token == '(':
                depth += 1
                if depth == 1:
                    subExpStartIdx = tokenIdx
            elif token == ')':
                depth -= 1
                if depth == 0:
                    exp.subExpressions.append(ParseExpressionFromTokens(tokens[subExpStartIdx+1:tokenIdx]))
            elif depth == 0:
                if token == '+':
                    exp.operations.append(Addition())
                elif token == '*':
                    exp.operations.append(Multiplication())
                else:
                    exp.subExpressions.append(ParseExpressionFromTokens(tokens[tokenIdx:tokenIdx+1]))
        return exp
                
        
            
def ParseExpression(str):
    str = str.replace('(','( ')
    str = str.replace(')',' )')
    tokens = str.split(' ')
    return ParseExpressionFromTokens(tokens)
                    
            
            
        
input = []
with open("input.txt") as FILE:
    for line in FILE:
        input.append(ParseExpression(line.strip()))
                
#part a
sum = 0
for exp in input:
    sum += exp.EvaluateLinear()
print(sum)

#part a
sum = 0
for exp in input:
    sum += exp.EvaluateAddThenMult()
print(sum)