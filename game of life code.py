import turtle

import random
import time

def drawScreenBorders():
    pen = turtle.Turtle()  
    pen.hideturtle()
    pen.penup()
    pen.goto(-350, 350)
    pen.pendown()
    for i in range(4):
        pen.forward(700)
        pen.right(90)

def initializeTheCells():
    cells = []
    for i in range(35):
        cells.append([])
        for j in range(35):
            newCell = turtle.Turtle()
            newCell.penup()
            newCell.shape("square")
            newCell.shapesize(stretch_wid=0.9, stretch_len=0.9)
            cells[i].append(newCell)
            rand = random.randint(0, 1)
            newCell.state = rand
            
            newCell.death_count = 0 # initalize death for each cell created
            
            if rand == 0:  # state 0 for being dead
                newCell.color("gray100")  # color white for being dead
                newCell.death_count = 0 
            else:
                newCell.color("gray0")  # color black for being alive
                newCell.death_count = 20
    return cells

def showTheUniverse(cells):
    ycor = 340
    for i in range(35):
        xcor = -340
        for j in range(35):
            cells[i][j].goto(xcor, ycor)
            xcor += 20
        ycor -= 20

def esc():
    global stop
    stop = True

def getNeighbors(cells, i, j, boundaryCondition):
    neighbors_sum = 0
    for x in range(-1, 2):
        for y in range(-1, 2):
            if x == 0 and y == 0:
                continue

            if boundaryCondition == 1:
                if 0 <= i - x < 35 and 0 <= j - y < 35:
                    neighbors_sum += cells[i - x][j - y].state
            elif boundaryCondition == 2:
                neighbors_sum += cells[(i - x) % 35][(j - y) % 35].state

    return neighbors_sum

def updateCells(cells):
    # list of gray shades
    dead_colors = ["gray50", "gray60", "gray70", "gray80", "gray90", "gray100"]
    
    # create a temp list to store the new updated cells
    temp_state = [[0] * 35 for _ in range(35)]

    for i in range(35):
        for j in range(35):
            neighbors_sum = getNeighbors(cells, i, j, boundaryCondition)

            if cells[i][j].state == 1 and (neighbors_sum == 2 or neighbors_sum == 3):
                # If cell is alive and has 2 or 3 neighbors, remain alive
                temp_state[i][j] = 1
             
            elif cells[i][j].state == 0 and neighbors_sum == 3:
                # If cell is dead and has 3 neighbors, switch to alive
                temp_state[i][j] = 1
             
            elif cells[i][j].state == 1 and (neighbors_sum < 2 or neighbors_sum >= 4):
                # If cell is alive and has less than 2 or more than 3 neighbors, die
                temp_state[i][j] = 0
                

    for i in range(35):
        for j in range(35):
            cells[i][j].state = temp_state[i][j]
        
        # Gradually change color based on the state using the gray shades
            if cells[i][j].state == 1:
                cells[i][j].color("gray0")
                cells[i][j].death_count = 0
            else:
                cells[i][j].death_count += 1
                color = min(cells[i][j].death_count, len(dead_colors) - 1)
                cells[i][j].color(dead_colors[color])
                
    print(cells[i][j].death_count)

boundaryCondition = int(input("Choose the Boundary Condition? \nEnter 1 for Constant or 2 for Periodic: "))
print("Press ESC to exit")

wn = turtle.Screen()
wn.setup(width=35 * 20, height=35 * 20)
wn.title("Life Game")
wn.tracer(0)

wn.listen()
wn.onkeypress(esc, "Escape")  # Press ESC to exit

stop = False
cells = initializeTheCells()
drawScreenBorders()
showTheUniverse(cells)

while not stop:
    wn.update()
    updateCells(cells)
    time.sleep(0.1)

