class Scanner():
    #Assuming that rotation preceded translation
    def __init__(self):
        self.beacons = []
        self.rotatedBeacons = []
        self.translatedBeacons = []
        self.currentRotation = ((0,1,2),(1,1,1))
        self.currentTranslation = (0,0,0)
        self.transformedBeaconSet = set()
        self.locked = False
        self.index = 0
        
    def Setify(self):
        self.transformedBeaconSet = set(self.translatedBeacons)
        
    def ClearAllTransformation(self):
        self.rotatedBeacons = self.beacons.copy()
        self.translatedBeacons = self.beacons.copy()
        self.currentRotation = ((0,1,2),(1,1,1))
        self.currentTranslation = (0,0,0)
        
    def ClearTranslation(self):
        self.translatedBeacons = self.rotatedBeacons.copy()
        
    def Rotate(self,rotation):
        for i in range(len(self.rotatedBeacons)):
            pos = self.rotatedBeacons[i]
            permutation, inversion = rotation
            newPos = [0,0,0]
            for axis in range(len(permutation)):
                newPos[permutation[axis]] = pos[axis]*inversion[axis]
            self.rotatedBeacons[i] = tuple(newPos)
        self.translatedBeacons = self.rotatedBeacons.copy()
        
        self.currentRotation = rotation
        self.currentTranslation = (0,0,0)
        
    def Translate(self,translation):
        for i in range(len(self.translatedBeacons)):
            pos = self.translatedBeacons[i]
            newPos = (pos[0]+translation[0],pos[1]+translation[1],pos[2]+translation[2])
            self.translatedBeacons[i] = newPos
        self.currentTranslation = translation
            
    def IsInBounds(self,pos):
        for i in range(3):
            if abs(pos[i]-self.currentTranslation[i])>500:
                return False
        return True
        
rotations = [] #permutation, inversion. screw it im doing it manually
rotations.append(((0,1,2),(1,1,1)))
rotations.append(((0,1,2),(-1,-1,1)))
rotations.append(((0,1,2),(-1,1,-1)))
rotations.append(((0,1,2),(1,-1,-1)))

rotations.append(((1,0,2),(1,-1,1)))
rotations.append(((1,0,2),(-1,1,1)))
rotations.append(((1,0,2),(1,1,-1)))
rotations.append(((1,0,2),(-1,-1,-1)))

rotations.append(((0,2,1),(1,1,-1)))
rotations.append(((0,2,1),(-1,1,1)))
rotations.append(((0,2,1),(1,-1,1)))
rotations.append(((0,2,1),(-1,-1,-1)))

rotations.append(((1,2,0),(1,1,1)))
rotations.append(((1,2,0),(-1,1,-1)))
rotations.append(((1,2,0),(-1,-1,1)))
rotations.append(((1,2,0),(1,-1,-1)))

rotations.append(((2,0,1),(1,1,1)))
rotations.append(((2,0,1),(1,-1,-1)))
rotations.append(((2,0,1),(-1,-1,1)))
rotations.append(((2,0,1),(-1,1,-1)))

rotations.append(((2,1,0),(1,1,-1)))
rotations.append(((2,1,0),(1,-1,1)))
rotations.append(((2,1,0),(-1,1,1)))
rotations.append(((2,1,0),(-1,-1,-1)))
        
input = []
with open("input.txt") as FILE:
    currentScanner = None
    for line in FILE.readlines():
        line = line.strip()
        if len(line) == 0:
            continue
        if line.startswith('---'):
            currentScanner = Scanner()
            currentScanner.index = len(input)
            input.append(currentScanner)
        else:
            tokens = line.split(',')
            currentScanner.beacons.append((int(tokens[0]),int(tokens[1]),int(tokens[2])))
        
def TryToFindMatch(rootScanner, scanner):
    for rotation in rotations:
        scanner.ClearAllTransformation()
        scanner.Rotate(rotation)
        
        #Move each test becon to each root beacon to see if we can get sufficient alignment
        for rootBeacon in rootScanner.translatedBeacons:
            for beacon in scanner.rotatedBeacons:
                translation = (rootBeacon[0]-beacon[0],rootBeacon[1]-beacon[1],rootBeacon[2]-beacon[2])
                
                scanner.ClearTranslation()
                scanner.Translate(translation)
                scanner.Setify()
                
                matchingCount = 0
                for b in rootScanner.translatedBeacons:
                    if b in scanner.transformedBeaconSet:
                        matchingCount += 1
                        
                if matchingCount >= 12:
                    print(str(scanner.index) + " " + str(translation))
                    scanner.locked = True
                    return
        
#part a
input[0].ClearAllTransformation()
input[0].Setify()
input[0].locked = True
while True:
    for i in range(0,len(input)):
        if input[i].locked:
            for j in range(0,len(input)):
                if not input[j].locked:
                    TryToFindMatch(input[i],input[j])
    allLocked = True
    for beacon in input:
        if not beacon.locked:
            allLocked = False
            break
    if allLocked:
        break
    
fullBeaconSet = set()
for scanner in input:
    fullBeaconSet.update(scanner.transformedBeaconSet)
print(len(fullBeaconSet))

#part b
maxDistance = 0
for s1 in input:
    for s2 in input:
        distance = abs(s1.currentTranslation[0]-s2.currentTranslation[0])+abs(s1.currentTranslation[1]-s2.currentTranslation[1])+abs(s1.currentTranslation[2]-s2.currentTranslation[2])
        if distance > maxDistance:
            maxDistance = distance
print(maxDistance)