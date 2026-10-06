file = open("my_file.txt")

contents = file.read()

print(contents)

file.close()

#-----------------------------


with open("my_file.txt") as file:
    contents = file.read()
    print(contents)

#-----------------------------

# Default olarak read only modunda.

with open("my_file.txt", mode = "w") as file:
    file.write("write modu")
# mode = "w" ile halihazırda yazılı olan şeyler silinir ve
# yeni yazdığın olur sadece


# append modu ekleme yapar
with open("my_file.txt", mode = "a") as file:
    file.write("\nappend modu")


# Öylre bir dosya yoksa oluşturur
with open("new_file.txt", mode = "w") as file:
    file.write("New text")


