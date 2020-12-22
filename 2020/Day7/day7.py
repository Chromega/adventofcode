class Bag:
    def __init__(self):
        self.id = ""
        #ids
        self.containsIds = {}
        #refs
        self.contains = {}
        self.containedDirectlyBy = set()
    def AddPredecessors(self, predecessorSet):
        for predecessor in self.containedDirectlyBy:
            isNew = predecessor not in predecessorSet
            predecessorSet.add(predecessor)
            if isNew:
                predecessor.AddPredecessors(predecessorSet)
    def GetSuccessorCount(self):
        successorCount = 0
        for successor in self.contains:
            successorCount += self.contains[successor]*(successor.GetSuccessorCount()+1)
        return successorCount

class BagGraph:
    def __init__(self):
        self.bags = {}
    def GetBag(self, id):
        if id in self.bags:
            return self.bags[id]
        else:
            bag = Bag()
            self.bags[id] = bag
            bag.id = id
            return bag
            
    def GetBagPredecessors(self, testBag):
        predecessors = set()
        testBag.AddPredecessors(predecessors)
        return(predecessors)

input = BagGraph()
with open("input.txt") as FILE:
    for line in FILE:
        line = line.strip()
        firstBagsIdx = line.find(" bags")
        sourceBagId = line[:firstBagsIdx]
        containedBagTokens = line[firstBagsIdx+14:].strip('.').split(',')
        
        sourceBag = input.GetBag(sourceBagId)
        
        for token in containedBagTokens:
            token = token.strip()
            if token == 'no other bags':
                pass#print("empty")
            else:
                firstSpaceIdx = token.find(' ')
                count = int(token[:firstSpaceIdx])
                bagIdx = token.find(' bag')
                bagName = token[firstSpaceIdx+1:bagIdx]
                sourceBag.containsIds[bagName] = count
                input.GetBag(bagName)
    
#resolve refs
for bagId in input.bags:
    bag = input.GetBag(bagId)
    for containedBagId in bag.containsIds:
        bag.contains[input.GetBag(containedBagId)] = bag.containsIds[containedBagId]
    
#reverse graph links
for bagId in input.bags:
    bag = input.GetBag(bagId)
    for containedBagId in bag.containsIds:
        containedBag = input.GetBag(containedBagId)
        containedBag.containedDirectlyBy.add(bag)
        
#part a 32:18
testBagId = 'shiny gold'
testBag = input.GetBag(testBagId)
#print(len(input.GetBagPredecessors(testBag)))

#part b 40:00
print(testBag.GetSuccessorCount())