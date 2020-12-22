class MemoryInstruction:
    def __init__(self):
        self.index = 0
        self.value = 0
        
class Mask:
    def __init__(self):
        self.str = ""
        self.oneMask = 0
        self.zeroMask = 0
        self.xMask = 0
        self.xPositions = []
        
    def ComputeMask(self):
        self.oneMask = 0
        self.zeroMask = 0
        self.xMask = 0
        self.xPositions = []
        
        pos = 0
        for c in self.str:
            self.oneMask *= 2
            self.zeroMask *= 2
            self.xMask *= 2
            if c == '1':
                self.oneMask += 1
            elif c == '0':
                self.zeroMask += 1
            elif c == 'X':
                self.xMask += 1
                self.xPositions.append(len(self.str)-1-pos)
            pos += 1
                
    def ApplyMaskA(self, value):
        value |= self.oneMask
        value = ~value
        value |= self.zeroMask
        value = ~value
        return value
        
    def ApplyMaskB(self, value):
        value |= self.oneMask
        return value
        
        
    def GenerateIndices(self, value):
        newValues = []
        value = self.ApplyMaskB(value)
        
        
        for i in range(2**len(self.xPositions)):
            for j in range(len(self.xPositions)):
                bitVal = (i>>j)&1
                if bitVal == 0:
                    value &= ~(1<<self.xPositions[j])
                else:
                    value |= (1<<self.xPositions[j])
            newValues.append(value)
        return newValues
        

class Computer:
    def __init__(self):
        self.memory = {}
        self.currentMask = None
        
    def RunProgramA(self, program):
        for line in program:
            if isinstance(line, Mask):
                self.currentMask = line
            else:
                maskedValue = self.currentMask.ApplyMaskA(line.value)
                self.memory[line.index] = maskedValue
                
    def RunProgramB(self, program):
        for line in program:
            if isinstance(line, Mask):
                self.currentMask = line
            else:
                maskedIndices = self.currentMask.GenerateIndices(line.index)
                for index in maskedIndices:
                    self.memory[index] = line.value
    
            
            
  
input = []
with open("input.txt") as FILE:
    for line in FILE:
        line = line.strip()
        if line.startswith("mask"):
            mask = Mask()
            mask.str = line[line.find('=')+2:]
            mask.ComputeMask()
            input.append(mask)
        else:
            leftBracketPos = line.find('[')
            rightBracketPos = line.find(']')
            index = int(line[leftBracketPos+1:rightBracketPos])
            value = int(line[line.find('=')+2:])
            mi = MemoryInstruction()
            mi.index = index
            mi.value = value
            input.append(mi)
    


#part a 15:17
partA = Computer()
partA.RunProgramA(input)

sum = 0
for key in partA.memory:
    sum += partA.memory[key]
print(sum)

#part b 15:17
partB = Computer()
partB.RunProgramB(input)

sum = 0
for key in partB.memory:
    sum += partB.memory[key]
print(sum)