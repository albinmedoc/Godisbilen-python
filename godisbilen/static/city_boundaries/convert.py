import json
import os

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

filename = "staffanstorp"

temp = []
with open(os.path.join(__location__, filename + ".json"), "r") as json_file:
    data = json.load(json_file)
    for coord in data:
        temp2 = {}
        temp2["lat"] = coord[1]
        temp2["lng"] = coord[0]
        temp.append(temp2)

with open(os.path.join(__location__, filename + ".json"), "w") as out_file:
    json.dump(temp, out_file, indent=4)

print("File has been converted")
