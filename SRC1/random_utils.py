from random import randint

# * from_dungeon_level : 
def from_dungeon_level(table, dungeon_level):
    for (value, level) in reversed(table):
        if dungeon_level >= level:
            return value
    return 0

# * random_choice_index : 
def random_choice_index(chances):
    random_chance = randint(1, sum(chances))
    running_sum = 0
    choice = 0
    for w in chances:
        running_sum += w
        if random_chance <= running_sum:
            return choice
        choice += 1

        
# * random_choice_from_dict : 
def random_choice_from_dict(choice_dict):
    choices = list(choice_dict.keys())
    chances = list(choice_dict.values())
    return choices[random_choice_index(chances)]
