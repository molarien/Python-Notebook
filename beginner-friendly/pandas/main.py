import csv

with open("./wheather.csv") as data_file:
    data = csv.reader(data_file)
    temperatures = []

    for row in data:
        if row[1] != "temp":
            temperatures.append(row[1])
        print(row)
    print(temperatures)


print("--------------------------")

# pandas ile kolayı var

import pandas

data = pandas.read_csv("wheather.csv") 
print(data)