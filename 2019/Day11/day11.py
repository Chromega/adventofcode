import math


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
               x = int(input("Input integer "))
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

with open("input.txt", "r") as FILE:
   line = FILE.readline()
   codes = [int(element) for element in line.strip().split(',')]
   
   
   whiteCells = set()
   totalCells = set()
   cell = (0,0)
   computer = IntcodeComputer(codes)
   direction = (0,1)
   
   #part2
   whiteCells.add((0,0))
   
   while True:
      isCurrentCellWhiteVal = 1 if cell in whiteCells else 0
      color = computer.RunIntcodeProgram([isCurrentCellWhiteVal,])
      if color == None:
         break
      directionChange = computer.RunIntcodeProgram([])
      if directionChange == None:
         break
      if color==1:
         whiteCells.add(cell)
      elif cell in whiteCells:
         whiteCells.remove(cell)
      totalCells.add(cell)
      if directionChange == 0:
         angle = -90
      else:
         angle = 90
      angle *= math.pi/180
      direction = (int(math.cos(angle)*direction[0]-math.sin(angle)*direction[1]),int(math.sin(angle)*direction[0]+math.cos(angle)*direction[1]))
      cell = (cell[0] + direction[0], cell[1]+direction[1])
      
   print len(totalCells)
   
   minX = 9999999
   minY = 9999999
   maxX = -9999999
   maxY = -9999999
   
   for cell in whiteCells:
      if cell[0] < minX:
         minX = cell[0]
      if cell[0] > maxX:
         maxX = cell[0]
      if cell[1] < minY:
         minY = cell[1]
      if cell[1] > maxY:
         maxY = cell[1]
   
   out = ""
   for y in xrange(minY, maxY+1):
      for x in xrange(minX, maxX+1):
         cell = (x,y)
         if cell in whiteCells:
            out += "#"
         else:
            out += " "
      out += "\n"
   print out[::-1]
   