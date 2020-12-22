
PREAMBLE_LENGTH = 25
input = []
with open("input.txt") as FILE:
    for line in FILE:
        line = line.strip()
        input.append(int(line))

        
#part a
invalidNumber = 0
for i in range(len(input)):
    currentVal = input[i]
    if i < PREAMBLE_LENGTH:
        continue
    
    found = False
    preambleStart = i-PREAMBLE_LENGTH
    for j in range(preambleStart,i):
        for k in range(j+1, i):
            sum = input[j]+input[k]
            if sum == currentVal:
                found = True
                break
        if found:
            break
    if not found:
        invalidNumber = currentVal
        print(currentVal)
        break
        
        
#part b
for i in range(len(input)):
    sum = input[i]
    for j in range(i+1,len(input)):
        sum += input[j]
        if sum == invalidNumber:
            smallest = input[i]
            largest = input[i]
            for k in range(i,j+1):
                if input[k] < smallest:
                    smallest = input[k]
                if input[k] > largest:
                    largest = input[k]
            print(smallest+largest)
            break
        
