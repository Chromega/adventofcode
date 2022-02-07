
   
def runIntcodeProgram(codes):
   opcodeIndex = 0
   while True:
      opcode = codes[opcodeIndex]
      
      if opcode == 1:
         arg1 = codes[opcodeIndex+1]
         arg2 = codes[opcodeIndex+2]
         arg3 = codes[opcodeIndex+3]
         codes[arg3] = codes[arg1]+codes[arg2]
      elif opcode == 2:
         arg1 = codes[opcodeIndex+1]
         arg2 = codes[opcodeIndex+2]
         arg3 = codes[opcodeIndex+3]
         codes[arg3] = codes[arg1]*codes[arg2]
      elif opcode == 99:
         break
      else:
         print 'bad news...'
      
      opcodeIndex += 4
   return codes

def part1():
   with open("input.txt", "r") as FILE:
      line = FILE.readline()
      codes = [int(element) for element in line.strip().split(',')]
      
      print codes
      
      codes[1] = 12
      codes[2] = 2
      codes = runIntcodeProgram(codes)
      
      print codes
      
def part2():
   with open("input.txt", "r") as FILE:
      line = FILE.readline()
      codes = [int(element) for element in line.strip().split(',')]
      
      for noun in xrange(0,len(codes)):
         for verb in xrange(0,len(codes)):
            codesCopy = codes[:]
            codesCopy[1] = noun
            codesCopy[2] = verb
            codesCopy = runIntcodeProgram(codesCopy)
            if (codesCopy[0] == 19690720):
               return 100 * noun + verb
print part2()