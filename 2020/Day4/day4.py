requiredFields = {"byr","iyr","eyr","hgt","hcl","ecl","pid"}
optionalFields = {"cid",}

class Passport:
    def __init__(self):
        self.requiredFields = {}
        self.optionalFields = {}
    def AddFields(self, fields):
        for key in fields:
            self.AddField(key, fields[key])
    def AddField(self, key, value):
        if key in requiredFields:
            self.requiredFields[key] = value
        if key in optionalFields:
            self.optionalFields[key] = value
    def IsValidA(self):
        return len(self.requiredFields)==len(requiredFields)
    def IsValidB(self):
        if len(self.requiredFields)!=len(requiredFields):
            return False
            
        byr = int(self.requiredFields["byr"])
        if byr<1920 or byr > 2002:
            return False
            
        iyr = int(self.requiredFields["iyr"])
        if iyr<2010 or iyr > 2020:
            return False
            
        eyr = int(self.requiredFields["eyr"])
        if eyr<2020 or eyr > 2030:
            return False
        
        hgt = self.requiredFields["hgt"]
        if hgt.endswith("cm"):
            hgtVal = int(hgt[:-2])
            if hgtVal < 150 or hgtVal > 193:
                return False
        elif hgt.endswith("in"):
            hgtVal = int(hgt[:-2])
            if hgtVal < 59 or hgtVal > 76:
                return False
        else:
            return False
                
        hcl = self.requiredFields["hcl"]
        if len(hcl) != 7:
            return False
        if hcl[0] != "#":
            return False
        for c in hcl[1:]:
            if c not in {'0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f'}:
                return False
                
        ecl = self.requiredFields["ecl"]
        if ecl not in {'amb','blu','brn','gry','grn','hzl','oth'}:
            return False
            
        pid = self.requiredFields["pid"]
        if len(pid) != 9:
            return False
        for c in pid:
            if c not in {'0','1','2','3','4','5','6','7','8','9'}:
                return False
                
        return True

input = []
with open("input.txt") as FILE:
    passport = Passport()
    for line in FILE:
        fields = {}
        if len(line.strip()) == 0:
            input.append(passport)
            passport = Passport()
            continue
        for kvp in line.strip().split(' '):
            tokens = kvp.split(':')
            fields[tokens[0]] = tokens[1]
        passport.AddFields(fields)
    input.append(passport)
        
#Part a
count = 0
for passport in input:
    if passport.IsValidA():
        count += 1
print(count)

count = 0
for passport in input:
    if passport.IsValidB():
        count += 1
print(count)