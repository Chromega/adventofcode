totalFuel = 0

def addMass(mass):
   fuel = int(mass/3)-2
   if (fuel < 0):
      return 0
   fuelForFuel = addMass(fuel)
   return fuel + fuelForFuel

with open("input.txt", "r") as FILE:
   for line in FILE.readlines():
      mass = int(line)
      totalFuel += addMass(mass)
      
print totalFuel