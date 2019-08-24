import multiprocessing as mp
from math import floor
from time import time

def main():
    #tegnlister som kan brukes
    smallLetters = "abcdefghijklmnopqrstuvwxyzæøå"
    largeLetters = "ABCDEFGHIJKLMNOPQRSTUVWXYZÆØÅ"
    numbers = "0123456789"
    commonSymbols = ".,?!- "
    otherSymbols = ":;_+/\\*'\"<>~^¨$£#¤%&([{]})=|§`´"

    #Programvariabler
    startpunkt = "a"
    sluttpunkt = "999999"
    tegn = smallLetters + largeLetters + numbers
    kodeord = "T3sT"

    #Automatisk hentede variabler
    kjerner = mp.cpu_count()

    #print(bruteforce("accaa", "a", "aaaaaa", "abcd"))
    startSok(kodeord, startpunkt, sluttpunkt, tegn, kjerner)


def startSok(kodeord, startpunkt, sluttpunkt, tegn, antProsesser):
    #Finner Hvilke områder de forskjellige prosessene skal søke gjennom
    startArbeidsfordeling = time()
    sokerom = splittSokerom(startpunkt, sluttpunkt, tegn, antProsesser)
    print('Søkerom: \n{}\n'.format(sokerom))
    sluttArbeidsfordeling = time()

    #Starter opp prosesser for å lete etter svar
    pool = mp.Pool(antProsesser)
    print("Starter søk:")
    startSok = time()
    resultat = [pool.apply_async(bruteforce, (kodeord, sokerom[i][0], sokerom[i][1], tegn)) for i in range(antProsesser)]

    #Leser resultat fra prosessene
    resultaterStr = []
    for res in resultat:
        resultaterStr.extend(res.get(timeout=900))
    print('Resultat funnet: {}\n'.format(resultaterStr))
    sluttSok = time()

    print('Fordeling av arbeidsoppgaver tok: \n{0:.3f} sekunder \nOrdet ble funnet etter:\n{1:.3f} sekunder'.format(sluttArbeidsfordeling - startArbeidsfordeling, sluttSok -startSok))

def splittSokerom(startpunkt, sluttpunkt, tegn, antDeler):
    """
    Splitter rommet det skal søkes etter kodeord i opp i like store deler så det kan fordeles til forskjellige prosesser
    variabler:
        startpunkt = Adressen en skal begynne søket i (f.eks. "a")
        sluttpunkt = Adressen hvor søket skal avsluttes (f.eks. "ZZZZ")
        antDeler   = Hvor mange prosesser skal oppgavene fordeles til
    """
    sokerom = []
    avstand = beregnStorrelseStartSlutt(startpunkt, sluttpunkt, tegn)
    lengdePrDel = int(floor(avstand / antDeler))
    gjeldendeOrd = startpunkt
    gjeldendeVerdi = beregnVerdi(startpunkt, tegn)

    for i in range(antDeler):
        if i == antDeler - 1:
            sokerom.append([gjeldendeOrd, sluttpunkt])
        else:
            nesteVerdi = gjeldendeVerdi + lengdePrDel
            tempOrd = ordFraVerdi(nesteVerdi, tegn)
            sokerom.append([gjeldendeOrd, tempOrd])
            gjeldendeOrd = tempOrd
            gjeldendeVerdi = nesteVerdi

    return sokerom


def beregnStorrelseStartSlutt(startpunkt, sluttpunkt, tegn):
    """
    Beregner avstanden mellom start og sluttpunkt, og returnerer den på desimalform, skal brukes til å dele
    """
    #Startverdi
    verdiStart = beregnVerdi(startpunkt, tegn)

    #Sluttverdi
    verdiSlutt = beregnVerdi(sluttpunkt, tegn)

    avstand = verdiSlutt - verdiStart
    print('Startverdi: {}\nSluttverdi: {}\n'.format(verdiStart, verdiSlutt, avstand))
    return avstand

#Beregner verdien i base 10 ved (z*(x^y)+...+b*(x^2)+a*(x^1))
def beregnVerdi(ord, tegn):
    """
    Beregner verdien fra base x-tall til base 10-tall
    Tar inn variablene:
        ord     = ordet som det skal beregnes verdi for
        tegn    = alle tegnene som brukes (f.eks. "0123456789")
    """
    grunntall = len(tegn)
    grunntallsplass = len(ord) - 1
    verdi = 0
    for symbol in ord:
        verdiTegn = tegn.find(symbol)
        verdi += verdiTegn * (grunntall ** grunntallsplass)
        #print('Verdi: {}\nverdiTegn: {}\nindex Symbol: {}\ngrunntallsplass: {}'.format(verdi, verdiTegn, grunntall, grunntallsplass))
        grunntallsplass -= 1
    return verdi

def ordFraVerdi(verdi, tegn):
    """
    Beregner base-x ordet gitt base-10 verdien, og returnerer denne
    Variabler
        verdi   = base-10 verdien av kodeordet
        tegn    = verdiene kodeordet skal beregnes fra
    """
    grunntall = len(tegn)
    ord = ""
    while verdi != 0:
        rest = verdi % grunntall
        verdi = int((verdi - rest) / grunntall)
        ord = tegn[rest] + ord
    return ord

def bruteforce(kodeord, startpunkt, sluttpunkt, tegn):
    """
    Sjekker alle muligheter i gitt rom
    Variabler:
        kodeord     = ordet det letes etter
        startpunkt  = Tegn hvor det skal startes (eks. aa)
        sluttpunkt  = Tegn hvor det skal sluttes (eks. ZZZZ)
        tegn        = Tegn som kan brukes i kodeordet
    """
    lenTegn = len(tegn)
    ord = list(startpunkt)
    while True:
        ordStr = "".join(ord)
        if ordStr == kodeord:
            return ordStr
        elif ordStr == sluttpunkt or len(ordStr) > len(kodeord):
            #print('fullført \nord = {}\nlengde ord: {} av {}'.format(ordStr, len(ordStr), len(kodeord)))
            return ""
        ord = increaseVal(ord, tegn, lenTegn - 1, len(ordStr) - 1)


def increaseVal(ord, listeTegn, antTegn, plass):
    """
    Gir neste ordet som skal testes
    Variabler:
        ord         = nåværende ord (f.eks ZZ)
        listeTegn   = tegn som kan brukes i ordet
        antTegn     = antall tegn, brukes for å vite når den når siste tegn
        plass       = plassering i ordet som skal økes (kalles utenfra alltid på siste tegnet f.eks 4)
    """
    #print(ord, listeTegn, antTegn, plass)
    x = listeTegn.index(ord[plass])
    if x == antTegn:
        if plass == 0: #Sjekker om lengden på ordet må økes
            ord = list(listeTegn[0] * (len(ord) + 1))
        else:
            ord = increaseVal(ord, listeTegn, antTegn, plass - 1)  #Calls itself given one place lower in the string (letter in front)
            x = 0
            ord[plass] = listeTegn[x]
            #print(word)    #Prints the current word when anything but the last value gets changed (Will take a lot longer to run)
        return ord
    else:
        ord[plass] = listeTegn[x + 1]
        return ord


if __name__ == '__main__':
    main()
