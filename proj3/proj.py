import sys
import pulp as p

# Lê todas as linhas da entrada padrão dsddssfffffff
lines = sys.stdin.readlines()

if not lines:
    print("No input read from stdin.")
    sys.exit(1)

# Processa os dados
# A primeira linha contém o número de fábricas, países e crianças
n, m, t = map(int, lines[0].strip().split())

# Informações sobre fábricas
factories = {
    int(line.split()[0]): {"country": int(line.split()[1]), "max_stock": int(line.split()[2])}
    for line in lines[1:n + 1]
    if len(line.split()) >= 3 and int(line.split()[2]) > 0
}

# Informações sobre países
countries = {
    int(line.split()[0]): {"max_exports": int(line.split()[1]), "min_toys": int(line.split()[2])}
    for line in lines[n + 1:n + 1 + m]
    if len(line.split()) >= 3
}

# Informações sobre pedidos das crianças
children = [
    {"id": int(data[0]), "country": int(data[1]),
     "factories": list(map(int, data[2:]))}
    for data in (line.strip().split() for line in lines[n + 1 + m:])
    if len(data) >= 2
]

# Precompute and cache the country of each factory
factory_country = {factory_id: factory_data["country"]
                   for factory_id, factory_data in factories.items()}

# Precompute and cache the country of each child
child_country = {child["id"]: child["country"] for child in children}

# Variáveis de decisão: Satisfação de pedidos das crianças
child_vars = p.LpVariable.dicts(
    "ChildSatisfied",
    [child["id"] for child in children],
    cat="Binary",
)

factory_to_child_vars = p.LpVariable.dicts(
    "FactoryToChild",
    [
        (factory_id, child["id"])
        for child in children
        for factory_id in child["factories"]
    ],
    0,
    None,
    cat="Binary",
)

# Criação do problema de maximização
prob = p.LpProblem("SantaToyDistribution", p.LpMaximize)

# Objetivo: Maximizar o número de crianças satisfeitas
prob += p.lpSum([child_vars[child["id"]]
                for child in children]), "MaximizeSatisfiedChildren"

# Restrições de cada criança: Receber brinquedos apenas de fábricas permitidas
for child in children:
    child_id = child["id"]
    prob += (
        p.lpSum([factory_to_child_vars[(factory_id, child_id)]
                for factory_id in child["factories"]])
        == child_vars[child_id],  # Links satisfaction to toy delivery
        f"ChildSatisfactionAndRequest_{child_id}",
    )

n = len(factories)
# Loop for factory capacity constraints
for i in range(1, n + 1):
    # Restrições de capacidade das fábricas
    factory_id = list(factories.keys())[i - 1]
    factory_data = factories[factory_id]
    prob += (
        p.lpSum(
            [
                factory_to_child_vars[(factory_id, child_id)]
                for (factory_id_pair, child_id) in factory_to_child_vars
                if factory_id_pair == factory_id
            ]
        )
        <= factory_data["max_stock"],
        f"FactoryCapacity_{factory_id}",
    )

# Loop for export constraints by country
for i in range(1, m + 1):
    # Restrições de exportação máxima por país
    country_id = i
    prob += (
        p.lpSum(
            [
                factory_to_child_vars[(factory_id, child_id)]
                for factory_id, child_id in factory_to_child_vars
                if factory_country[factory_id] == country_id and factory_country[factory_id] != child_country[child_id]
            ]
        )
        <= countries[country_id]["max_exports"],
        f"MaxExport_{country_id}",
    )
    # Restrições de exportação mínima por país
    prob += (
        p.lpSum(
            [
                factory_to_child_vars[(factory_id, child_id)]
                for factory_id, child_id in factory_to_child_vars
                if child_country[child_id] == country_id
            ]
        )
        >= countries[country_id]["min_toys"],
        f"MinToysInCirculation_{country_id}",
    )

# Save the problem formulation to a file
# prob.writeLP("SantaToyDistribution.lp")

# Solve the problem using GLPK
glpk_solver = p.GLPK(msg=False)
prob.solve(glpk_solver)

# Calculate the number of satisfied children
ans = sum(1 for child in children if child_vars[child["id"]].varValue == 1)

# Print the result
if ans == 0:
    print(-1)
else:
    print(ans)
