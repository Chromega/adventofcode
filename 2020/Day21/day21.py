class Recipe:
    def __init__(self):
        self.ingredients = set()
        self.allergens = set()
        
recipes = set()
allIngredients = set()
allAllergens = set()
with open("input.txt") as FILE:
    for line in FILE:
        line = line.strip()
        if len(line) == 0:
            continue
        leftParenIdx = line.find("(")
        r = Recipe()
        r.ingredients = set(line[:leftParenIdx-1].split(' '))
        r.allergens = set([x.strip() for x in line[leftParenIdx+10:-1].split(',')])
        allIngredients = allIngredients.union(r.ingredients)
        allAllergens = allAllergens.union(r.allergens)
        recipes.add(r)
        
#part a
possibleIngredientsForAllergen = {}
for allergen in allAllergens:
    possibleIngredients = set(allIngredients)
    for r in recipes:
        if allergen in r.allergens:
            possibleIngredients = possibleIngredients.intersection(r.ingredients)
    possibleIngredientsForAllergen[allergen] = possibleIngredients
    
safeIngredients = set()
for ingredient in allIngredients:
    safe = True
    for allergen in possibleIngredientsForAllergen:
        if ingredient in possibleIngredientsForAllergen[allergen]:
            safe = False
            break
    if safe:
        safeIngredients.add(ingredient)

count = 0
for ingredient in safeIngredients:
    for r in recipes:
        if ingredient in r.ingredients:
            count += 1
print(count)

#part b
knownIngredientForAllergen = {}
while len(knownIngredientForAllergen)<len(possibleIngredientsForAllergen):
    for allergen, possibleIngredients in possibleIngredientsForAllergen.items():
        if allergen in knownIngredientForAllergen:
            continue
        if len(possibleIngredients) == 1:
            ingredient = min(possibleIngredients)
            knownIngredientForAllergen[allergen] = ingredient
            for otherAllergen, otherPossibleIngredients in possibleIngredientsForAllergen.items():
                if otherAllergen == allergen:
                    continue
                otherPossibleIngredients.discard(ingredient)
#comma delimited list of ingredient values sorted by allergen key                
print(','.join([knownIngredientForAllergen[x] for x in sorted(list(knownIngredientForAllergen))]))