class Program:
    def __init__(self):
        self.accumulator = 0
        self.instructions = []
        self.instructionPointer = 0
    def Reset(self):
        self.accumulator = 0
        self.instructionPointer = 0
    def GetCopy(self):
        copy = Program()
        copy.instructions = self.instructions[:]
        return copy
    def Step(self):
        instruction = self.instructions[self.instructionPointer]
        operation = instruction[0]
        value = instruction[1]
        if operation == "nop":
            self.instructionPointer += 1
        elif operation == "acc":
            self.accumulator += value
            self.instructionPointer += 1
        elif operation == "jmp":
            self.instructionPointer += value
        else:
            print("Unknown opcode: " + operation)
    def HasTerminated(self):
        return self.instructionPointer == len(self.instructions)
    def DoesTerminate(self):
        visitedCommands = set()
        while self.instructionPointer not in visitedCommands and not self.HasTerminated():
            visitedCommands.add(self.instructionPointer)
            self.Step()
        return self.HasTerminated()
        
input = Program()
with open("input.txt") as FILE:
    for line in FILE:
        line = line.strip()
        tokens = line.split(' ')
        instruction = tokens[0]
        value = int(tokens[1])
        input.instructions.append((instruction,value))

        
#part a
partAProgram = input.GetCopy()
partAProgram.DoesTerminate()
print(partAProgram.accumulator)

#part b
numJumps = 0
for instruction in input.instructions:
    if instruction[0] == 'jmp':
        numJumps += 1
for i in range(numJumps):
    iProgram = input.GetCopy()
    
    #find ith jump
    jumpsSoFar = 0
    for j in range(len(iProgram.instructions)):
        if iProgram.instructions[j][0] == 'jmp':
            if jumpsSoFar == i:
                iProgram.instructions[j] = ("nop",0)
                break
            jumpsSoFar += 1
            
    if iProgram.DoesTerminate():
        print(iProgram.accumulator)
        break