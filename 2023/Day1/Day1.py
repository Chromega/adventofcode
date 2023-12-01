input = []
with open("input.txt") as FILE:
    lines = FILE.readlines()
    for line in [x.strip() for x in lines]:
        if len(line) == 0:
            pass
        else:
            input.append(line)
    
"""
partA = 0
for s in input:
    digits = [c for c in s if c.isdigit()]
    val = int(digits[0])*10+int(digits[-1])
    partA += val
print(partA)
"""
partB = 0
digitStrings = ["zero","one","two","three","four","five","six","seven","eight","nine"]
for s in input:
    i = 0
    
    firstDigit = -1
    lastDigit = -1
    
    for i in range(len(s)):
        newDigit = -1
        if s[i].isdigit():
            newDigit = int(s[i])
        else:
            for ds in digitStrings:
                if s[i:].startswith(ds):
                    newDigit = digitStrings.index(ds)
                    break
        if newDigit!=-1:
            lastDigit = newDigit
            if firstDigit < 0:
                firstDigit = newDigit
                
    val = 10*firstDigit + lastDigit
    partB += val
print(partB)
        