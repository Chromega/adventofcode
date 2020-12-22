
input = []
with open("input.txt") as FILE:
    for line in FILE:
        input.append(int(line))
        
#Part a
for i in range(0,len(input)):
    for j in range(i,len(input)):
        if input[i] + input[j] == 2020:
            print(input[i]*input[j])
            
#Part b            
for i in range(0,len(input)):
    for j in range(i,len(input)):
        for k in range(j,len(input)):
            if input[i] + input[j] + input[k] == 2020:
                print(input[i]*input[j]*input[k])