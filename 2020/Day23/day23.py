CUPS_TO_PICK_UP = 3

def Mod(x, m):
    while x < 0:
        x += m
    return x%m

class GameStateA:
    def __init__(self):
        self.cups = []
        self.currentIdx = 0
    def GetCupFromCurrent(self, relativeIdx):
        absoluteIdx = Mod(self.currentIdx+relativeIdx, len(self.cups))
        return (self.cups[absoluteIdx],absoluteIdx)
    def GetCurrentCup(self):
        return self.cups[self.currentIdx]
    def Copy(self):
        copy = GameStateA()
        copy.cups = self.cups[:]
        copy.currentIdx = self.currentIdx
        return copy
        
class GameA:
    def __init__(self):
        self.state = None
        self.pickedUp = []
        for i in range(CUPS_TO_PICK_UP):
            self.pickedUp.append(0)
        
    def StepState(self):
        destination = self.FindDestination(self.state)
        stopShiftingIdx = (destination+1)%len(self.state.cups)        
        count = len(self.state.cups)
        for i in range(1,count):
            (cup, absIdx) = self.state.GetCupFromCurrent(i)
            if i < (1+CUPS_TO_PICK_UP):
                self.pickedUp[i-1]=cup
            if absIdx == stopShiftingIdx:
                break
            (newCup, newAbsIdx) = self.state.GetCupFromCurrent(i+CUPS_TO_PICK_UP)
            self.state.cups[absIdx] = newCup
        for i in range(CUPS_TO_PICK_UP):
            absoluteIdx = Mod(destination-CUPS_TO_PICK_UP+i+1, len(self.state.cups))
            self.state.cups[absoluteIdx] = self.pickedUp[i]
        self.state.currentIdx = Mod(self.state.currentIdx+1, len(self.state.cups))

        
    def FindDestination(self, state):
        count = len(state.cups)
        startingCup = state.GetCurrentCup()
        
        bestDistance = count
        bestCupIdx = 0
        for i in range(CUPS_TO_PICK_UP+1, count):
            (cup, idx) = state.GetCupFromCurrent(i)
            distance = startingCup-cup
            if distance < 0:
                distance += count
            if distance < bestDistance:
                bestDistance = distance
                bestCupIdx = idx
        return bestCupIdx
            
        
startingState = GameStateA()
with open("input.txt") as FILE:
    for line in FILE:
        line = line.strip()
        if len(line) == 0:
            continue
        startingState.cups = [int(c) for c in line]
        
#Part A
game = GameA()
game.state = startingState.Copy()
for i in range(100):
    game.StepState()
oneIdx = game.state.cups.index(1)
answer = ""
for i in range(1,len(game.state.cups)):
    absIdx = Mod(i+oneIdx, len(game.state.cups))
    answer += str(game.state.cups[absIdx])
print(answer)















#Part B
#Not good enough asymptotically, new plan with linked lists
class Cup:
    def __init__(self):
        self.prev = None
        self.next = None
        self.val = 0
        
class GameB:
    def __init__(self, cupVals):
        self.cups = {} #int value->Cup
        self.currentCup = None #Cup
        self.pickupCupHead = None #Cup, first in sequence
        
        firstCup = None
        previousCup = None
        for v in cupVals:
            cup = Cup()
            cup.prev = previousCup
            if previousCup:
                previousCup.next = cup
            cup.val = v
            previousCup = cup
            if firstCup is None:
                firstCup = cup
            self.cups[v] = cup
        previousCup.next = firstCup
        firstCup.prev = previousCup
        
        self.currentCup = firstCup
        
    def Step(self):
        self.pickupCupHead = self.currentCup.next
        
        #Find where we are cutting and merging
        firstCupAfterPickup = self.pickupCupHead
        for i in range(CUPS_TO_PICK_UP):
            firstCupAfterPickup = firstCupAfterPickup.next
        lastCupOfPickup = firstCupAfterPickup.prev
            
        #Pickup gets snipped
        self.pickupCupHead.prev = None
        lastCupOfPickup.next = None
        
        #Merge around the snip
        self.currentCup.next = firstCupAfterPickup
        firstCupAfterPickup.prev = self.currentCup
        
        #Find the destination (Only do after we've made the snip)
        destinationCup = self.FindDestination()
        cupAfterInsertion = destinationCup.next
        
        #Now put the snipped area after the destinationCup
        destinationCup.next = self.pickupCupHead
        self.pickupCupHead.prev = destinationCup
        lastCupOfPickup.next = cupAfterInsertion
        cupAfterInsertion.prev = lastCupOfPickup
                
        self.currentCup = self.currentCup.next
        
    def FindDestination(self):
        valToFind = self.currentCup.val
        
        while True:
            valToFind = Mod(valToFind-2, len(self.cups))+1
            pickupCup = self.pickupCupHead
            isInPickup = False
            while True:
                if pickupCup.val == valToFind:
                    isInPickup = True
                    break
                pickupCup = pickupCup.next
                if pickupCup == None:
                    break
            if not isInPickup:
                return self.cups[valToFind]
            

cupVals = []
with open("input.txt") as FILE:
    for line in FILE:
        line = line.strip()
        if len(line) == 0:
            continue
        cupVals = [int(c) for c in line]
        
#Part B
totalSize = 1000000
for i in range(len(cupVals)+1, totalSize+1):
    cupVals.append(i)

game = GameB(cupVals)
for i in range(10000000):
    if i%1000000==0:
        print(i)
    game.Step()
cup = game.cups[1]
answer = 1
for i in range(2):
    cup = cup.next
    answer *= cup.val
print(answer)
