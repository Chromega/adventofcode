class Node:   
   def __init__(self):
      self.children = []
      self.name = ""
      self.parent = None

   def GetTotalNumOrbits(self, depth):
      x = depth
      for node in self.children:
         x += node.GetTotalNumOrbits(depth+1)
      return x

   def PrintChildren(self):
      for child in self.children:
         print child.name
         
   def MakeParentStack(self, arr):
      arr.insert(0, self)
      if self.parent is not None:
         self.parent.MakeParentStack(arr)
nodes = {}

def GetOrCreateNode(name):
   global nodes
   if name in nodes:
      return nodes[name]
   else:
      node = Node()
      node.name = name
      nodes[name] = node
      return node
      
with open("input.txt", "r") as FILE:
   for line in FILE.readlines():
      orbitNodes = line.strip().split(')')
      
      node1 = GetOrCreateNode(orbitNodes[0])
      node2 = GetOrCreateNode(orbitNodes[1])
      node1.children.append(node2)
      node2.parent = node1
      
#print nodes["COM"].GetTotalNumOrbits(0)

youStack = []
sanStack = []
nodes["YOU"].MakeParentStack(youStack)
nodes["SAN"].MakeParentStack(sanStack)

stackIdx = 0
while True:
   youN = youStack[stackIdx]
   sanN = sanStack[stackIdx]
   if youN == sanN:
      stackIdx += 1
   else:
      print len(youStack) + len(sanStack) - 2*stackIdx - 2
      break