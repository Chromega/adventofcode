input = []
with open("input.txt") as FILE:
    for line in FILE:
        input.append(line)
        
        
seatNums = []

for i in input:
    row = 0
    for c in i[0:7]:
        row *= 2
        if c == 'B':
            row += 1
            
            
    col = 0
    for c in i[7:10]:
        col *= 2
        if c == 'R':
            col += 1
            
    seatNums.append((row,col))
    
#Part a 9:22
highestId = 0
for row,col in seatNums:
    id = row*8+col
    if id > highestId:
        highestId = id
print(highestId)

#Part b 12:06
ids = set()
for row,col in seatNums:
    id = row*8+col
    ids.add(id)
id = 0
while True:
    if id not in ids and (id-1) in ids and (id+1) in ids:
        print(id)
        break
    id += 1