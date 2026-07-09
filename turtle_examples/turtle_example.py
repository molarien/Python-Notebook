"""
import turtle

timmy = turtle.Turtle()
print(timmy)

# Pencerenin hemen kapanmaması için bu satırı ekle:
turtle.done()

"""

#------------------------------------------------

from turtle import Turtle, Screen

timmy = Turtle()
my_screen = Screen()

timmy.shape("turtle") # imlecin şeklini kaplumbağa yaptı
timmy.color("coral")


print(timmy)
print(my_screen.canvheight)


# ekrana tıkladığında kapanması için
# my_screen.exitonclick()

# Pencerenin açık kalmasını sağlayan fonksiyonu koyuyoruz
my_screen.mainloop()





