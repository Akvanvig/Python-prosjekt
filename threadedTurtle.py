"""
	Title:	testTimerTurtle.py
	Date:	10.03.2018
	Author:	Anders Kvanvig
"""
import turtle
import time
import threading

#Settings
numPoints = 12     #Points that should be put down
radius = -200       #Half the diameter of the circle :)
multiplier = 2
turtleSpeed = 0     #(0-10)0 is fastest, 10 fast, 1 slow
countTurtles = 4    #Must be divisible by number of points


                        #          0      1     2      3        4        5     6        7
def drawCircle(ts, nr): # ts = [turtle, posX, posY, heading, numPoints, dpp, radius, points[]]
    ts[nr][0].penup()
    ts[nr][0].setpos(ts[nr][1],ts[nr][2])
    ts[nr][0].setheading(ts[nr][3])
    ts[nr][0].pendown()
    i = 0
    while i < ts[nr][4]:
        ts[nr][0].circle(ts[nr][6], ts[nr][5])
        ts[nr][0].dot(7,'red')
        ts[nr][7][0].append(ts[nr][0].xcor())
        ts[nr][7][1].append(ts[nr][0].ycor())
        print('(' + str(ts[nr][0].xcor()) + ',' + str(ts[nr][0].ycor()) + ')')
        i += 1

    ts[nr][1] = ts[nr][0].xcor()
    ts[nr][2] = ts[nr][0].ycor()
    ts[nr][3] = ts[nr][0].heading()


def main():
    ts = [] # ts[x] = [turtle, posX, posY, heading, numPoints, dpp, radius, points[]
    dpp = 360 / numPoints
    points = [[],[]],    [[],[]],    [[],[]],    [[],[]]

    i = 0
    startPos = []
    lars = turtle.Turtle()
    lars.speed(turtleSpeed)
    lars.penup()
    lars.setpos(radius, 0)
    lars.left(90)
    while i < countTurtles:
        startPos.append([lars.xcor(), lars.ycor()])
        ts.append([turtle.Turtle(), lars.xcor(), lars.ycor(), lars.heading(), (numPoints/countTurtles), dpp, radius, points[i]])
        ts[i][0].speed(turtleSpeed)
        lars.circle(radius, (360 / countTurtles))
        i += 1

    lars.setpos(0,0)

    #creates new threads to draw the circle
    myThreads = []
    for j in range(0,countTurtles):
        t = threading.Thread(target=drawCircle, args=(ts,j))
        myThreads.append(t)

    #Starts threads
    for t in myThreads:
        t.start()

    window.mainloop()

    #Waites for threads to finish and rejoin program
    for t in myThreads:
        t.join()

    #Verifies number of points created
    countPoints = 0
    for j in range(0, countTurtles):
        countPoints += len(ts[j][7][0])
    print('fullført sirkel - ' + str(countPoints))

    #Adds all points to common list
    listPoints = [[]] * numPoints
    countr = 0
    for j in range(0,countTurtles):
        for k in range(0,len(points[j][0])):
            listPoints[countr] = [points[j][0][k],points[j][1][k]]
            countr += 1

    
window = turtle.Screen()
main()
window.exitonclick()
