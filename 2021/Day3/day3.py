input = []
with open("input.txt") as FILE:
    lines = FILE.readlines()
    for line in lines:
        input.append([int(x) for x in list(line.strip())])
print(len(input))
numBits = len(input[0])

#part a
gamma = 0
epsilon = 0
for i in range(numBits):
    numOnes = 0
    numZeroes = 0
    for bits in input:
        bit = bits[i]
        if bit == 0:
            numZeroes += 1
        else:
            numOnes += 1
    gamma *= 2
    epsilon *= 2
    if numOnes > numZeroes:
        gamma += 1
    else:
        epsilon += 1
print(gamma*epsilon)


#part b
def CountBitsAtIndex(lst, idx):
    numOnes = 0
    numZeroes = 0
    for bits in lst:
        bit = bits[idx]
        if bit == 0:
            numZeroes += 1
        else:
            numOnes += 1
    return (numZeroes, numOnes)
    
oxygenInput = input[:]
for bitIndex in range(numBits):
    (numZeroes, numOnes) = CountBitsAtIndex(oxygenInput, bitIndex)
    if numZeroes > numOnes:
        oxygenInput = list(filter(lambda x: x[bitIndex]==0, oxygenInput))
    else:
        oxygenInput = list(filter(lambda x: x[bitIndex]==1, oxygenInput))
    if len(oxygenInput)==1:
        break
print(oxygenInput)

co2Input = input[:]
for bitIndex in range(numBits):
    (numZeroes, numOnes) = CountBitsAtIndex(co2Input, bitIndex)
    if numZeroes > numOnes:
        co2Input = list(filter(lambda x: x[bitIndex]==1, co2Input))
    else:
        co2Input = list(filter(lambda x: x[bitIndex]==0, co2Input))
    if len(co2Input)==1:
        break
print(co2Input)

def BitListToInt(lst):
    val = 0
    for bit in lst:
        val *= 2
        val += bit
    return val

oxygen = BitListToInt(oxygenInput[0])
co2 = BitListToInt(co2Input[0])
print(oxygen*co2)
