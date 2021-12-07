input = []
with open("input.txt") as FILE:
    lines = FILE.readlines()
    for line in lines:
        parts = line.split(' ')
        directionLabel = parts[0]
        magnitude = int(parts[1])
        if directionLabel == 'forward':
            input.append((magnitude,0))
        elif directionLabel == 'down':
            input.append((0,magnitude))
        else:
            input.append((0,-magnitude))
print(len(input))

#part a
pos = [0,0]
for movement in input:
    pos[0] += movement[0]
    pos[1] += movement[1]

print(pos[0]*pos[1])


#part b
pos = [0,0]
aim = 0
for movement in input:
    pos[0] += movement[0]
    aim += movement[1]
    pos[1] += movement[0]*aim
print(pos[0]*pos[1])
