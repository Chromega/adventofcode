import math

NUM_DIMENSIONS = 3

class Rigidbody:
   def __init__(self):
      self.pos = [0,0,0]
      self.vel = [0,0,0]
      
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
      moons.append(moon)
      
   timestep = 0
   while timestep <= 1000000:
      #print 'after ' + str(timestep) + ' steps'
      #printState(moons)
      
      for moon1Idx in xrange(len(moons)):
         for moon2Idx in xrange(moon1Idx+1,len(moons)):
            moon1 = moons[moon1Idx]
            moon2 = moons[moon2Idx]
            for dimension in xrange(NUM_DIMENSIONS):
               if moon1.pos[dimension] < moon2.pos[dimension]:
                  moon1.vel[dimension] += 1
                  moon2.vel[dimension] -= 1
               elif moon1.pos[dimension] > moon2.pos[dimension]:
                  moon1.vel[dimension] -= 1
                  moon2.vel[dimension] += 1
                  
      for moon in moons:
         for dimension in xrange(NUM_DIMENSIONS):
            moon.pos[dimension] += moon.vel[dimension]
      timestep += 1
   #14645 too high