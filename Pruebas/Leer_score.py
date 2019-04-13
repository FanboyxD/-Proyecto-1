import json

with open('scores_prueba.json') as file:
    scores = json.load(file)
print(scores["score1"])
print(scores["score2"])
print(scores["score3"])
print(scores["score4"])
print(scores["score5"])
