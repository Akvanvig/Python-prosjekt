import time
#Svar -2
tekst = 'judwxohuhuCghuhCkduCixqqhwCphoglqjhqD'
listeTegn = list(tekst)
shift = -1
sumShift = 0
#Kjører til bruker avbryter med ctrl + c
while True:
    for i in range(0,len(listeTegn)):
        verdiTegn = ord(listeTegn[i])
        verdiTegn += shift
        if verdiTegn > 255:
            verdiTegn -= 256
        elif verdiTegn < 0:
            verdiTegn += 256
        listeTegn[i] = chr(verdiTegn)
    printOut = ''.join(listeTegn)
    print(printOut + " - " + str(sumShift))
    sumShift += shift
    time.sleep(1)
