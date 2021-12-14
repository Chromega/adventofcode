startSequence = []
substitutions = {}

READ_SEQUENCE=0
READ_SUBSTITUTIONS=1
inputMode = READ_SEQUENCE
with open("input.txt") as FILE:
    for line in FILE.readlines():
        line = line.strip()
        if inputMode == READ_SEQUENCE:
            if len(line)==0:
                inputMode = READ_SUBSTITUTIONS
            else:
                startSequence = list(line)
        else:
            tokens = line.split(' -> ')
            substitutions[tokens[0]] = tokens[1]

#part a
currentSequence = startSequence
for step in range(10):
    newElements = []
    for i in range(0,len(currentSequence)-1):
        pair = ''.join(currentSequence[i:i+2])
        newElements += substitutions[pair]
    newSequence = currentSequence+newElements
    newSequence[::2] = currentSequence
    newSequence[1::2] = newElements
    currentSequence = newSequence

from collections import Counter
counter = Counter(currentSequence)
sorted = counter.most_common()
print(sorted[0][1]-sorted[-1][1])

#part b, aww peas
#assumption: start and end character unchanged (for resolving boundary conditions. appears to always be B...N for input)
startingPairs = Counter()
for i in range(0,len(startSequence)-1):
    pair = ''.join(startSequence[i:i+2])
    startingPairs[pair]+=1

currentPairs = startingPairs
for step in range(40):
    newPairs = Counter()
    for pair, value in currentPairs.items():
        newChar = substitutions[pair]
        newPairs[pair[0]+newChar] += value
        newPairs[newChar+pair[1]] += value
    currentPairs = newPairs
    
elementCounter = Counter()
for pair, count in currentPairs.items():
    for c in pair:
        elementCounter[c] += count
sorted = elementCounter.most_common()

def GetHalvedCount(count):
    if count%2 == 1:
        return count//2+1
    else:
        return count//2

print(GetHalvedCount(sorted[0][1])-GetHalvedCount(sorted[-1][1]))