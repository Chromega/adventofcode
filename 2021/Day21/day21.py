startingPositions = {}
with open("input.txt") as FILE:
    currentScanner = None
    for line in FILE.readlines():
        line = line.strip()
        tokens = line.split(' ')
        playerNum = int(tokens[1])
        position = int(tokens[4])
        startingPositions[playerNum] = position

class DeterministicDice():
    def __init__(self,size):
        self.size = size
        self.nextRoll = 1
        self.totalRolls = 0
    def Roll(self):
        current = self.nextRoll
        self.nextRoll = current%100+1
        self.totalRolls += 1
        return current
        
class Player():
    def __init__(self, index, position):
        self.index = index
        self.score = 0
        self.position = position
    def AdvanceAndScore(self, move):
        self.position = (self.position+move-1)%10+1
        self.score += self.position
        
#part a
player1 = Player(1,startingPositions[1])
player2 = Player(2,startingPositions[2])
players = [player1,player2]

dice = DeterministicDice(100)
playerTurn = 0
lastTurn = 1
while players[lastTurn].score < 1000:
    move = dice.Roll()+dice.Roll()+dice.Roll()
    players[playerTurn].AdvanceAndScore(move)
    lastTurn = playerTurn
    playerTurn = (lastTurn+1)%len(players)

print(min(player1.score,player2.score)*dice.totalRolls)

#part b
cachedOutcomes = {} #(p1Pos, p2Pos, p1Score, p2Score, currentTurn)

def ComputeNumOutcomes(state, cachedOutcomes):
    if state in cachedOutcomes:
        return cachedOutcomes[state]
    p1Pos,p2Pos,p1Score,p2Score,currentTurn = state
    
    #print(state)
    outcomes = [0,0]
    
    if p1Score >= 21:
        outcomes = [1,0]
    elif p2Score >= 21:
        outcomes = [0,1]
    else:
        
        newTurn = (currentTurn+1)%2
        for i in range(1,4):
            for j in range(1,4):
                for k in range(1,4):
                
                    scores = [p1Score,p2Score]
                    positions = [p1Pos,p2Pos]
                    currentPosition = positions[currentTurn]
                    currentScore = scores[currentTurn]
                    
                    move = i+j+k
                    newPosition = (currentPosition+move-1)%10+1
                    newScore = currentScore+newPosition
                    scores[currentTurn] = newScore
                    positions[currentTurn] = newPosition
                    
                    newState = (positions[0],positions[1],scores[0],scores[1],newTurn)
                    nextStepOutcomes = ComputeNumOutcomes(newState,cachedOutcomes)
                    outcomes[0] += nextStepOutcomes[0]
                    outcomes[1] += nextStepOutcomes[1]
    cachedOutcomes[state] = outcomes
    return outcomes
    
for s1 in range(21,-1,-1):
    for s2 in range(21,-1,-1):
        for p1 in range(1,11):
            for p2 in range(1,11):
                for turn in range(2):
                    #print("TOP " + str((p1,p2,s1,s2,turn)))
                    ComputeNumOutcomes((p1,p2,s1,s2,turn),cachedOutcomes)
outcomes = ComputeNumOutcomes((startingPositions[1],startingPositions[2],0,0,0), cachedOutcomes)
print(max(outcomes[0],outcomes[1]))