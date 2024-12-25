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
    prob += (
        lpSum([factory_to_child_vars[(factory_id, child_id)] for factory_id in child["factories"]])
        <= 1 * child_vars[child_id],
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
                if factory_id in child["factories"]
            ]
        )
        <= countries[country_id]["max_exports"],
        f"MaxExport_{country_id}",
    )
    prob += (
        lpSum(
            [
                child_vars[child["id"]]
                for child in children
                if child["country"] == country_id
            ]
        )
        >= countries[country_id]["min_toys"],
        f"MinToys_{country_id}",
    )

# Solve the problem using GLPK
glpk_solver = GLPK(msg=True)
prob.solve(glpk_solver)

# Print the results
for child in children:
    child_id = child["id"]
    print(f"Child {child_id} satisfied: {child_vars[child_id].varValue}")
