import time

def bubblesort(tekst):
    liste = list(tekst)
    for runde in range(len(liste) - 1, 0, -1):
        print(''.join(liste))
        uendret = True
        for i in range(runde):
            if liste[i] > liste[i + 1]:
                liste[i],liste[i + 1] = liste[i + 1],liste[i]
                uendret = False
        if (uendret):
            break
    return (''.join(liste))

tekst = input('Skriv noe: ')
start = time.time()
tekst = bubblesort(tekst)
slutt = time.time()
print('{0:.3f} seconds'.format((slutt - start)))
