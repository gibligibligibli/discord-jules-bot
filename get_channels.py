import json
with open("operations/execution/sessao-8-organize_resultado.json") as f:
    data = json.load(f)
for entry in data:
    if "Resultado: " in entry["details"]:
        print(entry["details"])
