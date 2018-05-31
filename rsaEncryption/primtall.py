#Genererer primtall
def getPrimtall(n):
    liste = [2,3]
    print(1)
    print(2)
    print(3)
    for i in range(3,n):
        erPrimtall = True
        for tall in liste:
            if i % tall == 0:
                erPrimtall = False
                break
        if erPrimtall:
            print(i)

getPrimtall(1000000)
