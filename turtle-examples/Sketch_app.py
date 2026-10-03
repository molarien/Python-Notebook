from turtle import Turtle, Screen

tim = Turtle()
screen = Screen()




def up():
    tim.forward(10)

def down():
    tim.backward(10)

def right():
    tim.setheading(tim.heading() - 10)  

def left():
    tim.setheading(tim.heading() + 10)  

def clear():
    tim.clear()
    tim.penup()
    tim.home()
    tim.pendown()


screen.listen()

screen.onkey(key = "w", fun = up)
screen.onkey(key = "s", fun = down)
screen.onkey(key = "d", fun = right)
screen.onkey(key = "a", fun = left)
screen.onkey(key = "space", fun = clear)

screen.exitonclick()