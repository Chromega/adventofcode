import math
import time

UP = 0
LEFT = 1
DOWN = 2
RIGHT = 3
NUM_DIRECTIONS = 4

WALL = "#"
CLEAR = "."
START = "@"

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

class PathState:
   def __init__(self):
      self.keys = None
      self.pos = None
      self.hash = None
      
   def __eq__(self, other):
      if self.pos is not other.pos:
         return False
         
      if len(self.keys) != len(other.keys):
         return False
         
      for key in self.keys:
         if key not in other.keys:
            return False
      
      return True
      
   def __ne__(self, other):
      return not self.__eq__(other)
      
   def __hash__(self):
      if self.hash is not None:
         return self.hash
         
      self.hash = 0
      for key in self.keys:
         self.hash += key.__hash__()
      self.hash += self.pos.__hash__()
      
      return self.hash
      
class MapData:
   def __init__(self):
      self.map = []
      self.width = 0
      self.height = 0
      self.keyPositions = {}
      self.cachedDistances = {} #(a,b)=>(dist, [keysNeeded])
      
   def FromString(self, mapStr):
      self.map = []
      for rowStr in mapStr.splitlines():
         row = []
         for c in rowStr.strip():
            row.append(c)
         if len(row) > 0:
            self.map.append(row)
      self.map = self.map[::-1]
      self.height = len(self.map)
      self.width = len(self.map[0])
      self.keyPositions = {}
      
      for y in xrange(self.height):
         for x in xrange(self.width):
            pos = (x,y)
            c = self.GetCharacterAt(pos)
            if c.islower():
               self.keyPositions[c] = pos
               
      self.ComputePairwiseDistances()
   
   def ToString(self):
      mapStr = ""
      for y in xrange(len(self.map)-1, -1, -1):
         row = self.map[y]
         for c in row:
            mapStr += c
         mapStr += "\n"
      return mapStr.strip()
      
   def ComputePairwiseDistances(self):
      self.cachedDistances = {}
      keyList = self.keyPositions.keys()
      self.CacheReachableKeys('@')
      for key in keyList:
         self.CacheReachableKeys(key)
         
   def CacheReachableKeys(self, start):
      if start == START:
         pos = self.GetStartPos()
      else:
         pos = self.keyPositions[start]
         
      exploredTiles = {} #pos->[keys]
      currentTiles = set()
      currentTiles.add(pos)
      exploredTiles[pos] = []
      
      iterations = 1
      while len(currentTiles) > 0:
         newTiles = set()
         for tile in currentTiles:
            for direction in xrange(NUM_DIRECTIONS):
               testTile = IncrementPosition(tile, direction)
               currentKeysNeeded = exploredTiles[tile]
               if testTile not in exploredTiles:
                  tileType = self.GetCharacterAt(testTile)
                  #Wall, done
                  if tileType == WALL:
                     continue
                  #Door or key
                  elif tileType != CLEAR and tileType != START:
                     #Door
                     if tileType.isupper():
                        key = tileType.lower()
                        #Locked door
                        currentKeysNeeded = currentKeysNeeded[:]
                        currentKeysNeeded.append(key)
                     #Key
                     else:
                        key = tileType
                        self.cachedDistances[(start, key)] = (iterations, currentKeysNeeded)
                  #If we got this far without a continue, we're on a clear tile
                  newTiles.add(testTile)
                  exploredTiles[testTile] = currentKeysNeeded
         currentTiles = newTiles
         iterations += 1
      
   def GetCharacterAt(self, pos):
      x = pos[0]
      y = pos[1]
      return self.map[y][x]
      
   def IsWall(self, pos):
      c = self.GetCharacterAt(pos)
      return c == WALL
      
   def IsClear(self, pos):
      c = self.GetCharacterAt(pos)
      return c == CLEAR
      
   def IsDeadEnd(self, pos):
      numWalls = 0
      if not self.IsClear(pos):
         return False
      for i in xrange(NUM_DIRECTIONS):
         newPos = IncrementPosition(pos, i)
         if self.IsWall(newPos):
            numWalls += 1
      return numWalls >= 3
   
   def FillGaps(self):
      numGapsFilled = 0
      for y in xrange(self.height):
         for x in xrange(self.width):
            pos = (x,y)
            if self.IsDeadEnd(pos):
               self.map[y][x] = WALL
               numGapsFilled += 1
      #Go Agane
      if numGapsFilled > 0:
         self.FillGaps()
         
   def GetStartPos(self):
      for y in xrange(self.height):
         for x in xrange(self.width):
            if self.GetCharacterAt((x,y))==START:
               return (x,y)
               
               
   def GetNumKeys(self):
      return len(self.keyPositions)
         
         
   def GetReachableKeysFromPosition(self, keySet, pos):
      exploredTiles = set()
      currentTiles = set()
      currentTiles.add(pos)
      exploredTiles.add(pos)
      
      reachableKeys = {}
      
      iterations = 1
      while len(currentTiles) > 0:
         newTiles = set()
         for tile in currentTiles:
            for direction in xrange(NUM_DIRECTIONS):
               testTile = IncrementPosition(tile, direction)
               if testTile not in exploredTiles:
                  tileType = self.GetCharacterAt(testTile)
                  #Wall, done
                  if tileType == WALL:
                     continue
                  #Door or key
                  elif tileType != CLEAR and tileType != START:
                     #Door
                     if tileType.isupper():
                        key = tileType.lower()
                        #Locked door
                        if key not in keySet:
                           continue
                     #Key
                     else:
                        key = tileType
                        #Already have key, treat as clear
                        if key in keySet:
                           pass
                        #We already found a shorter way here
                        elif key in reachableKeys:
                           continue
                        #nice, a new key!
                        else:
                           reachableKeys[key] = iterations
                           continue
                  #If we got this far without a continue, we're on a clear tile
                  newTiles.add(testTile)
                  exploredTiles.add(testTile)
         currentTiles = newTiles
         iterations += 1
               
      return reachableKeys
      
   def FindShortestPath(self):
      pos = self.GetStartPos()
      numKeys = self.GetNumKeys()
      
      #state vector, position
      startState = PathState()
      startState.keys = set()
      startState.pos = '@'
      
      currentStates = {}
      currentStates[startState] = 0
      
      for i in xrange(numKeys):
         print str(i) + ": " + str(len(currentStates))
            
         newStates = {}
         for state in currentStates:
            distance = currentStates[state]
            for key in self.keyPositions:
               if key in state.keys:
                  continue
                  
               distToKey, requiredKeys = self.cachedDistances[(state.pos, key)]
               
               hasNeededKeys = True
               for reqKey in requiredKeys:
                  if reqKey not in state.keys:
                     hasNeededKeys = False
                     break
                     
               if not hasNeededKeys:
                  continue
               
               newState = PathState()
               #copy data, add new stuff
               newState.keys = state.keys.copy()
               newState.keys.add(key)
               if len(newState.keys) < i+1:
                  print "uh oh"
                  print state.keys
                  print key
               newState.pos = key
               newDistance = distance + distToKey
               
               if newState in newStates:
                  oldDistance = newStates[newState]
                  if newDistance < oldDistance:
                     newStates[newState] = newDistance
               else:
                     newStates[newState] = newDistance
         currentStates = newStates
      for state in currentStates:
         print str(state.keys) + " " + str(state.pos) + " " + str(currentStates[state])
      shortestState = None
      shortestDistance = 999999999
      for state in currentStates:
         if currentStates[state] < shortestDistance:
            shortestDistance = currentStates[state]
            shortestState = state
      print shortestDistance

   def FindShortestPathOld(self):
      pos = self.GetStartPos()
      numKeys = self.GetNumKeys()
      
      #state vector, position
      startState = PathState()
      startState.keys = set()
      startState.pos = pos
      
      currentStates = {}
      currentStates[startState] = 0
      
      for i in xrange(numKeys):
         print str(i) + ": " + str(len(currentStates))
         bestDistanceSoFar = 99999999
         for state in currentStates:
            distance = currentStates[state]
            if distance < bestDistanceSoFar:
               bestDistanceSoFar = distance
            
         cutoffDistance = bestDistanceSoFar+500
            
         newStates = {}
         for state in currentStates:
            distance = currentStates[state]
            nextKeys = self.GetReachableKeysFromPosition(state.keys, state.pos)
            for key in nextKeys:
               distToKey = nextKeys[key]
               
               newState = PathState()
               #copy data, add new stuff
               newState.keys = state.keys.copy()
               newState.keys.add(key)
               newState.pos = self.keyPositions[key]
               newDistance = distance + distToKey
               
               if newDistance < cutoffDistance:
                  if newState in newStates:
                     oldDistance = newStates[newState]
                     if newDistance < oldDistance:
                        newStates[newState] = newDistance
                  else:
                        newStates[newState] = newDistance
         currentStates = newStates
      for state in currentStates:
         print str(state.keys) + " " + str(currentStates[state])
      

mapData = MapData()
mapStr = ""
with open("input.txt", "r") as FILE:
   mapStr = FILE.read()
   
#mapStr = 
"""########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################"""
mapData.FromString(mapStr)
   
   
p1 = PathState()
p1.pos = '@'
p1.keys = set()
p1.keys.add('a')
p1.keys.add('b')

p2 = PathState()
p2.pos = '@'
p2.keys = set()
p2.keys.add('a')
p2.keys.add('b')

stateSet = set()
stateSet.add(p1)
print p1 in stateSet
print p2 in stateSet

print mapData.ToString()
mapData.FillGaps()
print " "
print mapData.ToString()
#print mapData.cachedDistances[('@','m')]
"""startPos = mapData.GetStartPos()
keySet = set()
keySet.add('a')
keySet.add('f')
keySet.add('z')
keySet.add('i')
print mapData.GetReachableKeysFromPosition(keySet, startPos)"""
mapData.FindShortestPath()