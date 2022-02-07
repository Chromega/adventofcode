def MakeFFTMatrix(size):
   matrix = []
   for generation in xrange(size):
      row = []
      step = 0
      positionWithinStep = 0
      for i in xrange(size):
         positionWithinStep += 1
         if positionWithinStep > generation:
            step += 1
            positionWithinStep = 0
         
         if step%4 == 0:
            row.append(0)
         elif step%4 == 1:
            row.append(1)
         elif step%4 == 2:
            row.append(0)
         else:
            row.append(-1)
      matrix.append(row)
   return matrix
   
def ApplyFFTToRow(signal, row):
   result = 0
   for i in xrange(len(signal)):
      result += signal[i]*row[i]
   if result >= 0:
      return result%10 #yay sensible % operator
   else:
      return (-result)%10
   
def ApplyFFT(signal, matrix):
   result = []
   for i in xrange(len(signal)):
      result.append(ApplyFFTToRow(signal, matrix[i]))
   return result
      
def MatMask(mat, col):
   out = []
   size = len(row)
   for x in xrange(size):
      sum = 0
      for y in xrange(size):
         sum += col[y]*mat[y][x]
      out.append(sum)
   return out
   
#assumes from back half of data
def FasterFFT(signal):
   out = [0 for i in xrange(len(signal))]
   out[-1] = signal[-1]
   for i in xrange(len(signal)-1):
      j = len(signal)-1-i-1
      out[j] = (signal[j] + out[j+1])%10
   return out

with open("input.txt", "r") as FILE:
   line = FILE.readline()
   signal = [int(element) for element in line.strip()]
   
   
   #PART A
   """print "Start Signal: " + str(signal)
   
   fftMatrix = MakeFFTMatrix(len(signal))
   
   for i in xrange(100):
      signal = ApplyFFT(signal, fftMatrix)
   print signal"""
   
   #print FasterFFT(signal)
   
   #PART B
   
   signal = 10000*signal
   print len(signal)
   offset = 0
   for digit in signal[0:7]:
      offset *= 10
      offset += digit
   print offset
   
   reducedSignal = signal[offset:]
   
   for i in xrange(100):
      reducedSignal = FasterFFT(reducedSignal)
      
   print reducedSignal[0:8]
   
   
   #See below, second half of data follows pattern where can be computed based on
   #its value and the one below it.  Sneaky buggers, input is in the back half with
   #the offset they gave, need to know data for this optimization
   """
   fftMatrix = MakeFFTMatrix(16)
   for row in fftMatrix:
      rowTxt = ""
      for elt in row:
         rowTxt += str(elt)
         rowTxt += '\t'
      print rowTxt"""
   """
   print MatMask(fftMatrix, [0,0,0,0,0,0,0,1])
   print MatMask(fftMatrix, [0,0,0,0,0,0,1,-1])
   print MatMask(fftMatrix, [0,0,0,0,0,1,-1,0])
   print MatMask(fftMatrix, [0,0,0,0,1,-1,0,0])
   print MatMask(fftMatrix, [0,0,0,1,-1,0,0,1])
   print MatMask(fftMatrix, [0,0,1,-1,0,1,0,0])
   print MatMask(fftMatrix, [0,1,-1,1,0,0,0,0])
   print MatMask(fftMatrix, [1,0,1,-1,-1,2,1,-2])
   """
   """
   print MatMask(fftMatrix, [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1])
   print MatMask(fftMatrix, [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,-1])
   print MatMask(fftMatrix, [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,-1, 0])
   print MatMask(fftMatrix, [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,-1, 0, 0])
   print MatMask(fftMatrix, [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,-1, 0, 0, 0])
   print MatMask(fftMatrix, [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,-1, 0, 0, 0, 0])
   print MatMask(fftMatrix, [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,-1, 0, 0, 0, 0, 0])
   print MatMask(fftMatrix, [ 0, 0, 0, 0, 0, 0, 0, 0, 1,-1, 0, 0, 0, 0, 0, 0])
   print MatMask(fftMatrix, [ 0, 0, 0, 0, 0, 0, 0, 1,-1, 0, 0, 0, 0, 0, 0, 1])
   print MatMask(fftMatrix, [ 0, 0, 0, 0, 0, 0, 1,-1, 0, 0, 0, 0, 0, 1, 0,-1])
   print MatMask(fftMatrix, [ 0, 0, 0, 0, 0, 1,-1, 0, 0, 0, 0, 1, 0,-1, 0, 0])
   print MatMask(fftMatrix, [ 0, 0, 0, 0, 1,-1, 0, 0, 0, 1, 0,-1, 0, 0, 1, 0])
   print MatMask(fftMatrix, [ 0, 0, 0, 1,-1, 0, 0, 1, 0,-1, 0, 1, 0, 0,-1, 0])
   print MatMask(fftMatrix, [ 0, 0, 1,-1, 0, 1, 0,-1, 1, 0, 0,-1, 0, 0,-1, 0])
   print MatMask(fftMatrix, [ 0, 1,-1, 1, 0, 0, 0, 0,-1,-1, 0, 3, 0, 1, 1,-2])
   print MatMask(fftMatrix, [ 1, 0, 1,-1,-1, 2, 1,-2, 0, 0, 1,-1,-1, 2,-1,-2])"""