import json
with open("operations/execution/sessao-1-infos_resultado.json") as f:
    data = json.load(f)
for log in data:
    if "Resultado:" in log["details"]:
        print(log["details"][:500])
