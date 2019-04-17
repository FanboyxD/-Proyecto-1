import json

with open('puntajes.json') as file:
    scores = json.load(file)
print(scores["Nombres"][0])
print(scores["Nombres"][1])
print(scores["Nombres"][2])
print(scores["Nombres"][3])
print(scores["Nombres"][4])
