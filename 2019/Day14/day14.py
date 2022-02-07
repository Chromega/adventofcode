reactions = {}

class Reaction:
   def __init__(self):
      self.result = ""
      self.resultQuantity = 0
      self.reactants = []
      self.generation = -1
      
   def GetGeneration(self):
      global reactions
      if self.generation >= 0:
         return self.generation
      
      maxReactantGeneration = -1
      for reactantData in self.reactants:
         reactant = reactantData[0]
         reaction = reactions[reactant]
         generation = reaction.GetGeneration()
         if generation > maxReactantGeneration:
            maxReactantGeneration = generation
      self.generation = maxReactantGeneration+1
      return self.generation
      
   def RunReaction(self, resources, times):
      for reactantData in self.reactants:
         reactant = reactantData[0]
         reactantQuantity = reactantData[1]
         
         resources[reactant] -= times*reactantQuantity
         if resources[reactant] < 0:
            print "uh oh"
      resources[self.result] = self.resultQuantity*times
      
def NumOreToProduceFuel(quantity):
   resourcesRequired = {}
   resourcesRequired["FUEL"] = quantity
   
   for generation in xrange(reactions["FUEL"].GetGeneration(),0,-1):
      #print resourcesRequired
      newResourcesRequired = {}
      for resource in resourcesRequired:
         numRequired = resourcesRequired[resource]
         rxn = reactions[resource]
         if rxn.GetGeneration() != generation:
            if resource not in newResourcesRequired:
               newResourcesRequired[resource] = 0
            newResourcesRequired[resource] += numRequired
            continue
         minProduced = rxn.resultQuantity
         timesToRunRxn = numRequired/minProduced
         if numRequired%minProduced != 0:
            timesToRunRxn += 1
         #print "Run " + resource + " rxn " + str(timesToRunRxn) + " times"
         for reactantData in rxn.reactants:
            reactant = reactantData[0]
            reactantQuantity = reactantData[1]
            if reactant not in newResourcesRequired:
               newResourcesRequired[reactant] = 0
            newResourcesRequired[reactant] += reactantQuantity*timesToRunRxn
      resourcesRequired = newResourcesRequired
   return resourcesRequired["ORE"]

with open("input.txt", "r") as FILE:

   for line in FILE.readlines():
   
      rxn = Reaction()
      
      sides = line.strip().split("=>")
      
      resultOptions = sides[1].strip().split(" ")
      rxn.result = resultOptions[1]
      rxn.resultQuantity = int(resultOptions[0])
      
      allReactants = sides[0].strip().split(",")
      for reactantData in allReactants:
         reactantOptions = reactantData.strip().split(" ")
         reactant = reactantOptions[1]
         reactantQuantity = int(reactantOptions[0])
         rxn.reactants.append((reactant, reactantQuantity))
      reactions[rxn.result] = rxn
      
   oreRxn = Reaction()
   oreRxn.result = "ORE"
   oreRxn.resultQuantity = 1
   oreRxn.generation = 0
   reactions["ORE"] = oreRxn
      
   #for rxnName in reactions:
   #   rxn = reactions[rxnName]
   #   print (rxn.result, rxn.GetGeneration())
   
      
   totalOre = 1000000000000
   min = totalOre/NumOreToProduceFuel(1)
   max = min*2
   
   print (min, max)
   while min <= max:
      mid = (min + max)/2
      resourcesRequired = {}
      oreRequired = NumOreToProduceFuel(mid)
      if oreRequired < totalOre:
         min = mid+1
      elif oreRequired > totalOre:
         max = mid-1
      else:
         max = mid
         min = mid
         break
   print max
   print NumOreToProduceFuel(max)
   """
   reactions["DCFZ"].RunReaction(resourcesRequired, 27)
   reactions["GPVTF"].RunReaction(resourcesRequired, 5)
   reactions["NZVS"].RunReaction(resourcesRequired, 8)
   reactions["PSHF"].RunReaction(resourcesRequired, 25)
   reactions["HKGWZ"].RunReaction(resourcesRequired, 10)
   print resourcesRequired
   reactions["QDVJ"].RunReaction(resourcesRequired, 1)
   reactions["XJWVT"].RunReaction(resourcesRequired, 22)
   reactions["KHKGT"].RunReaction(resourcesRequired, 1)
   print resourcesRequired
   reactions["FUEL"].RunReaction(resourcesRequired, 1)
   print resourcesRequired"""