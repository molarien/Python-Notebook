import pandas

data = pandas.read_csv("2018_Central_Park_Squirrel_Census_-_Squirrel_Data_20261006.csv")

grey_squireels_count = len(data[data["Primary Fur Color"] == "Gray"])
red_squireels_count = len(data[data["Primary Fur Color"] == "Cinnamon"])
black_squireels_count = len(data[data["Primary Fur Color"] == "Black"])


data_dict = {
    "Fur Color" : ["Gray", "Cinnamon", "Black"],
    "Count" : [grey_squireels_count, red_squireels_count, black_squireels_count]
}


df = pandas.DataFrame(data_dict)
df.to_csv("squirrel_count.csv")

