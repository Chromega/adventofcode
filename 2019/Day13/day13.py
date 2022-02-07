import math
import time


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

with open("input.txt", "r") as FILE:
   line = FILE.readline()
   codes = [int(element) for element in line.strip().split(',')]
   
   codes[0] = 2 #freeplay
   
   computer = IntcodeComputer(codes)
   score = 0
   nextInput = None
   finished = False
   tiles = {}
   while not finished:
      while True:
         if nextInput is not None:
            firstArgs = [nextInput,]
            nextInput = None
         else:
            firstArgs = []
         x = computer.RunIntcodeProgram(firstArgs)
         if x is None:
            finished = True
            break
         if x is "INPUT":
            break
         y = computer.RunIntcodeProgram([])
         type = computer.RunIntcodeProgram([])
         
         if x == -1 and y == 0:
            score = type
         else:
            tiles[(x,y)] = type
      #if type == 1:
      #   print (x,y)
      
   
      minX = 9999999
      minY = 9999999
      maxX = -9999999
      maxY = -9999999
      
      for tile in tiles:
         if tile[0] < minX:
            minX = tile[0]
         if tile[0] > maxX:
            maxX = tile[0]
         if tile[1] < minY:
            minY = tile[1]
         if tile[1] > maxY:
            maxY = tile[1]
      
      out = ""
      numBlocks = 0
      paddleX = 0
      ballX = 0
      for y in xrange(minY, maxY+1):
         for x in xrange(minX, maxX+1):
            tile = (x,y)
            if tile in tiles:
               type = tiles[tile]
               #empty
               if type == 0:
                  out += " "
               #wall
               elif type == 1:
                  out += "#"
               #block
               elif type == 2:
                  out += "+"
                  numBlocks += 1
               #paddle
               elif type == 3:
                  out += "="
                  paddleX = x
               #ball
               elif type == 4:
                  out += "o"
                  ballX = x
            else:
               out += " "
         out += "\n"
      print "SCORE " + str(score)
      print out
      print numBlocks
      if ballX < paddleX:
         nextInput = -1
      elif ballX > paddleX:
         nextInput = 1
      else:
         nextInput = 0
      #time.sleep(.01)