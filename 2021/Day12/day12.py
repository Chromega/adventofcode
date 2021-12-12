class Node:
    def __init__(self,name):
        self.name = name
        self.neighborNames = []
        
def GetOrMakeNode(graph, name):
    if name in graph:
        return graph[name]
    else:
        node = Node(name)
        graph[name] = node
        return node
        
def IsSmallCave(name):
    return name.lower() == name
        
input = {}

with open("input.txt") as FILE:
    for line in FILE.readlines():
        nodeNames = line.strip().split('-')
        leftNode = GetOrMakeNode(input, nodeNames[0])
        rightNode = GetOrMakeNode(input, nodeNames[1])
        leftNode.neighborNames.append(nodeNames[1])
        rightNode.neighborNames.append(nodeNames[0])
       
#part a
def FindPaths(pathSoFar,graph):
    currentNode = graph[pathSoFar[-1]]
    if currentNode.name == "end":
        return [pathSoFar]
    newPaths = []
    for neighborName in currentNode.neighborNames:
        if IsSmallCave(neighborName) and neighborName in pathSoFar:
            continue
        pathsFromNeighbor = FindPaths(pathSoFar+[neighborName],graph)
        newPaths.extend(pathsFromNeighbor)
    return newPaths
    
print(len(FindPaths(["start"],input)))


#part b
def FindPaths(pathSoFar,graph,hasUsedDouble):
    currentNode = graph[pathSoFar[-1]]
    if currentNode.name == "end":
        return [pathSoFar]
    newPaths = []
    for neighborName in currentNode.neighborNames:
        justAddedDouble = False
        if IsSmallCave(neighborName) and neighborName in pathSoFar:
            if hasUsedDouble or neighborName == "start" or neighborName == "end":
                continue
            else:
                justAddedDouble = True
        pathsFromNeighbor = FindPaths(pathSoFar+[neighborName],graph, hasUsedDouble or justAddedDouble)
        newPaths.extend(pathsFromNeighbor)
    return newPaths
    
print(len(FindPaths(["start"],input, False)))