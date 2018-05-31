"""
    Anders Kvanvig
    31.05.18
    Brute.py

    Brute-forces given passwords and gives time used
"""
import time

#Sets of symbols that can be used for cracking passwords, any other sets of symbols can be added beneath
smallLetters = "abcdefghijklmnopqrstuvwxyzæøå"
largeLetters = "ABCDEFGHIJKLMNOPQRSTUVWXYZÆØÅ"
numbers = "0123456789"
commonSymbols = ".,?!- "
otherSymbols = ":;_+/\\*'\"<>~^¨$£#¤%&([{]})=|§`´"

#Settings
password    = "T4*?"
symbols     = smallLetters + largeLetters + numbers + commonSymbols + otherSymbols
maxLength   = 5

def startup():
    print("start")
    start = time.time()
    res = brute(password, symbols, maxLength)
    slutt = time.time()
    print(res)
    print('{0:.3f} sekunder'.format((slutt - start)))

def brute(p, sym, mL): #Password, symbols and maxLength
    listChars = list(sym)
    l = len(listChars) - 1
    word = list(listChars[0])
    for i in range(1, mL):  #Number of chars in password, Runs until password is found, or limit reached
        #print("length tested = " + str(i))  #Prints the length of current words getting tested
        word = list(i * listChars[0])
        while "".join(word) != (i * listChars[l]):   #all possibilities tested, Runs until it reaches last char time number of chars guessed
            if "".join(word) == p:
                return word
            word = increaseVal(word, listChars, l, i - 1)


def increaseVal(word, listChars, numChr, place):    #Increses value of string (word) according to given symbols
    x = listChars.index(word[place])
    if x == numChr:
        word = increaseVal(word, listChars, numChr, place - 1)  #Calls itself given one place lower in the string (letter in front)
        x = 0
        word[place] = listChars[x]
        #print(word)    #Prints the current word when anything but the last value gets changed
        return word
    else:
        word[place] = listChars[x + 1]
        return word

startup()
