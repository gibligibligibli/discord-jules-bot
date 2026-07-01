import json
with open("operations/execution/sessao-8-organize_resultado.json") as f:
    data = json.load(f)
for e in data:
    if "📢・anúncios" in e["details"]:
        print(e["details"])
