import math
import time

UP = 0
LEFT = 1
DOWN = 2
RIGHT = 3
NUM_DIRECTIONS = 4


TURN_LEFT = 10
TURN_RIGHT = 11

def MirrorDirection(direction):
   return (direction+2)%4
   
def IncrementPosition(pos, direction, distance=1):
   if direction == UP:
      return (pos[0], pos[1]+distance)
   elif direction == DOWN:
      return (pos[0], pos[1]-distance)
   elif direction == LEFT:
      return (pos[0]-distance, pos[1])
   elif direction == RIGHT:
      return (pos[0]+distance, pos[1])
      
def GetTurnDirection(startDirection, endDirection):
   turnMod = (endDirection - startDirection + NUM_DIRECTIONS)%NUM_DIRECTIONS
   if turnMod == 1:
      return TURN_LEFT
   elif turnMod == 3:
      return TURN_RIGHT

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
      
class MapData:
   def __init__(self):
      self.map = []
      
   def FromString(self, mapStr):
      self.map = []
      for rowStr in mapStr.splitlines():
         row = []
         for c in rowStr.strip():
            row.append(c)
         if len(row) > 0:
            self.map.append(row)
      self.map = self.map[::-1]
   
   def ToString(self):
      mapStr = ""
      for y in xrange(len(self.map)-1, -1, -1):
         row = self.map[y]
         for c in row:
            mapStr.append(c)
         mapStr.append("\n")
      return mapStr.strip()
      
   def GetCharacterAt(self, pos):
      x = pos[0]
      y = pos[1]
      if y < 0 or y >= len(self.map):
         return '.'
      if x < 0 or x >= len(self.map[0]):
         return '.'
      return self.map[y][x]
      
   def HasScaffolding(self, pos):
      c = self.GetCharacterAt(pos)
      return c != '.'
      
   def IsIntersection(self, pos):
      for i in xrange(NUM_DIRECTIONS):
         incPos = IncrementPosition(pos, i)
         if not self.HasScaffolding(incPos):
            return False;
      return self.HasScaffolding(pos)
      
   def ScoreIntersections(self):
      score = 0
      for y in xrange(len(self.map)):
         row = self.map[y]
         for x in xrange(len(row)):
            if self.IsIntersection(x,y):
               score += x*y
      return score
      
   def GetPlayerTransform(self):
      for y in xrange(len(self.map)):
         row = self.map[y]
         for x in xrange(len(row)):
            c = self.GetCharacterAt((x,y))
            if c == '<' or c == '>' or c == 'v' or c == '^':
               if c == '<':
                  direction = LEFT
               elif c == '>':
                  direction = RIGHT
               elif c == '^':
                  direction = UP
               elif c == 'v':
                  direction = DOWN
               return ((x,y), direction)
               
   def GetNextDirection(self, pos, lastDirection):
      if lastDirection is not None:
         lastDirectionMirror = MirrorDirection(lastDirection)
      else:
         lastDirectionMirror = None
      
      for i in xrange(NUM_DIRECTIONS):
         if i == lastDirectionMirror:
            continue
         if self.HasScaffolding(IncrementPosition(pos, i)):
            return i
            
   def GetDistanceToMoveToEnd(self, pos, direction):
      count = 0
      pos = IncrementPosition(pos, direction)
      while (self.HasScaffolding(pos)):
         pos = IncrementPosition(pos, direction)
         count += 1
      return count
      
   def GetScriptToEnd(self):
      pos, direction = self.GetPlayerTransform()
      script = []
      
      while True:
         newDirection = self.GetNextDirection(pos, direction) #not quite right on first loop...but OK for our example data
         if newDirection == None:
            break
         turn = GetTurnDirection(direction, newDirection)
         distance = self.GetDistanceToMoveToEnd(pos, newDirection)
         newPos = IncrementPosition(pos, newDirection, distance)
         
         if turn == TURN_RIGHT:
            script.append('R')
         elif turn == TURN_LEFT:
            script.append('L')
         
         script.append(distance)
         
         pos = newPos
         direction = newDirection
         #print script
      return script
      
with open("input.txt", "r") as FILE:
   line = FILE.readline()
   codes = [int(element) for element in line.strip().split(',')]
   codes[0] = 2
   computer = IntcodeComputer(codes)
   
mapStr = ""
while True:
   val = computer.RunIntcodeProgram([])
   if val == None:
      break
   elif val == "INPUT":
      print 'input'
      break
   else:
      mapStr += chr(val)
    
print mapStr

#PART A
"""
mapData = MapData()
mapData.FromString(mapStr)
script = mapData.GetScriptToEnd()

out = ""
for c in script:
   out += str(c)
print out
"""

def SequenceToArgList(seq):
   argList = []
   for c in seq:
      argList.append(ord(c))
   argList.append(10)
   return argList

def RunToNextInput(computer, args):
   print "SENDING " + str(args)
   out = ""
   while True:
      val = computer.RunIntcodeProgram(args)
      args = []
      if val == None:
         print "DONE"
         break
      elif val == "INPUT":
         break
      elif val >= 256:
         out += str(val)
      else:
         out += chr(val)
   return out
   
A = "L,6,L,4,R,8"
B = "R,8,L,6,L,4,L,10,R,8"
C = "L,4,R,4,L,4,R,8"

MAIN = "A,B,A,C,B,C,B,C,A,B"

print RunToNextInput(computer, SequenceToArgList(MAIN))
print RunToNextInput(computer, SequenceToArgList(A))
print RunToNextInput(computer, SequenceToArgList(B))
print RunToNextInput(computer, SequenceToArgList(C))
print RunToNextInput(computer, [ord('n'),10])





   
"""
L6L4R8
R8L6L4L10R8
L6L4R8
L4R4L4R8
R8L6L4L10R8
L4R4L4R8
R8L6L4L10R8
L4R4L4R8
L6L4R8
R8L6L4L10R8
"""