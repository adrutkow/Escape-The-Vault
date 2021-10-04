import json

jsonFile = open("data.json", "r")
data = json.load(jsonFile)
jsonFile.close()

print(data)
for i in range(0, 50):
    data[str(i)] = 0


print(data["3"])

jsonFile = open("data.json", "w+")
jsonFile.write(json.dumps(data))
jsonFile.close()

#jsonFile.write("test")
