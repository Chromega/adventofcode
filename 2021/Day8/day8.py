import itertools

class Entry:
    def __init__(self):
        self.examples = set()
        self.code = []
        self.cipher = {}

input = []

with open("input.txt") as FILE:
    for line in FILE.readlines():
        tokens = line.split("|")
        entry = Entry()
        for example in tokens[0].strip().split(' '):
            entry.examples.add(''.join(sorted(example)))
            
        for code in tokens[1].strip().split(' '):
            entry.code.append(''.join(sorted(code)))
        
        input.append(entry)
        
validDigits = {}
validDigits['abcefg'] = 0
validDigits['cf'] = 1
validDigits['acdeg'] = 2
validDigits['acdfg'] = 3
validDigits['bcdf'] = 4
validDigits['abdfg'] = 5
validDigits['abdefg'] = 6
validDigits['acf'] = 7
validDigits['abcdefg'] = 8
validDigits['abcdfg'] = 9
            
            
#part a
count = 0
for entry in input:
    for digit in entry.code:
        segments = len(digit)
        if segments == 2 or segments == 4 or segments == 3 or segments == 7:
            count += 1
print(count)


#part b
partB = 0
for entry in input:
    for perm in itertools.permutations('abcdefg'):
        transformationDict = {}
        transformationDict['a'] = perm[0]
        transformationDict['b'] = perm[1]
        transformationDict['c'] = perm[2]
        transformationDict['d'] = perm[3]
        transformationDict['e'] = perm[4]
        transformationDict['f'] = perm[5]
        transformationDict['g'] = perm[6]
        
        allExamplesValid = True
        for example in entry.examples:
            transformedExample = ""
            for c in example:
                transformedExample += transformationDict[c]
            transformedExample = ''.join(sorted(transformedExample))
            if transformedExample not in validDigits:
                allExamplesValid = False
                break
        if allExamplesValid:
            entry.cipher = transformationDict
            break
                
    numericalResult = 0
    for digit in entry.code:
        transformedDigit = ""
        for c in digit:
            transformedDigit += entry.cipher[c]
        transformedDigit = ''.join(sorted(transformedDigit))
        numericalDigit = validDigits[transformedDigit]
        numericalResult *= 10
        numericalResult += numericalDigit
    partB += numericalResult
print(partB)   