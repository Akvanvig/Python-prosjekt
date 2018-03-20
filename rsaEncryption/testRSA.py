from hans import encrypt
from hans import decrypt
from hans import generate_keypair
from rsaFactor import main

keyPair = generate_keypair()
tekst = 'a'
encrypted = encrypt(keyPair[0], tekst)
#main(listeChar, kryptModulo, pubKey)
print(tekst)
main(encrypted, keyPair[0][1], keyPair[0][0])
