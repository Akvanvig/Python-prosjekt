import multiprocessing
from multiprocessing import Pool, Queue, Manager
import random
import time


#Mottar en kode og gjetter frem til svaret er funnet, eller den mottar ett stopp signal
def main():
    #variabler
    ord = "bogo"
    minTegn = 4
    maxTegn = 4

    #Tegnsett
    smallLetters = "abcdefghijklmnopqrstuvwxyzæøå"
    largeLetters = "ABCDEFGHIJKLMNOPQRSTUVWXYZÆØÅ"
    numbers = "0123456789"
    commonSymbols = ".,?!- "
    otherSymbols = ":;_+/\\*'\"<>~^¨$£#¤%&([{]})=|§`´"

    #tegn brukt
    tegn = smallLetters + "ABCDEF"#smallLetters + largeLetters + numbers

    #Spinn opp en tråd pr kjerne:
    kjerner = multiprocessing.cpu_count()
    print('ant kjerner: {}'.format(kjerner))
    pool = Pool(processes=kjerner)
    res = [pool.apply_async(crack, (ord, tegn, minTegn, maxTegn, queue)) for i in range(kjerner)] #Ender i en exception

    results = []
    for i in range(len(res)):
        if i == 0:
            results.append([i, res[i].get(10000)])
        else:
            results.append([i, res[i].get(1)])
    print(results)

def crack(kodeord, lovligeTegn, minLengde, maxLengde, q):
    while True:
        lengde = random.randint(minLengde, maxLengde)   #Velger en lengde innenfor angitte muligheter
        gjettetOrd = ''.join(random.choices(lovligeTegn, k=lengde)) #Velger gitt antall tegn fra den gitte tegnlisten
        #print(kodeord, gjettetOrd)
        if kodeord == gjettetOrd:
            print("-----------------------")
            q.put(gjettetOrd)
            return gjettetOrd
        elif not q.empty(): #Sjekker om noen av de andre trådene har funnet ordet
            break


if __name__ == '__main__':
    startpunkt = time.time()
    m = Manager()
    queue = m.Queue()

    try:
        main()
    except Exception as e:
        print('exception: {}'.format(e))

    sluttpunkt = time.time()
    print('\n\nOrd mottat: {}'.format(queue.get()))
    print('mottat svar etter {0:.3f} sekunder'.format(sluttpunkt - startpunkt))
