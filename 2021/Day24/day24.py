inputParams = []
currentParam = None

with open("input.txt") as FILE:
    for line in FILE.readlines():
        line = line.strip()
        if line.startswith("inp"):
            if currentParam is not None:
                inputParams.append(currentParam)
            currentParam = [0,0,0]
        elif line.startswith("div"):
            currentParam[1] = int(line.split(' ')[2])
        elif line.startswith("add x"):
            val = line.split(' ')[2]
            try:
                currentParam[0] = int(val)
            except ValueError:
                pass
        elif line.startswith("add y"):
            val = line.split(' ')[2]
            try:
                currentParam[2] = int(val)
            except ValueError:
                pass
    inputParams.append(currentParam)
print(inputParams)

def DigitFunc(input,z,params):
    w,x,y=input,0,0
    x = z%26 + params[0]
    z = z//params[1]
    x = 0 if x==w else 1
    z *= 25 * x + 1
    z += (w+params[2])*x
    return z
    
cache = {}
def GetValidNumber(startIndex=0,z=0,biggest=True):
    t = (startIndex,z,biggest)
    if t in cache:
        return cache[t]
        
    ret = False,0
    if startIndex == len(inputParams):
        if z == 0:
            ret = True,0
        else:
            ret = False,0
    else:
        params = inputParams[startIndex]
        needsToDecrease = params[1]==26
        #for digit in range(9,0,-1):
        if biggest:
            r = range(9,0,-1)
        else:
            r = range(1,10)
        for digit in r:
            newZ = DigitFunc(digit,z,params)
            if needsToDecrease and newZ > z:
                continue
            exists,value=GetValidNumber(startIndex+1,newZ,biggest)
            if exists:
                ret = True,digit+10*value
                break
    cache[t]=ret
    return ret
    
print(str(GetValidNumber(0,0,True)[1])[::-1])
print(str(GetValidNumber(0,0,False)[1])[::-1])