input = []
with open("input.txt") as FILE:
    lines = FILE.readlines()
    for line in lines:
        input.append(int(line))
print(len(input))

#part a
incCount = 0
lastVal = input[0]
for val in input[1:]:
    if val > lastVal:
        incCount += 1
    lastVal = val
print(incCount)

#part b
windows = []
WINDOW_SIZE = 3
for i in range(len(input)-WINDOW_SIZE+1):
    windowVal = 0
    for j in range(WINDOW_SIZE):
        windowVal += input[i+j]
    windows.append(windowVal)

incCount = 0
lastVal = windows[0]
for val in windows[1:]:
    if val > lastVal:
        incCount += 1
    lastVal = val
print(incCount)

