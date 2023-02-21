import turtle
from functools import partial
import random

shiplength = [2, 3, 4, 5]
shipOffset = [[0, 0], [10, 0], [0, 0], [10, 0]]
shipNames = ["Patrol Boat", "Cruiser", "Destroyer", "Aircraft Carrier"]
shipori = []
set = []
ships = []
positions = []
enemyPositions = []
doublecheck = []

setup = True
turn = True

screen = turtle.Screen()
screen.setup(500, 500)
turtle.speed(0)

#TODO
#make sure no double target squares
#make sure enbemy position cannot spwn outside grid

twrite = turtle.Turtle()


def align(i, x, y):
  global setup
  if setup == True:
    ship = ships[i]
    offset = shipOffset[i]
    if x > 0:
      x = int(x / 20 + .5) * 20 - offset[0]
    else:
      x = int(x / 20 - .5) * 20 + offset[0]

    y = int(y / 20 - .5) * 20 - offset[1]

    ship.goto(x, y)
    inBounds(i, ship, x, y)


def inBounds(i, ship, x, y):
  coef = shiplength[i] / 2 * 20
  if shipori[i] == 'h':
    if -100 <= x - coef and x + coef < 100 and -210 <= y <= -10:
      set[i] = True
      ship.color("green")
    else:
      set[i] = False
      ship.color("red")
  else:
    if -200 <= y - coef and y + coef <= -10 and -100 < x < 100:
      set[i] = True
      ship.color("green")
    else:
      set[i] = False
      ship.color("red")


def turn(i, x, y):
  global setup
  if setup == True:
    ship = ships[i]

    ship.right(90)

    if shiplength[i] % 2 == 0:
      offset = shipOffset[i]
      offset[0] = abs(offset[0] - 10)
      offset[1] = abs(offset[1] - 10)

    if shipori[i] == "h":
      shipori[i] = "v"
    else:
      shipori[i] = "h"

    align(i, x, y)


def goto(i, x, y):
  global setup
  if setup == True:
    ships[i](x, y)


for i in range(len(shiplength)):
  t = turtle.Turtle()
  t.shape("square")
  t.penup()
  t.color("red")
  t.turtlesize(1, shiplength[i], .25)
  t.goto(110 + (i * 10), 75 - (i * 20))

  t.ondrag(partial(goto, i))
  t.onrelease(partial(align, i))
  t.onclick(partial(turn, i), 3)

  shipori.append('h')
  ships.append(t)
  set.append(False)

# randomly generate enemies
for i in range(len(shiplength)):
  decision = random.randint(0, 9)
  # horizontal
  if decision > 4:
    h = random.randint(0, 9 - shiplength[i])
    v = random.randint(0, 9)

    h = h * 20 - 90
    v = 20 + v * 20

    temp = []
    for j in range(shiplength[i]):
      temp.append((h + (j * 20), v))
      # peg("red", h + (j * 20), v)
    enemyPositions.append(temp)

  # vertical
  else:
    h = random.randint(0, 9)
    v = random.randint(0, 9 - shiplength[i])

    h = h * 20 - 90
    v = 20 + v * 20

    temp = []
    for j in range(shiplength[i]):
      temp.append((h, v + (j * 20)))
      # peg("red", h, v + (j * 20))
    enemyPositions.append(temp)

upper = turtle.Turtle()
lower = turtle.Turtle()

upper.speed(0)
lower.speed(0)

upper.penup()
lower.penup()

upper.goto(-100, 10)
lower.goto(-100, -10)

upper.pendown()
lower.pendown()

for i in range(5):
  upper.left(90)
  lower.right(90)

  upper.forward(180)
  lower.forward(180)

  upper.right(90)
  lower.left(90)

  upper.forward(20)
  lower.forward(20)

  upper.right(90)
  lower.left(90)

  upper.forward(180)
  lower.forward(180)

  upper.left(90)
  lower.right(90)

  if i < 4:
    upper.forward(20)
    lower.forward(20)

upper.left(90)
lower.right(90)

for i in range(5):
  upper.left(90)
  lower.right(90)

  upper.forward(180)
  lower.forward(180)

  upper.right(90)
  lower.left(90)

  upper.forward(20)
  lower.forward(20)

  upper.right(90)
  lower.left(90)

  upper.forward(180)
  lower.forward(180)

  upper.left(90)
  lower.right(90)

  if i < 4:
    upper.forward(20)
    lower.forward(20)
    upper.hideturtle()
    lower.hideturtle()


def contain(cord, matrix):
  for i in matrix:
    if cord in i:
      return True
  return False


def check(matrix):
  for i in matrix:
    if len(i) > 0:
      return True
  return False


def battle():
  global twrite
  if False in set:
    twrite.clear()
    twrite.color("black")
    twrite.penup()
    for i in range(len(set)):
      if set[i] == False:
        twrite.goto(ships[i].xcor() - shiplength[i] / 2 * 20 + shiplength[i],
                    ships[i].ycor() - 5)
        twrite.write("OUT OF BOUNDS")
  else:
    global setup
    twrite.clear()
    setup = False
    for i in range(len(ships)):
      ships[i].color("gray")
      if shipori[i] == "h":
        temp = []
        for j in range(shiplength[i]):
          temp.append((ships[i].xcor() - shiplength[i] * 10 + 10 + j * 20,
                       ships[i].ycor()))
        positions.append(temp)
      else:
        temp = []
        for j in range(shiplength[i]):
          temp.append((ships[i].xcor(),
                       ships[i].ycor() - shiplength[i] * 10 + 10 + j * 20))
        positions.append(temp)


# what happens when player clicks on square
def checkship(x, y):
  global setup, doublecheck
  if x > 100 or x < -100 or y < 10 or y > 210 or setup == True or (
      x, y) in doublecheck:
    return

  if x > 0:
    x = int((x / 20) + .5) * 20 - 10
  else:
    x = int((x / 20) - .5) * 20 + 10

  y = int((y / 20) + .5) * 20

  doublecheck.append((x, y))

  if contain((x, y), enemyPositions):
    peg("green", x, y)
    for i in range(len(enemyPositions)):
      try:
        enemyPositions[i].remove((x, y))
        if len(enemyPositions[i]) == 0:
          print("You sunk my " + shipNames[i])
      except:
        print()
  else:
    peg("blue", x, y)

  gameplay()


def peg(p, x, y):
  t = turtle.Turtle()
  t.shape("circle")
  t.penup()
  t.color(p)
  t.goto(x, y)


def gameplay():
  if check(enemyPositions):
    global turn, doublecheck
    turn = False
    h = random.randint(-4, 4) * 20 - 10
    v = random.randint(-9, -1) * 20

    while (h, v) in doublecheck:
      h = random.randint(-4, 4) * 20 - 10
      v = random.randint(-9, -1) * 20

    if contain((h, v), positions):
      peg("red", h, v)
      for i in range(len(positions)):
        try:
          positions[i].remove((h, v))
          if len(positions[i]) == 0:
            print("Your " + shipNames[i] + " was sunk!")
        except:
          print()
    else:
      peg("yellow", h, v)

    if check(positions):
      turn = True
    else:
      print("Sorry, you lost.")
  else:
    print("victory")


turtle.onkey(battle, "space")
turtle.listen()
screen.onclick(checkship)

turtle.done()