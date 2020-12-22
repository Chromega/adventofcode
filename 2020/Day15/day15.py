class NumberGame():
    def __init__(self):
        self.lastTimeNumberSpoken = {}
        self.mostRecentNumber = 0
        self.count = 0
        pass
        
    def AppendNumber(self, number):
        self.lastTimeNumberSpoken[self.mostRecentNumber] = self.count
        self.mostRecentNumber = number
        self.count += 1
        
    def GenerateNextNumber(self):
        if self.mostRecentNumber in self.lastTimeNumberSpoken:
            nextNum = self.count - self.lastTimeNumberSpoken[self.mostRecentNumber]
        else:
            nextNum = 0
        self.AppendNumber(nextNum)
        
    def GetCount(self):
        return self.count
        
input = NumberGame()
with open("input.txt") as FILE:
    for line in FILE:
        line = line.strip()
        for token in line.split(','):
            input.AppendNumber(int(token))
    


#part a 15:17
while input.GetCount() < 30000000:
    if input.GetCount()%1000000==0:
        print(input.GetCount())
    input.GenerateNextNumber()
print(input.mostRecentNumber)