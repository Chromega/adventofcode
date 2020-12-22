class Passenger:
    def __init__(self):
        self.yes = set()

class Group:
    def __init__(self):
        self.passengers = []
    def GetYesUnion(self):
        output = set()
        for p in self.passengers:
            output = output.union(p.yes)
        return output
    def GetYesIntersection(self):
        output = self.passengers[0].yes
        for p in self.passengers:
            output = output.intersection(p.yes)
        return output

input = []
with open("input.txt") as FILE:
    group = Group()
    for line in FILE:
        line = line.strip()
        if len(line) == 0:
            input.append(group)
            group = Group()
        else:
            passenger = Passenger()
            for c in line:
                passenger.yes.add(c)
            group.passengers.append(passenger)
    if len(group.passengers) > 0:
        input.append(group)
        
    
#Part a 8:30
count = 0
for group in input:
    count += len(group.GetYesUnion())
print(count)

#Part b 9:16
count = 0
for group in input:
    count += len(group.GetYesIntersection())
print(count)