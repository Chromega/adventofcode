class Key:
    def __init__(self):
        self.publicKey = 0
        self.loopSize = 1
        
    def Transform(self, subjectNumber):
        value = 1
        for i in range(self.loopSize):
            value = self.TransformStep(subjectNumber, value)
        return value
        
    def TransformStep(self, subjectNumber, currentValue):
        currentValue *= subjectNumber
        currentValue %= 20201227
        return currentValue
        
    def DetermineLoopSizeFromPublicKey(self):
        self.loopSize = 1
        value = 1
        while True:
            value = self.TransformStep(7, value)
            if value == self.publicKey:
                break
            self.loopSize += 1
        return self.loopSize

card = Key()
door = Key()
with open("input.txt") as FILE:
    card.publicKey = int(FILE.readline().strip())
    door.publicKey = int(FILE.readline().strip())
        
print(card.DetermineLoopSizeFromPublicKey())
print(door.DetermineLoopSizeFromPublicKey())

print(card.Transform(door.publicKey))