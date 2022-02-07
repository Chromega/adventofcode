import math
import time

WALL = 0
NORTH = 1
SOUTH = 2
WEST = 3
EAST = 4
START = 5
END = 6

RES_WALL = 0
RES_CLEAR = 1
RES_END = 2



def DirectionToDeltaPos(direction):
   if direction == NORTH:
      return (0,1)
   elif direction == SOUTH:
      return (0,-1)
   elif direction == WEST:
      return (-1,0)
   elif direction == EAST:
      return (1,0)
   else:
      print "Oh no!"
      return None
      
def MirrorDirection(direction):
   if direction == NORTH:
      return SOUTH
   elif direction == SOUTH:
      return NORTH
   elif direction == WEST:
      return EAST
   elif direction == EAST:
      return WEST
      
def IncrementPosition(pos, direction):
   deltaPos = DirectionToDeltaPos(direction)
   return (pos[0]+deltaPos[0], pos[1]+deltaPos[1])

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
      
class Drone:
   def __init__(self):
      self.pos = (0,0)
      self.startTile = (0,0)
      
def TryMove(drone, computer, direction, tiles):
   result = computer.RunIntcodeProgram([direction,])
   newPos = IncrementPosition(drone.pos, direction)
   if result != RES_WALL:
      drone.pos = newPos
   
   if newPos not in tiles:
      if result == RES_WALL:
         tiles[newPos] = WALL
      elif result == RES_CLEAR:
         tiles[newPos] = MirrorDirection(direction)
      elif result == RES_END:
         tiles[newPos] = MirrorDirection(direction)
      
   return result
   
def ReturnToStart(drone, computer, tiles):
   while True:
      direction = tiles[drone.pos]
      if direction == START:
         return
      if direction == END:
         print "ASDF"
         return
      
      res = TryMove(drone, computer, direction, tiles)
      #print (drone.pos, direction, res)
      
def GoToKnownTile(tile, drone, computer, tiles):
   #very inefficient, should find common ancenstor in path
   ReturnToStart(drone, computer, tiles)
   directions = []
   while tile != drone.startTile:
      direction = tiles[tile]
      mirror = MirrorDirection(direction)
      directions.append(mirror)
      tile = IncrementPosition(tile, direction)
   
   for i in xrange(len(directions)):
      direction = directions[len(directions)-1-i]
      TryMove(drone, computer, direction, tiles)
   
def ExploreNewTiles(drone, computer, tiles, newTiles, stopAtOxygen):
   newerTiles = set()
   for tile in newTiles:
      GoToKnownTile(tile, drone, computer, tiles)
      
      for direction in xrange(1,5):
         testTile = IncrementPosition(tile, direction)
         if testTile not in tiles:
            res = TryMove(drone, computer, direction, tiles)
            if stopAtOxygen and res == RES_END:
               print 'huzzah'
               return None
            elif res != RES_WALL:
               TryMove(drone, computer, MirrorDirection(direction), tiles) #undo
               newerTiles.add(testTile)
   return newerTiles
   
def ExploreUntilEnd(drone, computer, tiles, stopAtOxygen):
   newTiles = set()
   newTiles.add(drone.pos)
   steps = 0
   while (len(newTiles)>0):
      steps += 1
      print steps
      newTiles = ExploreNewTiles(drone, computer, tiles, newTiles, stopAtOxygen)
      if newTiles == None:
         break
   PrintTiles(drone, tiles)
   print steps
   
def PrintTiles(drone, tiles):
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
      for y in xrange(maxY, minY-1, -1):
         for x in xrange(minX, maxX+1):
            tile = (x,y)
            if tile == drone.pos:
               out += "O"
            elif tile in tiles:
               type = tiles[tile]
               if type == WALL:
                  out += "#"
               elif type == START:
                  out += "S"
               elif type == NORTH:
                  out += "^"
               elif type == SOUTH:
                  out += "v"
               elif type == EAST:
                  out += ">"
               elif type == WEST:
                  out += "<"
            else:
               out += " "
         out += "\n"
      print out
      print drone.pos
      

with open("input.txt", "r") as FILE:
   line = FILE.readline()
   codes = [int(element) for element in line.strip().split(',')]
   
   computer = IntcodeComputer(codes)
   drone = Drone()
   
   tiles = {}
   tiles[drone.pos] = START
   
   ExploreUntilEnd(drone, computer, tiles, True)
   
   tiles = {}
   tiles[drone.pos] = START
   drone.startTile = drone.pos
   ExploreUntilEnd(drone, computer, tiles, False) #minus 1
   
   """while True:
      direction = int(input("Input direction: "))
      if direction == 0:
         ReturnToStart(drone, computer, tiles)
      elif direction == 9:
         GoToKnownTile((-2,0), drone, computer, tiles)
      else:
         TryMove(drone, computer, direction, tiles)
      PrintTiles(drone, tiles)"""