fishCounts = {}

def SafeAdd(d, key, inc):
    if key in d:
        d[key] = d[key]+inc
    else:
        d[key] = inc

with open("input.txt") as FILE:
    for line in FILE.readlines():
        vals = [int(x) for x in line.split(",")]
        for val in vals:
            SafeAdd(fishCounts,val,1)

def SimulateForDays(numDays, fish):
    for i in range(numDays):
        newCounts = {}
        for days in fish:
            thisCount = fish[days]
            if days == 0:
                SafeAdd(newCounts,6,thisCount)
                SafeAdd(newCounts,8,thisCount)
            else:
                SafeAdd(newCounts,days-1,thisCount)
        fish = newCounts
    return fish

print(fishCounts)
#part a
partA = fishCounts.copy()
partA = SimulateForDays(80,partA)

totalCount = 0
for days in partA:
    totalCount += partA[days]
    
print(totalCount)


#part b
partB = fishCounts.copy()
partB = SimulateForDays(256,partB)
    
totalCount = 0
for days in partB:
    totalCount += partB[days]
    
print(totalCount)