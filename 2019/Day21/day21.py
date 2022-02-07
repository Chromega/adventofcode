class IntcodeComputer:
   def __init__(self, codes):
      self.codes = codes[:]
      self.opcodeIndex = 0
      self.lastOutput = None
      self.relativeBase = 0
      
   def GetArg(self, fullOpcode, offset, getPtr):
      divider = 10
      for i in xrange(offset):
         divider*=10
      mode = fullOpcode/divider%10
      
      #abs ptr
      if mode == 0:
         ptr = self.codes[self.opcodeIndex+offset]
      #rvalue
      elif mode == 1:
         ptr = self.opcodeIndex+offset
      #rel ptr
      elif mode == 2:
         ptr = self.codes[self.opcodeIndex+offset]+self.relativeBase
         
      if getPtr:
         return ptr
      elif ptr<len(self.codes):
         return self.codes[ptr]
      else:
         return 0
         
   def WriteValue(self, index, value):
      if index >= len(self.codes):
         self.codes = self.codes + [0 for i in xrange(index-len(self.codes)+1)]
      self.codes[index] = value
      
   def RunIntcodeProgram(self,inputArgs):
      inputIdx = 0
      while True:
         fullOpcode = self.codes[self.opcodeIndex]
         opcode = fullOpcode%100
         #add
         if opcode == 1:
            arg1 = self.GetArg(fullOpcode, 1, False)
            arg2 = self.GetArg(fullOpcode, 2, False)
            arg3 = self.GetArg(fullOpcode, 3, True)
            self.WriteValue(arg3, arg1+arg2)
            self.opcodeIndex += 4
         #multiply
         elif opcode == 2:
            arg1 = self.GetArg(fullOpcode, 1, False)
            arg2 = self.GetArg(fullOpcode, 2, False)
            arg3 = self.GetArg(fullOpcode, 3, True)
            self.WriteValue(arg3, arg1*arg2)
            self.opcodeIndex += 4
         #input
         elif opcode == 3:
            arg1 = self.GetArg(fullOpcode, 1, True)
            
            if inputArgs is not None and inputIdx < len(inputArgs):
               x = inputArgs[inputIdx]
               inputIdx += 1
            else:
               #x = int(input("Input integer "))
               return "INPUT"
            self.WriteValue(arg1, x)
            self.opcodeIndex += 2
         #output
         elif opcode == 4:
            arg1 = self.GetArg(fullOpcode, 1, False)
            self.lastOutput = arg1
            self.opcodeIndex += 2
            return self.lastOutput
         #jump if true
         elif opcode == 5:
            arg1 = self.GetArg(fullOpcode, 1, False)
            arg2 = self.GetArg(fullOpcode, 2, False)
            if arg1 != 0:
               self.opcodeIndex = arg2
            else:
               self.opcodeIndex += 3
         #jump if false
         elif opcode == 6:
            arg1 = self.GetArg(fullOpcode, 1, False)
            arg2 = self.GetArg(fullOpcode, 2, False)
            if arg1 == 0:
               self.opcodeIndex = arg2
            else:
               self.opcodeIndex += 3
         #less than
         elif opcode == 7:
            arg1 = self.GetArg(fullOpcode, 1, False)
            arg2 = self.GetArg(fullOpcode, 2, False)
            arg3 = self.GetArg(fullOpcode, 3, True)
            
            self.WriteValue(arg3, 1 if arg1 < arg2 else 0)
            self.opcodeIndex += 4
         #equals
         elif opcode == 8:
            arg1 = self.GetArg(fullOpcode, 1, False)
            arg2 = self.GetArg(fullOpcode, 2, False)
            arg3 = self.GetArg(fullOpcode, 3, True)
            
            self.WriteValue(arg3, 1 if arg2 == arg1 else 0)
            self.opcodeIndex += 4
         #adjust relative ptr
         elif opcode == 9:
            arg1 = self.GetArg(fullOpcode, 1, False)
            
            self.relativeBase += arg1
            self.opcodeIndex += 2
         #quit
         elif opcode == 99:
            break
         else:
            print 'bad news...'
            print opcode
         
      return None
      
def PrintASCIIOutput(computer):
   outStr = ""
   while True:
      c = computer.RunIntcodeProgram([])
      if c == None or c == "INPUT":
         break
      elif c > 256:
         outStr += str(c)
      else:
         outStr += chr(c)
   print outStr
   
def ProvideASCIIInput(computer, text):
   arr = []
   for c in text:
      arr.append(ord(c))
   o = computer.RunIntcodeProgram(arr)
   print o
      
with open("input.txt", "r") as FILE:
   line = FILE.readline()
   codes = [int(element) for element in line.strip().split(',')]

computer = IntcodeComputer(codes)

#Inputs A B C D
#Outputs J
#Temp T

#Jump if D is 1 and any of A,B, or C is false
#D AND NOT (A AND B AND C)
"""NOT A J
NOT J J #A is in J
NOT B T
NOT T T #B is in T
AND J T #A and B is in T
NOT C J
NOT J J #C is in T
AND J T #A and B and C is in T
NOT T T #NOT A&&B&&C is in T
NOT D J
NOT J J #D is in J
AND T J #Done
WALK
"""

walkProgram = """NOT A J
NOT J J
NOT B T
NOT T T
AND J T
NOT C J
NOT J J
AND J T
NOT T T
NOT D J
NOT J J
AND T J
WALK
"""

#If there's an immediate hole (ABC)
#AND We can land on D
#AND We can jump from D to H (or walk to E then jump to I)
#OR A is empty (failsafe)
#...jump!
#A omitted from first ABC check since we get it in the failsafe
runProgram = """NOT B T
NOT T T
AND C T
NOT T T
AND D T
NOT E J
NOT J J
AND I J
OR H J
AND J T
NOT A J
OR T J
RUN
"""

runProgramZ = """NOT E J
NOT J J
AND I J
OR H J
NOT D T
NOT T T
AND E T
AND F T
OR T J
AND D J
NOT A T
OR T J
RUN
"""

runProgramY = """OR E J
AND I J
OR H J
NOT A T
NOT T T
AND B T
AND C T
AND G T
AND H T
AND I T
NOT T T
AND T J
AND D J
NOT A T
OR T J
RUN
"""

runProgramX = """NOT E J
NOT J J
NOT I T
NOT T T
AND J T
NOT H J
NOT J J
OR J T
NOT D J
NOT J J
AND T J
RUN
"""

PrintASCIIOutput(computer)
ProvideASCIIInput(computer, runProgram)
PrintASCIIOutput(computer)

