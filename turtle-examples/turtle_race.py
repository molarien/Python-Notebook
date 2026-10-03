from turtle import Turtle, Screen
import random

tim = Turtle()
screen = Screen()

screen.setup(width= 500,height= 400)

is_race_on = False
user_bet = screen.textinput(title=  "Make your bet", prompt= "Which turtle will win?")
colors = ["red", "orange", "yellow", "green", "blue"]
y_pos = [-70, -40, -10, 20, 50]
all_turtles = []

for i in range(0,5):
    new_turtle = Turtle(shape="turtle")
    new_turtle.color(colors[i])
    new_turtle.penup()
    new_turtle.goto(-230, y_pos[i])
    all_turtles.append(new_turtle)


if user_bet:
    is_race_on = True


while is_race_on:

    for turtle in all_turtles:

        if turtle.xcor() > 230:
            is_race_on = False
            winning_color = turtle.pencolor()
            if winning_color == user_bet:
                print("You have won")
            else:
                print("You have lost")

        random_distance = random.randint(0,10)
        turtle.forward(random_distance)


screen.exitonclick()