with open("input.txt") as FILE:
    for line in FILE.readlines():
        line = line.strip()
        tokens = line.split(' ')
        minX,maxX = [int(x) for x in tokens[2][2:-1].split('..')]
        minY,maxY = [int(x) for x in tokens[3][2:].split('..')]
        
#part a
def Step(pos,vel):
    newPos = (pos[0]+vel[0],pos[1]+vel[1])
    xVel = vel[0]
    if xVel > 0:
        xVel -= 1
    newVel = (xVel,vel[1]-1)
    return (newPos,newVel)
    
def SimulateUntilInBox(vel,minX,maxX,minY,maxY):
    pos = (0,0)
    while pos[0]<=maxX and pos[1]>=minY:
        pos,vel = Step(pos,vel)
        if pos[0] >= minX and pos[0] <= maxX and pos[1] >= minY and pos[1] <= maxY:
            return True
    return False
    
    
maxYVel = abs(minY)
maxXVel = maxX

#part a
found = False
for yVel in range(maxYVel,0,-1):
    for xVel in range(maxXVel):
        if SimulateUntilInBox((xVel,yVel),minX,maxX,minY,maxY):
            print(((yVel+1)*yVel)//2)
            found = True
            break
    if found:
        break
        
#part b
count = 0
for yVel in range(-maxYVel,maxYVel+1):
    for xVel in range(maxXVel+1):
        if SimulateUntilInBox((xVel,yVel),minX,maxX,minY,maxY):
            count += 1
print(count)