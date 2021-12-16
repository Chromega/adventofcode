input = ""
with open("input.txt") as FILE:
    for line in FILE.readlines():
        input = line.strip()

def HexToBoolArr(hex):
    hexValueStr = "0123456789ABCDEF"
    intValue = hexValueStr.index(hex)
    return [intValue&8!=0,intValue&4!=0,intValue&2!=0,intValue&1!=0]
    
def BoolArrToInt(boolArr):
    val = 0
    for b in boolArr:
        val *= 2
        if b:
            val += 1
    return val
    
boolBuffer = []
for c in input:
    boolBuffer.extend(HexToBoolArr(c))
    
class Packet:
    def GetValue(self):
        pass
class LiteralPacket(Packet):
    def GetValue(self):
        return self.value
class SumPacket(Packet):
    def GetValue(self):
        value = 0
        for sp in self.subpackets:
            value += sp.GetValue()
        return value
class ProductPacket(Packet):
    def GetValue(self):
        value = 1
        for sp in self.subpackets:
            value *= sp.GetValue()
        return value
class MinimumPacket(Packet):
    def GetValue(self):
        value = 99999999999999
        for sp in self.subpackets:
            value = min(value,sp.GetValue())
        return value
class MaximumPacket(Packet):
    def GetValue(self):
        value = -99999999999999
        for sp in self.subpackets:
            value = max(value,sp.GetValue())
        return value
class GreaterThanPacket(Packet):
    def GetValue(self):
        if self.subpackets[0].GetValue() > self.subpackets[1].GetValue():
            return 1
        return 0
class LessThanPacket(Packet):
    def GetValue(self):
        if self.subpackets[0].GetValue() < self.subpackets[1].GetValue():
            return 1
        return 0
class EqualPacket(Packet):
    def GetValue(self):
        if self.subpackets[0].GetValue() == self.subpackets[1].GetValue():
            return 1
        return 0
        
versionSum = 0 #part a
        
def CreatePacketFromBoolStream(boolBuffer, startIdx):
    global versionSum
    version = BoolArrToInt(boolBuffer[startIdx:startIdx+3])
    versionSum += version
    packetType = BoolArrToInt(boolBuffer[startIdx+3:startIdx+6])
    packet = None
    if packetType == 4: #int literal
        currentIdx = startIdx+6
        hasMoreIntChunks = True
        intVal = 0
        while hasMoreIntChunks:
            hasMoreIntChunks = boolBuffer[currentIdx]
            intChunk = BoolArrToInt(boolBuffer[currentIdx+1:currentIdx+5])
            currentIdx = currentIdx+5
            intVal *= 16
            intVal += intChunk
        packet = LiteralPacket()
        packet.value = intVal
    else: #operator
        lengthTypeId = boolBuffer[startIdx+6]
        currentIdx = startIdx+6
        subpackets = []
        if lengthTypeId == 0:
            subPacketLength = BoolArrToInt(boolBuffer[startIdx+7:startIdx+22])
            subPacketStartIdx = startIdx+22
            currentIdx = subPacketStartIdx
            while currentIdx < subPacketStartIdx+subPacketLength:
                subpacket, currentIdx = CreatePacketFromBoolStream(boolBuffer, currentIdx)
                subpackets.append(subpacket)
            
        elif lengthTypeId == 1:
            numSubpackets = BoolArrToInt(boolBuffer[startIdx+7:startIdx+18])
            currentIdx = startIdx+18
            for i in range(numSubpackets):
                subpacket, currentIdx = CreatePacketFromBoolStream(boolBuffer, currentIdx)
                subpackets.append(subpacket)
                
        if packetType == 0:
            packet = SumPacket()
        elif packetType == 1:
            packet = ProductPacket()
        elif packetType == 2:
            packet = MinimumPacket()
        elif packetType == 3:
            packet = MaximumPacket()
        elif packetType == 5:
            packet = GreaterThanPacket()
        elif packetType == 6:
            packet = LessThanPacket()
        elif packetType == 7:
            packet = EqualPacket()
        packet.subpackets = subpackets

    return packet, currentIdx
    
packet, currentIdx = CreatePacketFromBoolStream(boolBuffer, 0)
print(versionSum)
print(packet.GetValue())