import math

NUM_DIMENSIONS = 3

def gcd(a,b):
    """Compute the greatest common divisor of a and b"""
    while b > 0:
        a, b = b, a % b
    return a
    
def lcm(a, b):
    """Compute the lowest common multiple of a and b"""
    return a * b / gcd(a, b)

class Rigidbody:
   def __init__(self):
      self.pos = [0,0,0]
      self.vel = [0,0,0]
      self.initialPos = [0,0,0]
      self.initialVel = [0,0,0]
   def hasLooped(self, dimension):
      return self.pos[dimension] == self.initialPos[dimension] and self.vel[dimension] == self.initialVel[dimension]
      
      
def printState(rigidbodies):
   for rb in rigidbodies:
      print str(rb.pos) + " " + str(rb.vel)
   print "Energy: " + str(getEnergy(rigidbodies))
   print ' '
   
def getEnergy(rigidbodies):
   energy = 0
   for rb in rigidbodies:
      pot = 0
      kin = 0
      for dimension in xrange(NUM_DIMENSIONS):
         pot += math.fabs(rb.pos[dimension])
         kin += math.fabs(rb.vel[dimension])
      energy += pot*kin
   return int(round(energy))
   
def simulateDimension(moons, dimension):
   for moon1Idx in xrange(len(moons)):
      moon1 = moons[moon1Idx]
      for moon2Idx in xrange(moon1Idx+1,len(moons)):
         moon2 = moons[moon2Idx]
         if moon1.pos[dimension] < moon2.pos[dimension]:
            moon1.vel[dimension] += 1
            moon2.vel[dimension] -= 1
         elif moon1.pos[dimension] > moon2.pos[dimension]:
            moon1.vel[dimension] -= 1
            moon2.vel[dimension] += 1
      moon1.pos[dimension] += moon1.vel[dimension]
            
def hasLooped(moons, dimension):
   for moon in moons:
      if not moon.hasLooped(dimension):
         return False
   return True
            
def simulateUntilLoop(moons, dimension):
   timestep = 0
   while (timestep==0 or not hasLooped(moons, dimension)):
      simulateDimension(moons, dimension)
      timestep += 1
      #print timestep
      #printState(moons)
   return timestep
   
def simulateNLoops(moons, n):
   timestep = 0
   #printState(moons)
   while (timestep < n):
      for dimension in xrange(NUM_DIMENSIONS):
         simulateDimension(moons, dimension)
      timestep += 1
      #print timestep
      #printState(moons)
   #print timestep
   #printState(moons)
   return timestep
      
      
with open("input.txt", "r") as FILE:

   moons = []
   for line in FILE.readlines():
      line = line.replace('<','').replace('>','').replace(',','').strip()
      moon = Rigidbody()
      dimension = 0
      for coordinateStr in line.split(' '):
         coordinateVal = int(coordinateStr[2:])
         moon.pos[dimension] = coordinateVal
         dimension += 1
      moon.initialPos = moon.pos[:]
      moon.initialVel = moon.vel[:]
      moons.append(moon)
      
   x = simulateUntilLoop(moons, 0)
   y = simulateUntilLoop(moons, 1)
   z = simulateUntilLoop(moons, 2)
   
   print x,y,z
   print lcm(lcm(x,y),z)
   #printState(moons)
   #print simulateNLoops(moons, 792)
   #14645 too high