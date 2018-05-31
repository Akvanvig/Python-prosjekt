"""
    Anders Kvanvig
    04.05.18
    Fraction.py

    Finds the lowest fraction made of integers given two integers (dividend & divisor)
"""

import math

numb1 = 1920    #dividend,  above
numb2 = 1080    #divisor,   below

def main(number1, number2):
    #Number one will be divided by number two
    f1, f2 = factor(number1), factor(number2)
    f1, f2 = removeCommon(f1, f2)
    res1, res2 = multiply(f1), multiply(f2)
    print(res1, res2)

#Takes in a list of numbers and multiplies them, returns result
def multiply(factors):
    res = 1
    for value in factors:
        res *= value
    return res

#cuts common numbers in the two given lists and returns the cut down versions
def removeCommon(factors1, factors2):
    i,j = 0,0
    while i < len(factors1) and j < len(factors2):
        if factors1[i] == factors2[j]:
            x = factors1[i]     #Integer we want to get out of lists
            factors1.remove(x)
            factors2.remove(x)
        elif factors1[i] > factors2[j]:
            j += 1
        elif factors1[i] < factors2[j]:
            i += 1

    return factors1, factors2

#Factorizes a number
def factor(number):
    primes = getPrimes(number + 1)  #+1 to avoid constant loop if given number is prime
    factors = []
    notOne = number != 1

    while notOne:   #While number hasn't reached 1
        for value in primes:
            if number % value == 0:
                factors.append(value)
                number /= value
                notOne = number != 1
                break

    return factors

#Generates primes up to given number
def getPrimes(n):
    list = [2,3]
    if n > 3:
        for i in range(3,n):
            isPrime = True
            for number in list:
                if i % number == 0:
                    isPrime = False
                    break
            if isPrime:
                list.append(i)

    return list

#startup
main(numb1, numb2)
