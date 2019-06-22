#Mottar ei liste, og deler denne opp i to tilnærmet like store lister
def splittListe(l):
    midtpunkt = len(l) // 2
    l1 = l[:midtpunkt]
    l2 = l[midtpunkt:]
    return l1, l2

#Slår sammen listene sortert
def slaaSammenSortert(l1, l2):
    #Hvis ei av listene er tomme
    if len(l1) == 0:
        return l2
    elif len(l2) == 0:
        return l1

    #Alle andre tilfeller
    #Antar begge listene er sortert
    index1, index2 = 0,0
    resListe = []
    lenLister = len(l1) + len(l2)

    while len(resListe) < lenLister:
        #Legger til objekt fra liste1 om den er mindre eller lik, ellrs neste objekt i liste 2
        if l1[index1] <= l2[index2]:
            resListe.append(l1[index1])
            index1 += 1
        else:
            resListe.append(l2[index2])
            index2 += 1

        #Om en når slutten på ei av listene, legges resten fra andre til
        if index1 == len(l1):
            resListe.extend(l2[index2:])
            break
        elif index2 == len(l2):
            resListe.extend(l1[index1:])
            break

    return resListe


def mergeSort(liste):
    if len(liste) <= 1:
        return liste
    else:
        l1, l2 = splittListe(liste)
        print(l1, l2)           #Skriver ut hva som vurderes i prosessen
        return slaaSammenSortert(mergeSort(l1), mergeSort(l2))

if __name__ == "__main__":
    l = [1,2,5,2,3,9]
    print(l)
    l1, l2 = splittListe(l)
    print(l1, l2)
    print(slaaSammenSortert(l1,l2))

    print()
    l = [1,5,2,3,9]
    print(l)
    l1, l2 = splittListe(l)
    print(l1, l2)
    print(slaaSammenSortert(l1,l2))

    #Samlet test
    print()
    l = [4,32,7,1,5,0,-2]
    print(l)
    print(mergeSort(l))
