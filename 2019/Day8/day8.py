with open("input.txt", "r") as FILE:
   width = 25
   height = 6
   layers = []

   line = FILE.readline()
   digits = [int(c) for c in line.strip()]
   
   layerSize = width*height
   
   numLayers = len(digits)/layerSize
   
   for i in xrange(numLayers):
      layer = digits[i*layerSize:(i+1)*layerSize]
      layers.append(layer)
   
   #part 1
   '''
   fewest0Digits = layerSize
   fewest0Layer = -1
   
   for layer in layers:
      numZeroes = 0
      for digit in layer:
         if digit == 0:
            numZeroes += 1
      if numZeroes < fewest0Digits:
         fewest0Digits = numZeroes
         fewest0Layer = layer
         
   ones = [i for i in fewest0Layer if i == 1]
   twos = [i for i in fewest0Layer if i == 2]
   
   print len(ones)*len(twos)
   '''
   
   composite = []
   for i in xrange(layerSize):
      pixel = 2
      for layer in layers:
         if layer[i] == 2:
            continue
         else:
            pixel = layer[i]
            break
      composite.append(pixel)
   
   outStr = ""
   for y in xrange(0,height):
      for x in xrange(0,width):
         i = x+y*width
         if composite[i] == 0:
            outStr += " "
         else:
            outStr += "#"
         #outStr += str(composite[i])
      outStr += "\n"
   print outStr