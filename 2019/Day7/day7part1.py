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
   
def runIntcodeProgram(codes, inputArgs):
   codes = codes[:] #copy codes
   opcodeIndex = 0
   inputIdx = 0
   lastOutput = None
   while True:
      fullOpcode = codes[opcodeIndex]
      opcode = fullOpcode%100
      #add
      if opcode == 1:
         arg1 = GetArg(fullOpcode, codes, opcodeIndex, 1)
         arg2 = GetArg(fullOpcode, codes, opcodeIndex, 2)
         arg3 = codes[opcodeIndex+3]
         codes[arg3] = arg1+arg2
         opcodeIndex += 4
      #multiply
      elif opcode == 2:
         arg1 = GetArg(fullOpcode, codes, opcodeIndex, 1)
         arg2 = GetArg(fullOpcode, codes, opcodeIndex, 2)
         arg3 = codes[opcodeIndex+3]
         codes[arg3] = arg1*arg2
         opcodeIndex += 4
      #input
      elif opcode == 3:
         arg1 = codes[opcodeIndex+1]
         
         if inputArgs is not None and inputIdx < len(inputArgs):
            x = inputArgs[inputIdx]
            inputIdx += 1
         else:
            x = int(input("Input integer "))
         codes[arg1] = x
         opcodeIndex += 2
      #output
      elif opcode == 4:
         arg1 = GetArg(fullOpcode, codes, opcodeIndex, 1)
         lastOutput = arg1
         opcodeIndex += 2
      #jump if true
      elif opcode == 5:
         arg1 = GetArg(fullOpcode, codes, opcodeIndex, 1)
         arg2 = GetArg(fullOpcode, codes, opcodeIndex, 2)
         if arg1 != 0:
            opcodeIndex = arg2
         else:
            opcodeIndex += 3
      #jump if false
      elif opcode == 6:
         arg1 = GetArg(fullOpcode, codes, opcodeIndex, 1)
         arg2 = GetArg(fullOpcode, codes, opcodeIndex, 2)
         if arg1 == 0:
            opcodeIndex = arg2
         else:
            opcodeIndex += 3
      #less than
      elif opcode == 7:
         arg1 = GetArg(fullOpcode, codes, opcodeIndex, 1)
         arg2 = GetArg(fullOpcode, codes, opcodeIndex, 2)
         arg3 = codes[opcodeIndex+3]
         
         codes[arg3] = 1 if arg1 < arg2 else 0
         opcodeIndex += 4
      #equals
      elif opcode == 8:
         arg1 = GetArg(fullOpcode, codes, opcodeIndex, 1)
         arg2 = GetArg(fullOpcode, codes, opcodeIndex, 2)
         arg3 = codes[opcodeIndex+3]
         
         codes[arg3] = 1 if arg2 == arg1 else 0
         opcodeIndex += 4
      #quit
      elif opcode == 99:
         break
      else:
         print 'bad news...'
         print opcode
      
   return lastOutput

with open("input.txt", "r") as FILE:
   line = FILE.readline()
   codes = [int(element) for element in line.strip().split(',')]
   
   
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




   