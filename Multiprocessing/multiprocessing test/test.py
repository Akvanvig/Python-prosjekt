import multiprocessing as mp
import time

def main():
    kjerner = mp.cpu_count()
    pool = mp.Pool(kjerner)

    resultsApplyResults = [pool.apply_async(workerProcess, ()) for i in range(kjerner)]
    results = []
    for res in resultsApplyResults:
        results.extend(res.get(timeout=10000))
    for res in results:
        print('Prosessen brukte {tidBrukt:.3f} sekunder på å finne passordet "{resultat}"'.format(**res))

def workerProcess():
    #Sets of symbols that can be used for cracking passwords, any other sets of symbols can be added beneath
    smallLetters = "abcdefghijklmnopqrstuvwxyzæøå"
    largeLetters = "ABCDEFGHIJKLMNOPQRSTUVWXYZÆØÅ"
    numbers = "0123456789"
    commonSymbols = ".,?!- "
    otherSymbols = ":;_+/\\*'\"<>~^¨$£#¤%&([{]})=|§`´"

    symbols = smallLetters + largeLetters + numbers
    startpunkt = time.time()
    res = brute("TesT01A", symbols, 7)
    sluttpunkt = time.time()
    return {'tidBrukt':(sluttpunkt - startpunkt), 'resultat': res}

def brute(p, sym, mL): #Password, symbols and maxLength
    listChars = list(sym)
    l = len(listChars) - 1
    word = list(listChars[0])
    for i in range(1, mL):  #Number of chars in password, Runs until password is found, or limit reached
        #print("length tested = " + str(i))  #Prints the length of current words getting tested
        word = list(i * listChars[0])
        countOptions = (l + 1) ** i - 1
        #print(countOptions)
        for j in range(0, countOptions):   #all possibilities tested, Checks all possibilities for current length word
            if "".join(word) == p:
                return word
            word = increaseVal(word, listChars, l, i - 1)
    return 'Kunne ikke finne passordet'


def increaseVal(word, listChars, numChr, place):    #Increses value of string (word) according to given symbols
    x = listChars.index(word[place])
    if x == numChr:
        word = increaseVal(word, listChars, numChr, place - 1)  #Calls itself given one place lower in the string (letter in front)
        x = 0
        word[place] = listChars[x]
        #print(word)    #Prints the current word when anything but the last value gets changed (Will take a lot longer to run)
        return word
    else:
        word[place] = listChars[x + 1]
        return word

if __name__ == '__main__':
    main()
