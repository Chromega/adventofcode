DEAL_NEW_STACK = "DNS"
CUT = "CUT"
DEAL_INCREMENT = "DIN"

def modInverse(a, m) : 
      
    g = gcd(a, m) 
      
    if (g != 1) : 
        return None 
          
    else : 
        return power(a, m - 2, m)
        
def BigMult(factor1, factor2, m):
   runningsum = 0
   while factor2 > 0:
      if factor2%2==0:
         factor1 *= 2
         factor2 /=2
      else:
         runningsum += factor1
         factor2 -= 1
      factor1 %= m
      factor2 %= m
      runningsum %= m
   return runningsum
      
# To compute x^y under modulo m 
def power(x, y, m) : 
      
    if (y == 0) : 
        return 1
          
    p = power(x, y // 2, m) % m 
    #p = (p * p) % m 
    p = BigMult(p,p,m)
  
    if(y % 2 == 0) : 
        return p  
    else :  
        return ((x * p) % m) 
  
# Function to return gcd of a and b 
def gcd(a, b) : 
    if (a == 0) : 
        return b 
          
    return gcd(b % a, a) 
    
def GetCutShuffle(n):
   return (1, n)
   
def GetNewStackShuffle(size):
   return (size-1, size-1)
   
def GetIncrementShuffleForPrimeDeck(n, size):
   modInv = modInverse(n, size)
   return (modInv, 0)

class Cards():
   def __init__(self, size, isSizePrime):
      self.deck = range(size)
      self.scratch = range(size)
      self.isSizePrime = isSizePrime
      
   def SwapScratch(self):
      temp = self.deck
      self.deck = self.scratch
      self.scratch = temp
      
   def DealIntoNewStack(self):
      size = len(self.deck)
      for i in xrange(size):
         self.scratch[i] = self.deck[(i*(size-1) - 1)%size]
         #self.scratch[i] = self.deck[size-i-1]
         #self.scratch[size-i-1] = self.deck[i]
      self.SwapScratch()
      
   def Cut(self, n):
      size = len(self.deck)
      for i in xrange(size):
         self.scratch[i] = self.deck[(i+n)%size]
         #self.scratch[(i-n)%size] = self.deck[i]
      self.SwapScratch()
      
   def DealIncrement(self, n):
      size = len(self.deck)
      if self.isSizePrime:
         modInv = modInverse(n, size)
         for i in xrange(size):
            self.scratch[i] = self.deck[(i*modInv)%size]
      else:
         for i in xrange(size):
            self.scratch[(i*n)%size] = self.deck[i]
      self.SwapScratch()
      
   def ApplyReducedShuffle(self, shuffle):
      for i in xrange(size):
         self.scratch[i] = self.deck[(i*shuffle[0]+shuffle[1])%size]
      self.SwapScratch()
      
   def RunSequence(self, seq):
      for shuffle in seq:
         if shuffle[0] == DEAL_NEW_STACK:
            self.DealIntoNewStack()
         elif shuffle[0] == CUT:
            self.Cut(shuffle[1])
         elif shuffle[0] == DEAL_INCREMENT:
            self.DealIncrement(shuffle[1])

inText = ""
with open("input.txt", "r") as FILE:
   inText = FILE.read()
   
#inText = ""
#inText = "deal into new stack"   
#inText = "cut -4"   
#inText = "deal with increment 3"   
#inText = """deal into new stack"""
   

shuffleSequence = []
for line in inText.split('\n'):
   line = line.strip()
   if line == "":
      break
   tokens = line.split(' ')
   if tokens[0] == "cut":
      shuffle = (CUT, int(tokens[1]))
   else:
      if tokens[1] == "into":
         shuffle = (DEAL_NEW_STACK,)
      else:
         shuffle = (DEAL_INCREMENT, int(tokens[3]))
   shuffleSequence.append(shuffle)
cards = Cards(10007, True)
#print cards.deck
cards.RunSequence(shuffleSequence)
#print cards.deck
"""for i in xrange(len(cards.deck)):
   if cards.deck[i] == 2019:
      print i
      break"""
#print cards.deck[0]
      

def Combine(outShuffle, shuffle0, shuffle1, size):
   s00 = shuffle0[0]
   s01 = shuffle0[1]
   s10 = shuffle1[0]
   s11 = shuffle1[1]
   outShuffle[0] = s10*s00
   outShuffle[1] = s11*s00 + s01
   outShuffle[0] %= size
   outShuffle[1] %= size
   
def Invert(shuffle, size):
   a = shuffle[0]
   b = shuffle[1]
   invA = modInverse(a, size)
   newA = (invA)%size
   newB = (-b*invA)%size
   return [newA, newB]
   
def MakeShuffleFromString(txt, size):
   totalShuffle = [1,0]
   for line in txt.split('\n'):
      line = line.strip()
      if line == "":
         break
      tokens = line.split(' ')
      if tokens[0] == "cut":
         shuffle = GetCutShuffle(int(tokens[1]))
      else:
         if tokens[1] == "into":
            shuffle = GetNewStackShuffle(size)
         else:
            shuffle = GetIncrementShuffleForPrimeDeck(int(tokens[3]), size)
      Combine(totalShuffle, totalShuffle, shuffle, size)
   return totalShuffle
      
size = 10007
totalShuffle = MakeShuffleFromString(inText, size)
print totalShuffle
idx = 6417
#for idx in xrange(size):
print (totalShuffle[0]*idx+totalShuffle[1])%size

shuffleIterations = 101741582076661
size = 119315717514047
baseShuffle = MakeShuffleFromString(inText, size)
print baseShuffle
print Invert(baseShuffle, size)
print Invert(baseShuffle, size)[0]
print Invert(baseShuffle, size)[1] - size

totalShuffle = [1,0]

while shuffleIterations > 0:
   if shuffleIterations%2==1:
      Combine(totalShuffle, totalShuffle, baseShuffle, size)
      shuffleIterations -= 1
   else:
      Combine(baseShuffle, baseShuffle, baseShuffle, size)
      shuffleIterations /= 2
idx = 2020
print "shuf + idx" + str(totalShuffle[0]*idx)
print (totalShuffle[0]*idx+totalShuffle[1])%size

print totalShuffle
inv = Invert(totalShuffle, size)
print inv
print (inv[0]*98461321956136+inv[1])%size
print Invert(inv, size)