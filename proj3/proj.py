import sys
from pulp import *

# Lê todas as linhas da entrada padrão
lines = sys.stdin.readlines()

if not lines:
    print("No input read from stdin.")
    sys.exit(1)

# Processa os dados
# A primeira linha contém o número de fábricas, países e crianças
n, m, t = map(int, lines[0].strip().split())

# Informações sobre fábricas
factories = {}
for i in range(1, n + 1):
    factory_id, country_id, max_stock = map(int, lines[i].strip().split())
    factories[factory_id] = {"country": country_id, "max_stock": max_stock}

# Informações sobre países
countries = {}
for i in range(n + 1, n + 1 + m):
    country_id, max_exports, min_toys = map(int, lines[i].strip().split())
    countries[country_id] = {"max_exports": max_exports, "min_toys": min_toys}

# Informações sobre pedidos das crianças
children = []
for i in range(n + 1 + m, len(lines)):
    data = list(map(int, lines[i].strip().split()))
    child_id, country_id, factories_list = data[0], data[1], data[2:]
    children.append({"id": child_id, "country": country_id, "factories": factories_list})

# Variáveis de decisão: Satisfação de pedidos das crianças
child_vars = LpVariable.dicts(
    "ChildSatisfied",
    [child["id"] for child in children],
    cat="Binary",
)

# Variáveis de fluxo: brinquedos enviados de fábricas para crianças
factory_to_child_vars = LpVariable.dicts(
    "FactoryToChild",
    [(factory_id, child["id"]) for factory_id in factories for child in children],
    0,
    None,
    cat="Binary",
)

# Criação do problema de maximização
prob = LpProblem("SantaToyDistribution", LpMaximize)

# Objetivo: Maximizar o número de crianças satisfeitas
prob += lpSum([child_vars[child["id"]] for child in children]), "MaximizeSatisfiedChildren"

# Restrições de cada criança: Receber brinquedos apenas de fábricas permitidas
for child in children:
    child_id = child["id"]
    # Ensure satisfaction is equal to the sum of the factory to child variables
    prob += (
        lpSum([factory_to_child_vars[(factory_id, child_id)] for factory_id in child["factories"]])
        == child_vars[child_id],
        f"ChildSatisfaction_{child_id}",
    )
    # Ensure that the sum is at most 1
    prob += (
        lpSum([factory_to_child_vars[(factory_id, child_id)] for factory_id in child["factories"]])
        <= 1,
        f"ChildRequest_{child_id}",
    )


# Restrições de capacidade das fábricas
for factory_id, factory_data in factories.items():
    prob += (
        lpSum(
            [
                factory_to_child_vars[(factory_id, child["id"])]
                for child in children
                if factory_id in child["factories"]
            ]
        )
        <= factory_data["max_stock"],
        f"FactoryCapacity_{factory_id}",
    )

# Restrições de exportação máxima e mínima por país
for country_id in range(1, m + 1):
    prob += (
        lpSum(
            [
                factory_to_child_vars[(factory_id, child["id"])]
                for factory_id, factory_data in factories.items()
                if factory_data["country"] == country_id
                for child in children
                if factory_id in child["factories"] and 
                factory_data["country"] != child["country"]
            ]
        )
        <= countries[country_id]["max_exports"],
        f"MaxExport_{country_id}",
    )
    prob += (
        lpSum(
            [
                factory_to_child_vars[(factory_id, child["id"])]
                for factory_id, factory_data in factories.items()
                for child in children
                if child["country"] == country_id and factory_id in child["factories"]
            ]
        )
        >= countries[country_id]["min_toys"],
        f"MinToysInCirculation_{country_id}",
    )

# Save the problem formulation to a file
prob.writeLP("SantaToyDistribution.lp")

# Solve the problem using GLPK
glpk_solver = GLPK(msg=False)
prob.solve(glpk_solver)

ans = 0
# Check if any child satisfaction variable needs to be reset to 0
for child in children:
    child_id = child["id"]
    if child_vars[child_id].varValue is None or child_vars[child_id].varValue != 0:
        ans += 1

if ans != 0:
    print(ans)
else:
    print(-1)

