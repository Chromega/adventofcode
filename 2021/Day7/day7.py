positions = []

with open("input.txt") as FILE:
    for line in FILE.readlines():
        positions = [int(x) for x in line.split(",")]
        
print(len(positions))
            
#part a
minPos = 99999999999
maxPos = -9999999999

for pos in positions:
    if pos < minPos:
        minPos = pos
    if pos > maxPos:
        maxPos = pos
        
bestCost = 999999999999999999
for targetPos in range(minPos,maxPos+1):
    cost = 0
    for crabPos in positions:
        cost += abs(crabPos-targetPos)
    if cost < bestCost:
        bestCost = cost
        
print(bestCost)

#part b
bestCost = 999999999999999999
for targetPos in range(minPos,maxPos+1):
    cost = 0
    for crabPos in positions:
        distance = abs(crabPos-targetPos)
        cost += distance*(distance+1)/2
    if cost < bestCost:
        bestCost = cost
        
print(bestCost)