#Settings:
values = [360, 83, 59, 130, 431, 67, 230, 52, 93,
            125, 670, 892, 600, 38, 48, 147, 78, 256,
            63, 17, 120, 164, 432, 35, 92, 110, 22,
            42, 50, 323, 514, 28, 87, 73, 78, 15,
            26, 78, 210, 36, 85, 189, 274, 43, 33,
            10, 19, 389, 276, 312]
weights = [[7, 0, 30, 22, 80, 94, 11, 81, 70,
            64, 59, 18, 0, 36, 3, 8, 15, 42,
            9, 0, 42, 47, 52, 32, 26, 48, 55,
            6, 29, 84, 2, 4, 18, 56, 7, 29,
            93, 44, 71, 3, 86, 66, 31, 65, 0,
            79, 20, 65, 52, 13]]
capacities = [850]

#Tar imot 2d liste:
#   0, 1 = values, weights
#   2 = weightedValues
def bubblesort(liste):
    for runde in range(len(liste[0]) - 1, 0, -1):
        uendret = True
        for i in range(runde):
            if liste[2][i] < liste[2][i + 1]:
                liste[0][i],liste[0][i + 1] = liste[0][i + 1],liste[0][i]
                liste[1][i],liste[1][i + 1] = liste[1][i + 1],liste[1][i]
                liste[2][i],liste[2][i + 1] = liste[2][i + 1],liste[2][i]
                uendret = False
        if (uendret):
            break
    return liste

def main():
    weightedValue = []
    for i in range(0,len(values)):
        if weights[0][i] == 0:
            weightedValue.append(999999)
        else:
            weightedValue.append(values[i] / weights[0][i])

    sortingList = [values, weights[0], weightedValue]
    sortingList = bubblesort(sortingList)

    weightAdded = 0
    valueAdded = 0
    itemsAdded = [] #Value, weight
    for i in range(0,len(sortingList[0])):
        if weightAdded + sortingList[1][i] <= capacities[0]:
            itemsAdded.append([sortingList[0][i], sortingList[1][i]])
            weightAdded += sortingList[1][i]
            valueAdded += sortingList[0][i]
        if weightAdded == 850:
            break

    print(itemsAdded)
    print()
    print(str(weightAdded) + ' ' + str(valueAdded))

main()
