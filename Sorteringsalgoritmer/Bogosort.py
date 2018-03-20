import random
import time
erSortert = False

#
def shuffle(tekst):
    temp = list(tekst)      #Ordet legges over i ei liste
    random.shuffle(temp)
    res = ''.join(temp)
    return res

#Tester om teksten er sortert
def test(tekst):
    liste = list(tekst)                         #legger ordet i ei liste for å kunne kjøre gjennom med løkke
    erSortert = True
    for i in range(len(tekst) - 1):
        if (ord(liste[i]) > ord(liste[i+1])):   #Sjekker om gjeldende tegn er større enn neste tegn på lista
            erSortert = False
            break                               #Bryter løkka om neste tegn er mindre enn gjeldende
    return erSortert                            #Returnerer svar på om lista er sortert

#----------------Hovedløp----------------#

tekst = input('skriv noe: ')#Ber bruker om noen tegn som skal sorteres
Forsok = 0
start = time.time()         #Henter Start-tidspunktet (brukes for å beregne kjøretid)
print(tekst)                #Skriver hva bruker førte inn som original tekst
erSortert = test(tekst)     #sjekker om startpunkt er sortert fra før
while not erSortert:        #Hvis ikke stringen er sortert, stokkes det om
    tekst = shuffle(tekst)  #Kjører shuffle-funksjonen for å endre teksten
    Forsok += 1
    print(tekst + ' Forsøk nr: ' + str(Forsok))            #Skriver resultat av shuffle til bruker
    erSortert = test(tekst) #Sjekker om lista er sortert
slutt = time.time()         #Henter Slutt-tidspunktet
#print(slutt - start)       #Skriver kjøretid til bruker
print('{0:.3f} seconds'.format((slutt - start))) #Skrives som '0.000 seconds'
