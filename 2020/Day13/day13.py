from typing import Tuple

def intTryParse(value):
    try:
        return int(value), True
    except ValueError:
        return value, False

   
def extended_euclid(a: int, b: int) -> Tuple[int, int]:
    """
    >>> extended_euclid(10, 6)
    (-1, 2)
    >>> extended_euclid(7, 5)
    (-2, 3)
    """
    if b == 0:
        return (1, 0)
    (x, y) = extended_euclid(b, a % b)
    k = a // b
    return (y, x - k * y)


# Uses ExtendedEuclid to find inverses
def chinese_remainder_theorem(n1: int, r1: int, n2: int, r2: int) -> int:
    """
    >>> chinese_remainder_theorem(5,1,7,3)
    31
    Explanation : 31 is the smallest number such that
                (i)  When we divide it by 5, we get remainder 1
                (ii) When we divide it by 7, we get remainder 3
    >>> chinese_remainder_theorem(6,1,4,3)
    14
    """
    (x, y) = extended_euclid(n1, n2)
    m = n1 * n2
    n = r2 * x * n1 + r1 * y * n2
    return (n % m + m) % m
  
startTime = -1
input = []
with open("input.txt") as FILE:
    startTime = int(FILE.readline().strip())
    input = [intTryParse(x)[0] for x in FILE.readline().strip().split(',')]
            
        
#part a 7:30
shortestWait = 9999999999
idOfShortestWait = 0
for id in input:
    if isinstance(id, int):
        m = startTime%id
        timeToWait = id-m
        if timeToWait < shortestWait:
            shortestWait = timeToWait
            idOfShortestWait = id
print(shortestWait*idOfShortestWait)

#part b 1:35:00
partBInput = []
for i in range(len(input)):
    id = input[i]
    if isinstance(id, int):
        partBInput.append((i,id))


#X%m=r
r = 0
m = 1
for j in range(0, len(partBInput)):
    i,id = partBInput[j]
    
    m2 = id
    r2 = id - i
    
    newR = chinese_remainder_theorem(m,r,m2,r2)
    newM = m*m2
    
    m = newM
    r = newR
    print((m,r))
print(r)


#print((modinv(7,13)*7*12)%(7*13))