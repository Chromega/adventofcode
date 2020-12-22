class GameState:
    def __init__(self):
        self.player1Hand = []
        self.player2Hand = []
    def Copy(self):
        copy = GameState()
        copy.player1Hand = self.player1Hand[:]
        copy.player2Hand = self.player2Hand[:]
        return copy
    def GetHand(self, playerIdx):
        if playerIdx == 1:
            return self.player1Hand
        else:
            return self.player2Hand
    def IsGameOver(self):
        return len(self.player1Hand) == 0 or len(self.player2Hand) == 0
    def GetWinner(self):
        if len(self.player1Hand) == 0:
            return 2
        elif len(self.player2Hand) == 0:
            return 1
        else:
            return 0
    def GetScore(self, playerIdx):
        hand = self.GetHand(playerIdx)
        score = 0
        for i in range(len(hand)):
            score += hand[i]*(len(hand)-i)
        return score
        
    def GetTuple(self):
        bigList = self.player1Hand + [999,] + self.player2Hand
        return tuple(bigList)
        
    def Equals(self, other):
        if (len(self.player1Hand) != len(other.player1Hand)) or (len(self.player2Hand) != len(other.player2Hand)):
            return False
        for i in range(len(self.player1Hand)):
            if self.player1Hand[i] != other.player1Hand[i]:
                return False
        for i in range(len(self.player2Hand)):
            if self.player2Hand[i] != other.player2Hand[i]:
                return False
        return True
        
GAME_NUM = 1
class Game:
    def __init__(self, startingState):
        self.gameState = startingState
        self.stateHistory = set()
        self.earlyWinner = 0
        self.roundNum = 0
        global GAME_NUM
        self.gameNum = GAME_NUM
        GAME_NUM += 1
        #print("")
        #print("=== Game " + str(self.gameNum) + " ===")
        
    def HasStateInHistory(self, gameState):
        return gameState.GetTuple() in self.stateHistory
            
        
    def StepStateA(self):
        card1 = self.gameState.player1Hand.pop(0)
        card2 = self.gameState.player2Hand.pop(0)
        
        if card1 > card2:
            self.gameState.player1Hand.append(card1)
            self.gameState.player1Hand.append(card2)
        else:
            self.gameState.player2Hand.append(card2)
            self.gameState.player2Hand.append(card1)
            
    def StepStateB(self):
        self.roundNum += 1
        #print("")
        #print("-- Round " + str(self.roundNum) + " (Game " + str(self.gameNum) + ") --")
        #print("Player 1's deck: " + str(self.gameState.player1Hand))
        #print("Player 2's deck: " + str(self.gameState.player2Hand))
        
        if self.HasStateInHistory(self.gameState):
            self.earlyWinner = 1
            #print("Duplicate state, Player 1 wins")
            return
        self.stateHistory.add(self.gameState.GetTuple())
    
        card1 = self.gameState.player1Hand.pop(0)
        card2 = self.gameState.player2Hand.pop(0)
        #print("Player 1 plays: " + str(card1))
        #print("Player 2 plays: " + str(card2))
        
        if len(self.gameState.player1Hand) >= card1 and len(self.gameState.player2Hand) >= card2:
            subGameState = GameState()
            subGameState.player1Hand = self.gameState.player1Hand[:card1]
            subGameState.player2Hand = self.gameState.player2Hand[:card2]
            subGame = Game(subGameState)
            #print('Playing a sub-game to determine the winner...')
            #print('')
            winner = subGame.PlayUntilWinnerB()
            #print("The winner of game " + str(subGame.gameNum) + " is player " + str(winner) + " !")
            #print("")
            #print("...anyway, back to game " + str(self.gameNum))
        elif card1 > card2:
            winner = 1
        else:
            winner = 2
        
        if winner == 1:
            self.gameState.player1Hand.append(card1)
            self.gameState.player1Hand.append(card2)
            #print("Player 1 wins round " + str(self.roundNum) + " of game " + str(self.gameNum) + "!")
        else:
            self.gameState.player2Hand.append(card2)
            self.gameState.player2Hand.append(card1)
            
            
    def IsGameOver(self):
        if self.earlyWinner != 0:
            return True
        return self.gameState.IsGameOver()
        
    def GetWinner(self):
        if self.earlyWinner != 0:
            return self.earlyWinner
        return self.gameState.GetWinner()
            
    def PlayUntilWinnerA(self):
        while not self.IsGameOver():
            self.StepStateA()
        winnerIdx = self.GetWinner()
        return winnerIdx
        
    def PlayUntilWinnerB(self):
        while not self.IsGameOver():
            self.StepStateB()
        winnerIdx = self.GetWinner()
        return winnerIdx
        
startingState = GameState()
currentPlayer = 0
with open("input.txt") as FILE:
    for line in FILE:
        line = line.strip()
        if len(line) == 0:
            continue
        if line.startswith("Player"):
            currentPlayer += 1
        else:
            card = int(line)
            startingState.GetHand(currentPlayer).append(card)
        
#part a
"""
partAGame = Game(startingState.Copy())
winnerIdx = partAGame.PlayUntilWinnerA()
print(partAGame.gameState.GetScore(winnerIdx))"""

#part b
partBGame = Game(startingState.Copy())
winnerIdx = partBGame.PlayUntilWinnerB()

print(partBGame.GetWinner())
print(partBGame.gameState.GetHand(partBGame.GetWinner()))

print(partBGame.gameState.GetScore(winnerIdx))
    