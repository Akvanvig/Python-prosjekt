import time

def bubblesort(liste):
    for runde in range(len(liste) - 1, 0, -1):
        print(liste)
        uendret = True
        for i in range(runde):
            if liste[i] > liste[i + 1]:
                liste[i],liste[i + 1] = liste[i + 1],liste[i]
                uendret = False
        if (uendret):
            break
    return (liste)

if __name__ == "__main__":
    tekst = input('Skriv noe: ')
    start = time.time()
    liste = list(tekst)
    tekst = ''.join(bubblesort(liste))
    slutt = time.time()
    print('{0:.3f} seconds'.format((slutt - start)))
