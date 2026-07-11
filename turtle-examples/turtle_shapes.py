from turtle_random_directions import Turtle, Screen

turtle = Turtle()


turtle.shape("triangle")
turtle.color("red")



def draw_shape(num_sides):
    angle = 360/num_sides
    for i in range(num_sides):
        turtle.forward(100)
        turtle.right(angle)

for shape_side_n in range(3,11):
    draw_shape(shape_side_n)





screen = Screen()
screen.exitonclick()

