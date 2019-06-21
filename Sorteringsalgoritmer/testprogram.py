import time
import Bubblesort as b, Selectionsort as s, Insertionsort as i
liste = [0, 5, 32, 1, 3, 22, 102, -22]

print()
print('Bubblesort:')
start = time.time()
ls = b.bubblesort(liste.copy())
slutt = time.time()
print(ls)
print('{0:.3f} seconds'.format((slutt - start)))


print()
print('Selectionsort:')
start = time.time()
ls = s.selectionsort(liste.copy())
slutt = time.time()
print(ls)
print('{0:.3f} seconds'.format((slutt - start)))


print()
print('Insertionsort:')
start = time.time()
ls = i.insertionsort(liste.copy())
slutt = time.time()
print(ls)
print('{0:.3f} seconds'.format((slutt - start)))
