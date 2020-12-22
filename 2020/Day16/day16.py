class Ticket():
    def __init__(self):
        self.values = []

class FieldRule():
    def __init__(self):
        self.range1 = (0,0)
        self.range2 = (0,0)
    def IsInRange(self, value):
        if value >= self.range1[0] and value <= self.range1[1]:
            return True
        if value >= self.range2[0] and value <= self.range2[1]:
            return True
        return False

class TicketRules():
    def __init__(self):
        self.fields = {} #name->FieldRule
        
    def GetInvalidRate(self, tickets, validTickets):
        invalidRate = 0
        validTickets.clear()
        for ticket in tickets:
            isInvalid = False
            for value in ticket.values:
                foundMatchingRule = False
                for field in self.fields:
                    fieldRule = self.fields[field]
                    if fieldRule.IsInRange(value):
                        foundMatchingRule = True
                        break
                if not foundMatchingRule:
                    invalidRate += value
                    isInvalid = True
            if not isInvalid:
                validTickets.append(ticket)
        return invalidRate
        
    def GetIndicesForField(self, validTickets, fieldName):
        fieldRule = self.fields[fieldName]
        indices = set()
        
        for idx in range(len(self.fields)):
            allValid = True
            for ticket in validTickets:
                value = ticket.values[idx]
                if not fieldRule.IsInRange(value):
                    allValid = False
                    break
            if allValid:
                indices.add(idx)
                
        return indices
        
    def DetermineFieldIndices(self, tickets):
        possibleFieldAssignments = {} #name->set<int>
        for fieldName in self.fields:
            possibleFieldAssignments[fieldName] = self.GetIndicesForField(tickets, fieldName)
        
        finalFieldAssignments = {} #name->int
        
        while len(possibleFieldAssignments)>0:
            for fieldName in possibleFieldAssignments:
                if len(possibleFieldAssignments[fieldName])==1:
                    idx = possibleFieldAssignments[fieldName].pop()
                    finalFieldAssignments[fieldName] = idx
                    print(fieldName + " is " + str(idx))
                    del possibleFieldAssignments[fieldName]
                    for iFieldName in possibleFieldAssignments:
                        if idx in possibleFieldAssignments[iFieldName]:
                            possibleFieldAssignments[iFieldName].remove(idx)
                    break
        return finalFieldAssignments
        
rules = TicketRules()
myTicket = Ticket()
nearbyTickets = []
with open("input.txt") as FILE:
    STATE_RULES = 0
    STATE_MY = 1
    STATE_NEARBY = 2
    
    state = STATE_RULES
    for line in FILE:
        line = line.strip()
        
        if len(line) == 0:
            continue
        
        if state == STATE_RULES:
            if line == "your ticket:":
                state = STATE_MY
            else:
                colonIdx = line.find(':')
                firstDashIdx = line.find('-', colonIdx+1)
                secondDashIdx = line.find('-', firstDashIdx+1)
                firstSpaceIdx = line.find(' ', colonIdx+1)
                secondSpaceIdx = line.find(' ', firstSpaceIdx+1)
                thirdSpaceIdx = line.find(' ', secondSpaceIdx+1)
                
                name = line[:colonIdx]
                firstVal = int(line[firstSpaceIdx+1:firstDashIdx])
                secondVal= int(line[firstDashIdx+1:secondSpaceIdx])
                thirdVal= int(line[thirdSpaceIdx+1:secondDashIdx])
                fourthVal= int(line[secondDashIdx+1:])
                
                fr = FieldRule()
                fr.range1 = (firstVal, secondVal)
                fr.range2 = (thirdVal, fourthVal)
                
                rules.fields[name] = fr
        elif state == STATE_MY:
            if line == "nearby tickets:":
                state = STATE_NEARBY
            else:
                myTicket.values = [int(x) for x in line.split(',')]
        elif state == STATE_NEARBY:
            t = Ticket()
            t.values = [int(x) for x in line.split(',')]
            nearbyTickets.append(t)


#part a 15:17
validTickets = []
print(rules.GetInvalidRate(nearbyTickets, validTickets))

#Part b
fieldAssignments = rules.DetermineFieldIndices(validTickets)
product = 1
for fieldName in rules.fields:
    if fieldName.startswith("departure"):
        product *= myTicket.values[fieldAssignments[fieldName]]
print(product)