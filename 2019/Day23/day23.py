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

NUM_COMPUTERS = 50
computers = []

for i in xrange(NUM_COMPUTERS):
   computer = IntcodeComputer(codes)
   computer.packetQueue = []
   computers.append(computer)
   computer.RunIntcodeProgram([i,]) #Network address assignment
    

lastNat = (-1,-1)
nat = (-1,-1)

while True:
   idle = True
   for i in xrange(NUM_COMPUTERS):
      computer = computers[i]
      if len(computer.packetQueue) > 0:
         inPacket = computer.packetQueue.pop(0)
         packetArgs = (inPacket[1], inPacket[2])
         idle = False
      else:
         packetArgs = (-1,)
      dest = computer.RunIntcodeProgram(packetArgs)
      if dest == "INPUT":
         continue
      idle = False
      x = computer.RunIntcodeProgram([])
      y = computer.RunIntcodeProgram([])
      if dest == 255:
         nat = (x,y)
      else:
         outPacket = (dest, x, y)
         computers[dest].packetQueue.append(outPacket)
   if idle:
         if nat[1] == lastNat[1]:
            print nat[1]
            break
         computers[0].packetQueue.append((0,nat[0], nat[1]))
         lastNat = nat