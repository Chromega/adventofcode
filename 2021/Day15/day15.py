import heapq

input = []

with open("input.txt") as FILE:
    for line in FILE.readlines():
        row = []
        for c in line.strip():
            row.append(int(c))
        input.append(row)
        
def TryGetPoint(matrix,coord):
    y = coord[1]
    x = coord[0]
    if y < 0 or y >= len(matrix):
        return (False,0)
    row = matrix[y]
    if x < 0 or x >= len(matrix[0]):
        return (False,0)
    return (True,matrix[y][x])
    
UP = (0,-1)
DOWN = (0,1)
LEFT = (-1,0)
RIGHT = (1,0)
cardinalDirections = (DOWN,RIGHT,LEFT,UP)

def AddCoordinates2D(c1,c2):
    return (c1[0]+c2[0],c1[1]+c2[1])
    
#part a
def djikstra(graph, start, end):
    queue,seen = [(0, start, None)], set()
    while True:
        (cost, v, prev) = heapq.heappop(queue)
        if v not in seen:
            seen.add(v)
            if v == end:
                return cost
                
            for direction in cardinalDirections:
                neighbor = AddCoordinates2D(v, direction)
                exists, neighborCost = TryGetPoint(graph, neighbor)
                if not exists:
                    continue
                heapq.heappush(queue, (cost + neighborCost, neighbor, v))
                
endPos = (len(input)-1,len(input[0])-1)
print(djikstra(input, (0,0), endPos))

#part b
bigInput = []
for i in range(5):
    for row in input:
        bigRow = []
        for j in range(5):
            bigRow.extend([(x+i+j+8)%9+1 for x in row])
        bigInput.append(bigRow)
endPos = (len(bigInput)-1,len(bigInput[0])-1)
print(djikstra(bigInput, (0,0), endPos))