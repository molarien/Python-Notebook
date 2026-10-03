from turtle import Turtle, Screen

tim = Turtle()
screen = Screen()


def move_forwards():
    tim.forward(10) 


screen.listen()
"""
Pencereye "klavyeden gelecek olayları dinlemeye başla" komutunu verir.
"""


screen.onkey(key = "space", fun = move_forwards)
"""
onkey(), bir klavye tuşunu bir fonksiyona bağlar
key = "space": Dinlenecek tuşun Boşluk (Space) tuşu olduğunu belirtir
fun = move_forwards: Space tuşuna basıldığında tetiklenecek fonksiyonu belirtir.
"""

screen.exitonclick()