import random
random.seed('Hemmelig123')

strHex = 'c15c5cc658fb8910abea5ff1c3a8a97d99cb'
forste = True
listInt = []
temp = ''
#Legger to og to hex-verdier i variabel og konverterer til dec
for i in range(0,len(strHex)):
    if forste:
        temp = strHex[i]
        forste = False
    else:
        temp += strHex[i]
        listInt.append(int(temp,16))
        forste = True

#Genererer KeyStream
listKeyStream = []
for value in listInt:
    listKeyStream.append(random.randint(0,255))

#Kjører xor på de to listene og gjør om til char
listChar = []
for i in range(0, len(listInt)):
    listChar.append(chr(listInt[i]^listKeyStream[i]))

print(''.join(listChar))
