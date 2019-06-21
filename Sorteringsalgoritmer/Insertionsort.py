liste = [0, 5, 32, 1, 3, 22, 102, -22]

def insertionsort(liste):
    lengde = len(liste)
    min = 0                                 #minimumsverdi funnet i denne gjennomgangen
    for x in range(0, lengde - 1):
        min = x
        for y in range(x + 1, lengde):
            if liste[min] > liste[y]:       #Sjekker om gjeldene element er større enn forrige minste noterte
                min = y
        liste[min], liste[x] = liste[x], liste[min]
        print(liste)
    return liste

print(liste)
liste = insertionsort(liste)
print(liste)
