import sys #Brukes for å lese parametre

#Standard variabler
innstillinger = {
    'inputfil' : ".\\tekstfil.txt",
    'outputfil' : ".\\resultat.txt",
    'antallTegn' : 2000,
    'kuttVedMellomrom' : False,
    'kuttVedPunktum' : False,
    'hjelp' : False
}
argVar = {
    'inputfil' : "i",
    'outputfil' : "o",
    'antallTegn' : "n",
    'kuttVedMellomrom' : "m",
    'kuttVedPunktum' : "p",
    'hjelp' : "h"
}
hjelpMelding = '''Mulige argumenter:
    Endre inputfil:             -{inputfil}
    Endre outputfil:            -{outputfil}

    Endre antall tegn pr del:   -{antallTegn} [int antall tegn]

    Kutt tekst ved mellomrom:   -{kuttVedMellomrom}
    Kutt tekst ved punktum:     -{kuttVedPunktum}

    Hjelp:                      -{hjelp}
'''.format(**argVar)


def tolkArgumenter(args):
    args = args[1:] #Fjerner første argument (filnavn)
    for i in range(0,len(args)):
        if args[i].startswith("-"):
            arg = args[i][1:].lower() #Fjerner første tegn (-)
            #Legger til
            if arg.startswith(argVar["antallTegn"]):         #Sett antall tegn
                if args[i+1].isnumeric():
                    innstillinger['antallTegn'] = int(args[i+1])
                else:
                    print('Kunne ikke endre antall tegn til {}'.format(args[i+1]))
            elif arg.startswith(argVar["inputfil"]):   #Sett inputfil
                innstillinger['inputfil'] = args[i+1]
            elif arg.startswith(argVar["outputfil"]):   #Sett outputfil
                innstillinger['outputfil'] = args[i+1]
            elif arg.startswith(argVar["kuttVedMellomrom"]):   #Sett kuttVedMellomrom
                innstillinger['kuttVedMellomrom'] = True
                innstillinger['kuttVedPunktum'] = False
            elif arg.startswith(argVar["kuttVedPunktum"]):   #Sett kuttVedPunktum
                innstillinger['kuttVedMellomrom'] = False
                innstillinger['kuttVedPunktum'] = True
            elif arg.startswith(argVar["hjelp"]):   #Sett Hjelp
                innstillinger['hjelp'] = True

def lesFil(filnavn):
    innhold = ""
    try:
        innhold = open(filnavn, "r").read()
    except Exception as e:
        print(e)
    return innhold

def skrivFil(filnavn, innhold):
    f = open(filnavn, "w+")
    for i in range(0,len(innhold)):
        f.write('{} \n\n\n\n\n'.format(innhold[i]))
    f.close()


#Finner siste sted gitt tegnkombinasjon oppstår, og kutter teksten her.
#Returner liste med tekstavsnitt
def kutt(tekst, maksAntTegn, tegn) -> list:
    maksTegnString = tekst[:(maksAntTegn-len(tegn))]    #Kutter tekst til maks antall tegn
    antTegn = maksTegnString.rfind(tegn) + len(tegn)    #Finner høyeste index hvor kombinasjon er funnet

    #Hvis det er mer enn maks antall tegn igjen kaller funksjonen seg selv med resten av teksten
    if len(tekst) > maksAntTegn: #Hvis det er mer enn maks antall tegn igjen
        tekstListe = kutt(tekst[antTegn:], maksAntTegn, tegn)
        #Legger til teksten herfra først i listen
        tekstListe.insert(0, tekst[:antTegn])

    else:   #Hvis det bare er en del igjen
        tekstListe = [tekst]

    return tekstListe

def Main():
    #Henter innhold fra oppgitt fil:
    innhold = lesFil(innstillinger['inputfil'])

    #Setter innstillinger til oppgitte verdier
    kuttTegn = ""
    if innstillinger['kuttVedPunktum']:
        kuttTegn = "."
    elif innstillinger['kuttVedMellomrom']:
        kuttTegn = " "

    #Splitter tekst til ønsket lengde
    tekstListe = kutt(innhold, innstillinger['antallTegn'], kuttTegn)

    #Skriver ut info om deler
    print("Antall deler: " + str(len(tekstListe)))
    for i in range(0,len(tekstListe)):
        print('     Del {:<3} lengde: {}'.format(i, len(tekstListe[i])))

    #Skriver deler til fil
    skrivFil(innstillinger['outputfil'], tekstListe)


if __name__ == '__main__':
    #Sjekker argumenter
    if len(sys.argv) > 1:
        tolkArgumenter(sys.argv)

    #Verifisering av innstillinger
    print('''Innstillinger:
    Inputfil:               {inputfil}
    Outputfil:              {outputfil}
    Maks tegn pr del:       {antallTegn}
    Kutt ved mellomrom:     {kuttVedMellomrom}
    Kutt ved punktum:       {kuttVedPunktum}
    Hjelp:                  {hjelp}
    '''.format(**innstillinger))

    #Gjennomfører oppdeling
    if innstillinger['hjelp']:
        print(hjelpMelding)
    else:
        Main()
