class Password:
    def __init__(self):
        self.min = 0
        self.max = 0
        self.char = ''
        self.password = ''
    def IsValidA(self):
        count = self.password.count(self.char)
        return count >= self.min and count <= self.max
    def IsValidB(self):
        char1 = self.password[self.min]
        char2 = self.password[self.max]
        return (char1 == self.char) ^ (char2 == self.char)

input = []
with open("input.txt") as FILE:
    for line in FILE:
        pw = Password()
        
        dashIdx = line.find('-')
        firstSpaceIdx = line.find(' ')
        
        pw.min = int(line[:dashIdx])
        pw.max = int(line[dashIdx+1:firstSpaceIdx])
        pw.char = line[firstSpaceIdx+1]
        pw.password = line[firstSpaceIdx+3:]
        input.append(pw)
        
#Part a
validCount = 0
for pw in input:
    if pw.IsValidA():
        validCount += 1
print(validCount)

#Part a
validCount = 0
for pw in input:
    if pw.IsValidB():
        validCount += 1
print(validCount)