import json
filSti = '.\\test.json'
navnListe = ['Per', 'Arne', 'Lars']
alderListe = [23, 43, 27]


def skrivJson():
    personer = []
    for i in range(0, len(navnListe)):
        personer.append(dict(navn=navnListe[i], alder=alderListe[i]))

    with open(filSti, 'w') as fout:
        json.dump(personer, fout)

def lesJson():
    with open(filSti, 'r') as fout:
        return json.load(fout)

#skrivJson()
print(lesJson())
