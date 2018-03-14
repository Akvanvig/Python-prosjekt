from hans import encrypt
from hans import decrypt
from hans import generate_keypair

keyPair = generate_keypair()
print(keyPair)

publicKey = keyPair[0]
privateKey = keyPair[1]
print(privateKey)
krypt = encrypt(publicKey, 'hDette er teksten')
print(krypt)
print()
print(decrypt(privateKey, krypt))
