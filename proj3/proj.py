import sys
import pulp as p
from collections import defaultdict

# Read input more efficiently
lines = sys.stdin.readlines()
if not lines:
    print("No input read from stdin.")
    sys.exit(1)

# Parse first line
num_factories, num_countries, num_children = map(int, lines[0].strip().split())

# Optimize factory parsing
factories = {}
for line in lines[1:num_factories + 1]:
    f_id, country, max_stock = map(int, line.split())
    if max_stock > 0:
        factories[f_id] = {"country": country, "max_stock": max_stock}

# Optimize country parsing
countries = {}
factory_by_country = defaultdict(list)
for line in lines[num_factories + 1:num_factories + 1 + num_countries]:
    country_id, max_exports, min_toys = map(int, line.split())
    countries[country_id] = {"max_exports": max_exports, "min_toys": min_toys}

# Optimize children parsing and preprocessing
children = []
child_factory_map = defaultdict(list)
factory_child_map = defaultdict(list)
child_country_map = {}

for line in lines[num_factories + 1 + num_countries:]:
    data = list(map(int, line.split()))
    child_id, country = data[0], data[1]
    valid_factories = [f for f in data[2:] if f in factories]
    
    if valid_factories:
        children.append({"id": child_id, "country": country, "factories": valid_factories})
        child_country_map[child_id] = country
        for f in valid_factories:
            child_factory_map[child_id].append(f)
            factory_child_map[f].append(child_id)

# Create problem variables more efficiently
factory_to_child_vars = {}
for child in children:
    for factory_id in child["factories"]:
        factory_to_child_vars[(factory_id, child["id"])] = p.LpVariable(
            f"F{factory_id}C{child['id']}", 
            cat="Binary"
        )

# Create problem
prob = p.LpProblem("SantaToyDistribution", p.LpMaximize)

# Objective function
prob += p.lpSum(factory_to_child_vars.values())

# Child constraints - more efficient implementation
for child in children:
    if len(child["factories"]) > 1:
        prob += p.lpSum(factory_to_child_vars[(f, child["id"])] for f in child["factories"]) <= 1

# Factory capacity constraints - more efficient implementation
for factory_id, factory_data in factories.items():
    children_count = len(factory_child_map[factory_id])
    if children_count > factory_data["max_stock"]:
        prob += p.lpSum(
            factory_to_child_vars[(factory_id, child_id)]
            for child_id in factory_child_map[factory_id]
        ) <= factory_data["max_stock"]

# Country constraints - more efficient implementation
for country_id, country_data in countries.items():
    if country_data["max_exports"] > 0:
        export_vars = [
            factory_to_child_vars[(f_id, c_id)]
            for f_id, f_data in factories.items()
            if f_data["country"] == country_id
            for c_id in factory_child_map[f_id]
            if child_country_map[c_id] != country_id
        ]
        if export_vars:
            prob += p.lpSum(export_vars) <= country_data["max_exports"]

    if country_data["min_toys"] > 0:
        country_vars = [
            factory_to_child_vars[key]
            for key in factory_to_child_vars
            if child_country_map[key[1]] == country_id
        ]
        if country_vars:
            prob += p.lpSum(country_vars) >= country_data["min_toys"]

# Solve with CBC
solver = p.PULP_CBC_CMD(msg=False)
prob.solve(solver)

# Safe solution checking
if prob.status != p.LpStatusOptimal:
    print(-1)
else:
    try:
        ans = sum(
            1 for child in children
            if any(factory_to_child_vars[(f, child["id"])].varValue > 0.5 for f in child["factories"])
        )
        print(ans if ans > 0 else -1)
    except:
        print(-1)