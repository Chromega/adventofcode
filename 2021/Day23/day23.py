import heapq

valueToCost = {}
valueToCost['A'] = 1
valueToCost['B'] = 10
valueToCost['C'] = 100
valueToCost['D'] = 1000

class Node():
    def __init__(self):
        pass

class HallwayNode(Node):
    def __init__(self,stateIndex):
        Node.__init__(self)
        self.pathsToSideRooms = {}
        self.stateIndex = stateIndex
    def AddPathToSideRoom(self,path):
        destination = path[-1].targetType
        self.pathsToSideRooms[destination] = path
        
        sideRoomPath = list(reversed(path))[1:]+[self]
        sideRoomPath = tuple(sideRoomPath)
        path[-1].AddPathToHallway(sideRoomPath)
        
    def GetCurrentVal(self,state):
        return state[self.stateIndex]
        
    def IsOccupied(self,state):
        return state[self.stateIndex]!=''
        
    def GetPossibleNextMoves(self,state):
        if not self.IsOccupied(state):
            return []
        val = self.GetCurrentVal(state)
        path = self.pathsToSideRooms[val]
        sideRoom = path[-1]
        
        if not sideRoom.CanEnter(state):
            return []
            
        for i in range(len(path)-1):
            if path[i] is not None and path[i].IsOccupied(state):
                return []
        
        newState = list(state)
        newState[self.stateIndex] = ''
        newState[sideRoom.GetFirstOpenStateIndex(state)] = val
        return [(tuple(newState),(len(path)+sideRoom.CountEmptySpacesInRoom(state)-1)*valueToCost[val])]
    
class SideRoomNode(Node):
    def __init__(self,targetType,size,stateIndex):
        Node.__init__(self)
        self.targetType = targetType
        self.hallwayPaths = []
        self.size = size
        self.stateIndex = stateIndex
    def AddPathToHallway(self,path):
        self.hallwayPaths.append(path)
    def CanEnter(self,state):
        complete = True
        for i in range(self.stateIndex,self.stateIndex+self.size):
            if state[i] != self.targetType and state[i] != '':
                return False
            if state[i] == '':
                complete = False
        return not complete
    def CountEmptySpacesInRoom(self,state):
        count = 0
        for i in range(self.stateIndex,self.stateIndex+self.size):
            if state[i] == '':
                count += 1
            else:
                break
        return count
    def GetFirstOpenStateIndex(self,state):
        return self.GetTopStateIndex(state)-1
    def GetTopStateIndex(self,state):
        for i in range(self.stateIndex,self.stateIndex+self.size):
            if state[i] != '':
                return i
        return self.stateIndex+self.size
    def GetPossibleNextMoves(self,state):
        complete = True
        empty = True
        for i in range(self.stateIndex,self.stateIndex+self.size):
            if state[i] != '':
                empty = False
            if state[i] != self.targetType:
                complete = False
        if complete or empty:
            return []
            
        idx = self.GetTopStateIndex(state)
        val = state[idx]
        
        nextMoves = []
        for path in self.hallwayPaths:
            clearPath = True
            for n in path:
                if n is not None and n.IsOccupied(state):
                    clearPath = False
                    break
            if not clearPath:
                continue
            newState = list(state)
            newState[path[-1].stateIndex] = val
            newState[idx] = ""
            cost = (len(path)+self.CountEmptySpacesInRoom(state))*valueToCost[val]
            nextMoves.append((tuple(newState),cost))
        return nextMoves
    
farLeftNode = HallwayNode(0)
nearLeftNode = HallwayNode(1)
abNode = HallwayNode(2)
bcNode = HallwayNode(3)
cdNode = HallwayNode(4)
nearRightNode = HallwayNode(5)
farRightNode = HallwayNode(6)

aNode = SideRoomNode("A",2,7)
bNode = SideRoomNode("B",2,9)
cNode = SideRoomNode("C",2,11)
dNode = SideRoomNode("D",2,13)

nodes = [farLeftNode,nearLeftNode,abNode,bcNode,cdNode,nearRightNode,farRightNode,aNode,bNode,cNode,dNode]

#Monument of shame
farLeftNode.AddPathToSideRoom((nearLeftNode,None,aNode))
farLeftNode.AddPathToSideRoom((nearLeftNode,None,abNode,None,bNode))
farLeftNode.AddPathToSideRoom((nearLeftNode,None,abNode,None,bcNode,None,cNode))
farLeftNode.AddPathToSideRoom((nearLeftNode,None,abNode,None,bcNode,None,cdNode,None,dNode))

nearLeftNode.AddPathToSideRoom((None,aNode,))
nearLeftNode.AddPathToSideRoom((None,abNode,None,bNode))
nearLeftNode.AddPathToSideRoom((None,abNode,None,bcNode,None,cNode))
nearLeftNode.AddPathToSideRoom((None,abNode,None,bcNode,None,cdNode,None,dNode))

abNode.AddPathToSideRoom((None,aNode,))
abNode.AddPathToSideRoom((None,bNode,))
abNode.AddPathToSideRoom((None,bcNode,None,cNode))
abNode.AddPathToSideRoom((None,bcNode,None,cdNode,None,dNode))

bcNode.AddPathToSideRoom((None,abNode,None,aNode))
bcNode.AddPathToSideRoom((None,bNode,))
bcNode.AddPathToSideRoom((None,cNode,))
bcNode.AddPathToSideRoom((None,cdNode,None,dNode))

cdNode.AddPathToSideRoom((None,bcNode,None,abNode,None,aNode))
cdNode.AddPathToSideRoom((None,bcNode,None,bNode))
cdNode.AddPathToSideRoom((None,cNode,))
cdNode.AddPathToSideRoom((None,dNode,))

nearRightNode.AddPathToSideRoom((None,cdNode,None,bcNode,None,abNode,None,aNode))
nearRightNode.AddPathToSideRoom((None,cdNode,None,bcNode,None,bNode))
nearRightNode.AddPathToSideRoom((None,cdNode,None,cNode))
nearRightNode.AddPathToSideRoom((None,dNode,))

farRightNode.AddPathToSideRoom((nearRightNode,None,cdNode,None,bcNode,None,abNode,None,aNode))
farRightNode.AddPathToSideRoom((nearRightNode,None,cdNode,None,bcNode,None,bNode))
farRightNode.AddPathToSideRoom((nearRightNode,None,cdNode,None,cNode))
farRightNode.AddPathToSideRoom((nearRightNode,None,dNode))

def PrintState(state):
    s = """#############
#01.2.3.4.56#
###7#9#b#d###
  #8#a#c#e#
  #########"""
    stateNoEmpty = ['.' if x =='' else x for x in state]
    s = s.replace('0',stateNoEmpty[0])
    s = s.replace('1',stateNoEmpty[1])
    s = s.replace('2',stateNoEmpty[2])
    s = s.replace('3',stateNoEmpty[3])
    s = s.replace('4',stateNoEmpty[4])
    s = s.replace('5',stateNoEmpty[5])
    s = s.replace('6',stateNoEmpty[6])
    s = s.replace('7',stateNoEmpty[7])
    s = s.replace('8',stateNoEmpty[8])
    s = s.replace('9',stateNoEmpty[9])
    s = s.replace('a',stateNoEmpty[10])
    s = s.replace('b',stateNoEmpty[11])
    s = s.replace('c',stateNoEmpty[12])
    s = s.replace('d',stateNoEmpty[13])
    s = s.replace('e',stateNoEmpty[14])
    print('')
    print(s)

#startState = ('','','','','','','','B','A','C','D','B','C','D','A') #PART A TEST
startState = ('','','','','','','','B','C','B','A','D','D','A','C')
endState = ('','','','','','','','A','A','B','B','C','C','D','D') 

"""def djikstra(graph,start, end):
    queue,seen = [(0, start, None)], set()
    while True:
        (cost, state, prev) = heapq.heappop(queue)
        if state not in seen:
            seen.add(state)
            if state == end:
                
                return cost
                
            newStates = []
            for node in graph:
                newStates.extend(node.GetPossibleNextMoves(state))
                
            for newState,addedCost in newStates:
                if newState in seen:
                    continue
                    
                heapq.heappush(queue, (cost + addedCost, newState, state))"""
                
def dijkstra(graph, start, end):
    q, seen, mins = [(0,start,[])], set(), {start: 0}
    while q:
        (cost,state,path) = heapq.heappop(q)
        if state not in seen:
            seen.add(state)
            path = [state] + path
            if state == end: return (cost, path)

            newStates = []
            for node in graph:
                newStates.extend(node.GetPossibleNextMoves(state))
                
            for newState,addedCost in newStates:
                if newState in seen: continue
                prev = mins.get(newState, None)
                next = cost + addedCost
                if prev is None or next < prev:
                    mins[newState] = next
                    heapq.heappush(q, (next, newState, path))

    return float("inf"), None

cost,path = dijkstra(nodes,startState,endState)
for state in path:
    PrintState(state)
print(cost)

#part b
#startState = ('','','','','','','','B','D','D','A','C','C','B','D','B','B','A','C','D','A','C','A')
startState = ('','','','','','','','B','D','D','C','B','C','B','A','D','B','A','D','A','A','C','C')
endState = ('','','','','','','','A','A','A','A','B','B','B','B','C','C','C','C','D','D','D','D') 
aNode.size = 4
bNode.size = 4
bNode.stateIndex = 11
cNode.size = 4
cNode.stateIndex = 15
dNode.size = 4
dNode.stateIndex = 19

cost,path = dijkstra(nodes,startState,endState)
print(cost)