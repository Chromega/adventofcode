def CheckNumber(num):
   digits = []
   for i in xrange(6):
      digits.insert(0,num%10)
      num/=10
   
   hadDuplicateDigits=False
   duplicateDigitValue=-1
   lastDigit=-1
   runOfDigits=0
   for digit in digits:
      if digit < lastDigit:
         return False
      if digit == lastDigit:
         #Part 2 code here
         runOfDigits += 1
         if runOfDigits > 2:
            if duplicateDigitValue == digit:
               hadDuplicateDigits = False
         else:
            if not hadDuplicateDigits:
               hadDuplicateDigits = True
               duplicateDigitValue = digit
         #end part 2 code
            
         #hadDuplicateDigits = True
      else:
         runOfDigits = 1
      lastDigit = digit
   return hadDuplicateDigits
   
total = 0
for i in xrange(124075, 580769+1):
   if CheckNumber(i):
      total += 1
      print i
      
print total