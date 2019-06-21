def insertionsort(liste):
    for x in range(1, len(liste)):
        for y in range(x, 0, -1):
            if liste[y - 1] > liste[y]:
                liste[y], liste[y - 1] = liste[y - 1], liste[y]
        print(liste)
    return liste

if __name__ == "__main__":
    liste = [0, 5, 32, 1, 3, 22, 102, -22]
    print(liste)
    liste = insertionsort(liste)
    print(liste)
