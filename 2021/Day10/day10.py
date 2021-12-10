input = []

with open("input.txt") as FILE:
    for line in FILE.readlines():
        input.append(line.strip())
        
#part a
openPairings = {}
openPairings['('] = ')'
openPairings['['] = ']'
openPairings['<'] = '>'
openPairings['{'] = '}'

closePairings = {}
closePairings[')'] = '('
closePairings[']'] = '['
closePairings['>'] = '<'
closePairings['}'] = '{'

uncorruptedLines = []
corruptionScore = 0
completionScores = []
for line in input:
    stack = []
    corrupted = False
    for c in line:
        if c in openPairings:
            stack.append(c)
        elif c in closePairings:
            if closePairings[c] == stack[-1]:
                stack = stack[:-1]
            else:
                #part a
                corrupted = True
                if c == ")":
                    corruptionScore += 3
                elif c == "]":
                    corruptionScore += 57
                elif c == "}":
                    corruptionScore += 1197
                elif c == ">":
                    corruptionScore += 25137
                break
    if not corrupted:
        #part b
        score = 0
        for c in reversed(stack):
            score *= 5
            if c == '(':
                score += 1
            elif c == '[':
                score += 2
            elif c == '{':
                score += 3
            elif c == '<':
                score += 4
        completionScores.append(score)
print(corruptionScore)
completionScores.sort()
print(completionScores[int((len(completionScores)-1)/2)])