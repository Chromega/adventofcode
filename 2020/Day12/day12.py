import copy

EAST = 0
NORTH = 1
WEST = 2
SOUTH = 3
NUM_ABSOLUTE_DIRECTIONS = 4
LEFT = 4
RIGHT = 5
FORWARD = 6

def DirectionToVector(direction):
    if direction == NORTH:
        return (0,1)
    elif direction == SOUTH:
        return (0,-1)
    elif direction == EAST:
        return (1,0)
    elif direction == WEST:
        return (-1,0)
    else:
        print("Invalid direction: " + str(direction))
    
def Turn(initialDirection, turnDirection, turnDegrees):
    if turnDirection == RIGHT:
        turnDegrees *= -1
        
    numTurns = round(turnDegrees/90)
    
    while numTurns < 0:
        numTurns += NUM_ABSOLUTE_DIRECTIONS
    
    direction = (initialDirection + numTurns)%NUM_ABSOLUTE_DIRECTIONS
    
    return direction
    
def TurnVec(vec, turnDegrees):
    numTurns = round(turnDegrees/90)
    
    retVec = vec[:]
    
    while numTurns < 0:
        numTurns += NUM_ABSOLUTE_DIRECTIONS
        
    for i in range(numTurns):
        tempX = retVec[0]
        tempY = retVec[1]
        retVec[1] = tempX
        retVec[0] = -tempY
        
    return retVec
    

class Agent:
    def __init__(self):
        self.facing = EAST
        self.pos = [0,0]
        self.waypoint = [10,1]
        
    def MoveA(self, direction, magnitude):
        if direction < NUM_ABSOLUTE_DIRECTIONS:
            vec = DirectionToVector(direction)
            self.pos[0] += vec[0]*magnitude
            self.pos[1] += vec[1]*magnitude
        elif direction == LEFT or direction == RIGHT:
            self.facing = Turn(self.facing, direction, magnitude)
        elif direction == FORWARD:
            vec = DirectionToVector(self.facing)
            self.pos[0] += vec[0]*magnitude
            self.pos[1] += vec[1]*magnitude
            
    def MoveB(self, direction, magnitude):
        if direction < NUM_ABSOLUTE_DIRECTIONS:
            vec = DirectionToVector(direction)
            self.waypoint[0] += vec[0]*magnitude
            self.waypoint[1] += vec[1]*magnitude
        elif direction == LEFT or direction == RIGHT:
            delta = [self.waypoint[0]-self.pos[0],self.waypoint[1]-self.pos[1]]
            if direction == RIGHT:
                magnitude *= -1
            newDelta = TurnVec(delta, magnitude)
            self.waypoint[0] = self.pos[0]+newDelta[0]
            self.waypoint[1] = self.pos[1]+newDelta[1]
        elif direction == FORWARD:
            delta = [self.waypoint[0]-self.pos[0],self.waypoint[1]-self.pos[1]]
            self.pos[0] += delta[0]*magnitude
            self.pos[1] += delta[1]*magnitude
            self.waypoint[0] += delta[0]*magnitude
            self.waypoint[1] += delta[1]*magnitude
            
            
  
input = []
with open("input.txt") as FILE:
    for line in FILE:
        line = line.strip()
        directionStr = line[0]
        magnitude = int(line[1:])
        
        if directionStr == "E":
            direction = EAST
        if directionStr == "N":
            direction = NORTH
        if directionStr == "W":
            direction = WEST
        if directionStr == "S":
            direction = SOUTH
        if directionStr == "L":
            direction = LEFT
        if directionStr == "R":
            direction = RIGHT
        if directionStr == "F":
            direction = FORWARD
            
        input.append((direction, magnitude))
        
    

        
#part a 18:00
agent = Agent()
for instruction in input:
    agent.MoveA(instruction[0], instruction[1])
print(abs(agent.pos[0])+abs(agent.pos[1]))

#part b 29:00
agent = Agent()
for instruction in input:
    agent.MoveB(instruction[0], instruction[1])
print(abs(agent.pos[0])+abs(agent.pos[1]))
    