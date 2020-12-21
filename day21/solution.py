import fileinput
from collections import defaultdict

input_rows = [line.rstrip() for line in fileinput.input('input.txt')]


def parse_ingredients(row):
    ingredients, allergens = row[:-1].split(' (contains ')
    return allergens.split(', '), set(ingredients.split())


ingredients_by_allergen = dict()
ingredient_occurences = defaultdict(int)

for allergens, ingredients in [parse_ingredients(row) for row in input_rows]:
    for allergen in allergens:
        if allergen in ingredients_by_allergen:
            ingredients_by_allergen[allergen] = ingredients.intersection(ingredients_by_allergen[allergen])
        else:
            ingredients_by_allergen[allergen] = ingredients
    for ingredient in ingredients:
        ingredient_occurences[ingredient] += 1

possible_allergen_ingredients = set()

for ingredients in ingredients_by_allergen.values():
    possible_allergen_ingredients.update(ingredients)

all_ingredients = ingredient_occurences.keys()
impossible_allergen_ingredients = all_ingredients - possible_allergen_ingredients

# Part 1

print(sum(ingredient_occurences[ingredient] for ingredient in impossible_allergen_ingredients))

# Part 2

while not all(len(ingredients) == 1 for ingredients in ingredients_by_allergen.values()):
    for allergen1, ingredients1 in ingredients_by_allergen.items():
        if len(ingredients1) == 1:
            for allergen2, ingredients2 in ingredients_by_allergen.items():
                if allergen1 == allergen2:
                    continue
                ingredients_by_allergen[allergen2] = ingredients2 - ingredients1

sorted_allergens = sorted(ingredients_by_allergen.keys())
canonical_dangerous_ingredient_list = [next(iter(ingredients_by_allergen[allergen])) for allergen in sorted_allergens]

print(','.join(canonical_dangerous_ingredient_list))
