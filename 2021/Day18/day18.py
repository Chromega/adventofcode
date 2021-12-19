from copy import copy,deepcopy

class Node():
    def __init__(self, parent):
        self.left = None
        self.right = None
        self.parent = parent
    def GetRoot(self):
        node = self
        while node.parent:
            node = node.parent
        return node
    def GetLeafToLeft(self,leaf,lastLeaf=None):
        done = False
        if self == leaf:
            return True,lastLeaf
        if self.right and self.left:
            done,lastLeaf = self.left.GetLeafToLeft(leaf, lastLeaf)
            if done:
                return True, lastLeaf
            done,lastLeaf = self.right.GetLeafToLeft(leaf, lastLeaf)
            if done:
                return True, lastLeaf
            return False, lastLeaf
        return False, self
        
    def GetLeafToRight(self,leaf,lastLeaf=None):
        done = False
        if self == leaf:
            return True,lastLeaf
        if self.right and self.left:
            done,lastLeaf = self.right.GetLeafToRight(leaf, lastLeaf)
            if done:
                return True, lastLeaf
            done,lastLeaf = self.left.GetLeafToRight(leaf, lastLeaf)
            if done:
                return True, lastLeaf
            return False, lastLeaf
        return False, self
        
    def ExplodeIfNeeded(self,depth=0):
        if depth == 4:
            done,nextLeft = self.GetRoot().GetLeafToLeft(self.left)
            done,nextRight = self.GetRoot().GetLeafToRight(self.right)
            if nextLeft:
                nextLeft.value += self.left.value
            if nextRight:
                nextRight.value += self.right.value
            newLeaf = Leaf(self.parent,0)
            self.ReplaceInParent(newLeaf)
            return True
        else:
            if self.left.ExplodeIfNeeded(depth+1):
                return True
            if self.right.ExplodeIfNeeded(depth+1):
                return True
            return False
            
    def ReplaceInParent(self, newNode):
            if self.parent.left == self:
                self.parent.left = newNode
            if self.parent.right == self:
                self.parent.right = newNode
            
    def SplitIfNeeded(self):
        if self.left.SplitIfNeeded():
            return True
        if self.right.SplitIfNeeded():
            return True
        return False
        
    def __str__(self):
        return "[" + str(self.left)+ "," + str(self.right) + "]"
        
    def GetMagnitude(self):
        return 3*self.left.GetMagnitude()+2*self.right.GetMagnitude()
    
class Leaf(Node):
    def __init__(self,parent,value):
        self.value = value
        Node.__init__(self,parent)
    def ExplodeIfNeeded(self,depth=0):
        return False
    def __str__(self):
        return str(self.value)
    def SplitIfNeeded(self):
        if self.value >= 10:
            half = self.value//2
            leftV = half
            rightV = half
            if self.value%2==1:
                rightV=half+1
            newNode = Node(self.parent)
            newNode.left = Leaf(newNode,leftV)
            newNode.right = Leaf(newNode,rightV)
            self.ReplaceInParent(newNode)
            return True
    def GetMagnitude(self):
        return self.value
        
def ParseExpression(exp, parent=None):
    if exp[0] == '[' or exp[0] == ']':
        bracketsRemovedExp = exp[1:-1]
        topLevelCommaIdx = 0
        bracketDepth = 0
        for i in range(len(bracketsRemovedExp)):
            c = bracketsRemovedExp[i]
            if bracketDepth == 0:
                if c == ',':
                    topLevelCommaIdx = i
                    break
            if c == '[':
                bracketDepth += 1
            if c == ']':
                bracketDepth -= 1
        node = Node(parent)
        node.left = ParseExpression(bracketsRemovedExp[:topLevelCommaIdx],node)
        node.right = ParseExpression(bracketsRemovedExp[topLevelCommaIdx+1:],node)
        return node
    else:
        i = int(exp)
        return Leaf(parent,i)
        
input = []

with open("input.txt") as FILE:
    for line in FILE.readlines():
        line = line.strip()
        input.append(ParseExpression(line))
        
#part a

def Add(lhs,rhs):
    #print("do " + str(lhs) + "+" + str(rhs))
    root = Node(None)
    root.left = deepcopy(lhs)
    root.left.parent = root
    root.right = deepcopy(rhs)
    root.right.parent = root
    #print("added " + str(root))
    Reduce(root)
    return root
    
def Reduce(tree):
    while True:
        exploded = tree.ExplodeIfNeeded()
        if exploded:
            #print("exploded " + str(tree))
            continue
        split = tree.SplitIfNeeded()
        if not split:
            break
        else:
            pass
            #print("split " + str(tree))

sum = input[0]
for i in range(1,len(input)):
    sum = Add(sum,input[i])
print(sum.GetMagnitude())

#part b
highestMagnitude = 0
for i in range(len(input)):
    for j in range(len(input)):
        if i == j:
            continue
        magnitude = Add(input[i],input[j]).GetMagnitude()
        if magnitude > highestMagnitude:
            highestMagnitude = magnitude
print(highestMagnitude)