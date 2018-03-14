import math
from hans import decrypt
from hans import gcd
from hans import multiplicative_inverse as multiplicativeInverse

#Settings:
listeChar = [84620, 66174, 66174, 5926, 9175, 87925, 54744, 54744, 65916, 79243, 39613, 9932, 70186, 85020, 70186, 5926, 65916, 72060, 70186, 21706, 39613, 11245, 34694, 13934, 54744, 9932, 70186, 85020, 70186, 54744, 81444, 32170, 53121, 81327, 82327, 92023,34694, 54896, 5926, 66174, 11245, 9175, 54896, 9175, 66174, 65916, 43579, 64029, 34496, 53121, 66174, 66174, 21706, 92023, 85020, 9175, 81327, 21706, 13934, 21706, 70186, 79243, 9175, 66174, 81327, 5926, 74450, 21706, 70186, 79243, 81327, 81444, 32170, 53121]
kryptModulo = 100127
pubKey = 29815

def main(intListe, n, publicKey):
    keys = getNokkel(n, publicKey)
    print(keys)
    for key in keys:
        tekst = decrypt(key[1], intListe)
        if not tekst.startswith('h'):
            tekst = decrypt(key[0], intListe)
        try:
            print(tekst + str(key))
        except Exception as e:
            print(e)


#Henter mulige nøkler
def getNokkel(n, publicKey):
    primtallListe = getPrimtall(math.floor(math.sqrt(n)))

    primtall = []

    funnet = False
    #finner p ved primtallfaktorisering
    for tall in primtallListe:
        if n % tall == 0:
            funnet = True
            primtall.append(tall)

    if funnet:
        resultat = []
        for p in primtall:
            #Regner ut q (n / p = q)
            q = int(n / p)

            phi = (p-1) * (q-1)

            e = publicKey

            #Use Extended Euclid's Algorithm to generate the private key
            d = multiplicativeInverse(e, phi)

            #Return public and private keypair
            #Public key is (e, n) and private key is (d, n)
            resultat.append([[e, n], [d, n]])
        return resultat
    else:
        return [[[0,0],[0,0]]]

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

print()
main(listeChar, kryptModulo, pubKey)
