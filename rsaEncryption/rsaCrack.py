from hans import decrypt

#Settings
primtallUnder = 64328
startPrimtallNr = 6435
keyN = 100127

#Genererer primtall
def getPrimtall(n):
    liste = [2,3]
    for i in range(3,n):
        erPrimtall = True
        for tall in liste:
            if i % tall == 0:
                erPrimtall = False
                break
        if erPrimtall:
            liste.append(i)
    return liste

def main():
    #Melding som har blitt kryptert
    intListe = [84620, 66174, 66174, 5926, 9175, 87925, 54744, 54744, 65916, 79243, 39613, 9932, 70186, 85020, 70186, 5926, 65916, 72060, 70186, 21706, 39613, 11245, 34694, 13934, 54744, 9932, 70186, 85020, 70186, 54744, 81444, 32170, 53121, 81327, 82327, 92023, 34694, 54896, 5926, 66174, 11245, 9175, 54896, 9175, 66174, 65916, 43579, 64029, 34496, 53121, 66174, 66174, 21706, 92023, 85020, 9175, 81327, 21706, 13934, 21706, 70186, 79243, 9175, 66174, 81327, 5926, 74450, 21706, 70186, 79243, 81327, 81444, 32170, 53121]

    primtallListe = []
    primtallListe = getPrimtall(primtallUnder)
    print('primtall hentet --> ' + str(len(primtallListe)))

    for i in range(startPrimtallNr,len(primtallListe)):
        nokkel = [primtallListe[i], keyN]
        melding = decrypt(nokkel, intListe)
        #Sjekker om riktig melding ut fra hintet er mottatt
        if melding.startswith("h"):
            print(melding + " - pk = " + str(primtallListe[i]))
    print('fullført')

main()
