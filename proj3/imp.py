import sys
import pulp as p

# Lê todas as linhas da entrada padrão
lines = sys.stdin.readlines()

if not lines:
    print("No input read from stdin.")
    sys.exit(1)

# Processa os dados
# A primeira linha contém o número de fábricas, países e crianças please work
n, m, t = map(int, lines[0].strip().split())

# Informações sobre fábricas
factories = {
    int(line.split()[0]): {"country": int(line.split()[1]), "max_stock": int(line.split()[2])}
    for line in lines[1:n + 1]
    if len(line.split()) >= 3 and int(line.split()[2]) > 0
}

# Informações sobre países
no_exports = []
countries = {}
for line in lines[n + 1:n + 1 + m]:
    data = line.split()
    if len(data) >= 3:
        country_id = int(data[0])
        max_exports = int(data[1])
        min_toys = int(data[2])
        countries[country_id] = {"max_exports": max_exports, "min_toys": min_toys, "factories": []}
        if max_exports == 0:
            no_exports.append(country_id)

# Precompute and cache the country of each factory
factory_country = {factory_id: factory_data["country"]
                   for factory_id, factory_data in factories.items()}

# Informações sobre pedidos das crianças
children = []
used_factories = set()
for data in (line.strip().split() for line in lines[n + 1 + m:]):
    if len(data) >= 2:
        child_id = int(data[0])
        child_country_id = int(data[1])
        factories_list = list(map(int, data[2:]))
        
        # Filter factories for children from countries in the no_exports list
        if child_country_id in no_exports:
            factories_list = [f for f in factories_list if f in factories and factory_country[f] == child_country_id]
        else:
            factories_list = [f for f in factories_list if f in factories]
        
        if factories_list:
            children.append({"id": child_id, "country": child_country_id, "factories": factories_list})
            used_factories.update(factories_list)

factories = {factory_id: factory_data for factory_id, factory_data in factories.items() if factory_id in used_factories}

# Precompute and cache the country of each child
child_country = {child["id"]: child["country"] for child in children}

# Create problem variables more efficiently
factory_to_child_vars = {}
for child in children:
    for factory_id in child["factories"]:
        factory_to_child_vars[(factory_id, child["id"])] = p.LpVariable(
            f"F{factory_id}C{child['id']}", 
            cat="Binary"
        )

# Criação do problema de maximização
prob = p.LpProblem("SantaToyDistribution", p.LpMaximize)

# Objetivo: Maximizar o número de crianças satisfeitas
prob += p.lpSum(factory_to_child_vars.values())

# Restrições de cada criança: Receber brinquedos apenas de fábricas permitidas
for child in children:
    if len(child["factories"]) > 1:
        prob += p.lpSum(factory_to_child_vars[(f, child["id"])] for f in child["factories"]) <= 1

# Loop for factory capacity constraints
for factory_id, factory_data in factories.items():
    num_factory_to_child_vars = sum(
        1 for (factory_id_pair, child_id) in factory_to_child_vars if factory_id_pair == factory_id
    )
    if num_factory_to_child_vars > factory_data["max_stock"]:
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
for country_id, country_data in countries.items():
    num_factory_to_child_vars = sum(
        1 for (factory_id, child_id) in factory_to_child_vars
        if factory_country[factory_id] == country_id and factory_country[factory_id] != child_country[child_id]
    )
    if num_factory_to_child_vars > country_data["max_exports"]:
    # Restrições de exportação máxima por país
        prob += (
            p.lpSum(
                [
                    factory_to_child_vars[(factory_id, child_id)]
                    for factory_id, child_id in factory_to_child_vars
                    if factory_country[factory_id] == country_id and factory_country[factory_id] != child_country[child_id]
                ]
            )
            <= country_data["max_exports"],
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
        >= country_data["min_toys"],
        f"MinToysInCirculation_{country_id}",
    )

# Save the problem formulation to a file
#prob.writeLP("SantaToyDistribution.lp")

# Solve the problem using GLPK
solver = p.PULP_CBC_CMD(msg=False)
status = prob.solve(solver)

# Calculate the number of satisfied children
obj_value = p.value(prob.objective)
print(-1 if obj_value is None or status != p.LpStatusOptimal else int(obj_value))
