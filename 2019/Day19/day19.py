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
               #return "INPUT"
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

computer = IntcodeComputer(codes)
sum = 0
outStr = ""

SIZE = 100

BEAM = "#"
CLEAR = "."

def PrintArr(arr):
   outStr = ""
   for y in xrange(len(arr)):
      for x in xrange(len(arr[0])):
         if arr[y][x]:
            outStr += BEAM
         else:
            outStr += CLEAR
      outStr += "\n"
   print outStr
   
def PrintArrWithHighlight(arr, xmin, ymin, xmax, ymax):
   outStr = ""
   for y in xrange(len(arr)):
      for x in xrange(len(arr[0])):
         if x < xmin or y < ymin or x > xmax or y > ymax:
            outStr += " "
         elif arr[y][x]:
            outStr += BEAM
         else:
            outStr += CLEAR
      outStr += "\n"
   print outStr
   
def FindSquareOfSize(arr, size):
   print "Looking for " + str(size)
   height = len(arr)
   width = len(arr[0])
   for y in xrange(height):
      for x in xrange(width):
         if arr[y][x]:
            quit = False
            for deltaX in xrange(size):
               for deltaY in xrange(size):
                  xPrime = x + deltaX
                  yPrime = y + deltaY
                  if xPrime >= width:
                     quit = True
                     break
                  if yPrime >= height:
                     quit = True
                     break
                  if not arr[yPrime][xPrime]:
                     quit = True
                     break
               if quit:
                  break
            if not quit:
               return (x,y)

def SearchForSquare(minX, maxX, minY, maxY, stride, squareSize):
   print str((minX, minY)) + "->" + str((maxX, maxY)) + " @ " + str(stride)
   arr = []
   for y in xrange(minY, maxY+stride, stride):
      row = []
      for x in xrange(minX, maxX+stride, stride):
         computer = IntcodeComputer(codes)
         val = computer.RunIntcodeProgram([x*SIZE,y*SIZE])
         origin = x == 0 and y == 0
         if val == 1 and not origin:
            row.append(True)
         else:
            row.append(False)
      arr.append(row)
               
   PrintArr(arr)
   
   if stride == 1:
      answer = FindSquareOfSize(arr, squareSize)
      print (answer[0]+minX, answer[1]+minY)
      return
   minInARow = squareSize/stride - 1
   if minInARow <= 0:
      minInARow = 1
   maxInARow = squareSize/stride + 2
   
   newMinY = 9999999
   newMaxY = -9999999
   newMinX = 9999999
   newMaxX = -9999999
   
   topLeft = FindSquareOfSize(arr, minInARow)
   botRight = FindSquareOfSize(arr, maxInARow)
            
   newMinX = (topLeft[0]-5)*stride+minX
   newMinY = (topLeft[1]-5)*stride+minY
   
   newMaxX = (botRight[0]+maxInARow+5)*stride+minX
   newMaxY = (botRight[1]+maxInARow+5)*stride+minY
   
   PrintArrWithHighlight(arr, topLeft[0], topLeft[1], botRight[0], botRight[1])
   
   
   SearchForSquare(newMinX, newMaxX, newMinY, newMaxY, stride/2, squareSize)
         

searchSize = SIZE
minX = 0
maxX = 5000
minY = 0
maxY = 5000
SearchForSquare(minX, maxX, minY, maxY, SIZE, SIZE)