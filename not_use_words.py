import json


arr = []

with open('cenz.txt', 'r', encoding='UTF-8') as f:
    for el in f:
        n = el.lower().split('\n')[0]
        arr.append(n)


with open('cenz.json', 'w', encoding='UTF-8') as f:
    json.dump(arr, f)
