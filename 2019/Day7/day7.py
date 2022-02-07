from itertools import permutations

def GetArg(fullOpcode, codes, opcodeIndex, offset):
   divider = 10
   for i in xrange(offset):
      divider*=10
   mode = fullOpcode/divider%10
   
   if mode == 0:
      return codes[codes[opcodeIndex+offset]]
   elif mode == 1:
      return codes[opcodeIndex+offset]
   
class IntcodeComputer:
   def __init__(self, codes):
      self.codes = codes[:]
      self.opcodeIndex = 0
      self.lastOutput = None
      
   def RunIntcodeProgram(self,inputArgs):
      inputIdx = 0
      while True:
         fullOpcode = self.codes[self.opcodeIndex]
         opcode = fullOpcode%100
         #add
         if opcode == 1:
            arg1 = GetArg(fullOpcode, self.codes, self.opcodeIndex, 1)
            arg2 = GetArg(fullOpcode, self.codes, self.opcodeIndex, 2)
            arg3 = self.codes[self.opcodeIndex+3]
            self.codes[arg3] = arg1+arg2
            self.opcodeIndex += 4
         #multiply
         elif opcode == 2:
            arg1 = GetArg(fullOpcode, self.codes, self.opcodeIndex, 1)
            arg2 = GetArg(fullOpcode, self.codes, self.opcodeIndex, 2)
            arg3 = self.codes[self.opcodeIndex+3]
            self.codes[arg3] = arg1*arg2
            self.opcodeIndex += 4
         #input
         elif opcode == 3:
            arg1 = self.codes[self.opcodeIndex+1]
            
            if inputArgs is not None and inputIdx < len(inputArgs):
               x = inputArgs[inputIdx]
               inputIdx += 1
            else:
               x = int(input("Input integer "))
            self.codes[arg1] = x
            self.opcodeIndex += 2
         #output
         elif opcode == 4:
            arg1 = GetArg(fullOpcode, self.codes, self.opcodeIndex, 1)
            self.lastOutput = arg1
            self.opcodeIndex += 2
            return self.lastOutput
         #jump if true
         elif opcode == 5:
            arg1 = GetArg(fullOpcode, self.codes, self.opcodeIndex, 1)
            arg2 = GetArg(fullOpcode, self.codes, self.opcodeIndex, 2)
            if arg1 != 0:
               self.opcodeIndex = arg2
            else:
               self.opcodeIndex += 3
         #jump if false
         elif opcode == 6:
            arg1 = GetArg(fullOpcode, self.codes, self.opcodeIndex, 1)
            arg2 = GetArg(fullOpcode, self.codes, self.opcodeIndex, 2)
            if arg1 == 0:
               self.opcodeIndex = arg2
            else:
               self.opcodeIndex += 3
         #less than
         elif opcode == 7:
            arg1 = GetArg(fullOpcode, self.codes, self.opcodeIndex, 1)
            arg2 = GetArg(fullOpcode, self.codes, self.opcodeIndex, 2)
            arg3 = self.codes[self.opcodeIndex+3]
            
            self.codes[arg3] = 1 if arg1 < arg2 else 0
            self.opcodeIndex += 4
         #equals
         elif opcode == 8:
            arg1 = GetArg(fullOpcode, self.codes, self.opcodeIndex, 1)
            arg2 = GetArg(fullOpcode, self.codes, self.opcodeIndex, 2)
            arg3 = self.codes[self.opcodeIndex+3]
            
            self.codes[arg3] = 1 if arg2 == arg1 else 0
            self.opcodeIndex += 4
         #quit
         elif opcode == 99:
            break
         else:
            print 'bad news...'
            print opcode
         
      return None

with open("input.txt", "r") as FILE:
   line = FILE.readline()
   codes = [int(element) for element in line.strip().split(',')]
   
   biggestOutput = -999999
   biggestPermutation = None
   for phaseSequence in permutations([5,6,7,8,9]):
      numAmps = 5
      inout = 0
      computers = []
      for i in xrange(numAmps):
         computers.append(IntcodeComputer(codes))
      
      firstRun = True
      while inout is not None:
         for i in xrange(numAmps):
            if firstRun:
               args = [phaseSequence[i], inout]
            else:
               args = [inout,]
            inout = computers[i].RunIntcodeProgram(args)
         firstRun = False
      outputVal = computers[4].lastOutput
      
      if outputVal > biggestOutput:
         biggestOutput = outputVal
         biggestPermutation = phaseSequence
   print biggestOutput
   print biggestPermutation
   '''
   biggestOutput = -999999
   biggestPermutation = None
   for phaseSequence in permutations([0,1,2,3,4]):
      numAmps = 5
      inout = 0
      for i in xrange(numAmps):
         inout = runIntcodeProgram(codes, [phaseSequence[i], inout])
      if inout > biggestOutput:
         biggestOutput = inout
         biggestPermutation = phaseSequence
   print biggestOutput
   print biggestPermutation
   '''



   