
input = []
with open("input.txt") as FILE:
    for line in FILE:
        line = line.strip()
        input.append(int(line))

        
#part a 3:45
sortedInput = input[:]
sortedInput.sort()

lastVal = 0
num1 = 0
num3 = 1 #final step
for i in range(len(sortedInput)):
    difference = sortedInput[i]-lastVal
    lastVal = sortedInput[i]
    if difference == 1:
        num1 += 1
    elif difference == 3:
        num3 += 1
        
print(num1*num3)

#part b 15:47
sortedInput.append(0)
sortedInput.sort()
numPossibilitiesFromVal = {}
numPossibilitiesFromVal[sortedInput[len(sortedInput)-1]+3] = 1
for i in range(len(sortedInput)):
    joltage = sortedInput[len(sortedInput)-1-i]
    possibilities = 0
    for j in range(1,4):
        testJoltage = joltage+j
        if testJoltage in numPossibilitiesFromVal:
            possibilities += numPossibilitiesFromVal[testJoltage]
    numPossibilitiesFromVal[joltage] = possibilities
print(numPossibilitiesFromVal[0])