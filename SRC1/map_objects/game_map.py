# * imports :
import tcod as libtcod
from random import randint
from components.ai import BasicMonster
from components.equipment import EquipmentSlots
from components.equippable import Equippable
from components.fighter import Fighter
from game_messages import Message
from entity import Entity
from render_functions import RenderOrder
from random_utils import from_dungeon_level, random_choice_from_dict
from map_objects.rectangle import Rect
from map_objects.tile import Tile
from components.item import Item
from item_functions import cast_confuse, heal, cast_lightning, cast_fireball
from components.stairs import Stairs
#  }}}

# * GameMap class : 
class GameMap:
# ** __init__ : 
    def __init__(self, width, height, dungeon_level=1): # Folding {{{
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()
        self.dungeon_level = dungeon_level
        #  }}}
        
        
# ** initialize_tiles : 
    def initialize_tiles(self): # Folding {{{
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]
        return tiles

        
# ** create_room : 
    def create_room(self, room): # Folding {{{
        # go through the tiles in the rectangle and make them passable
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

                
# ** create_over_room : 
    def create_over_room(self, room): # Folding {{{
        # go through the tiles in the rectangle and make them passable
        for x in range(room.x1 , room.x2 - 1):
            for y in range(room.y1, room.y2 - 1):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

                
# ** make_test_map : 
    def make_test_map(self): # Folding {{{
        # Create two rooms for demonstration purposes
        room1 = Rect(20, 15, 10, 15)
        room2 = Rect(35, 15, 10, 15)
        self.create_room(room1)
        self.create_room(room2)
        self.create_h_tunnel(25, 40, 23)

        
# ** make_map : 
    def make_map(self,
                 max_rooms, room_min_size, room_max_size,
                 map_width, map_height,
                 player, entities): # Folding {{{
# *** init variabls:
        rooms = []
        num_rooms = 0
        center_of_last_room_x = None
        center_of_last_room_y = None
# *** }}} start of make rooms loop:
        for r in range(max_rooms):#   {{{
# **** generate room coordinates  : 
            # random width and height : 
            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_max_size)
            # random position without going out of the boundaries of the map
            x = randint(0, map_width - w - 1)
            y = randint(0, map_height - h - 1)
            # "Rect" class makes rectangles easier to work with
            new_room = Rect(x, y, w, h)
# **** run through the other rooms and see if they intersect with this one#   {{{:
            for other_room in rooms:
                if new_room.intersect(other_room):
                    break
            else:
                # this means there are no intersections, so this room is valid
# **** # "paint" it to the map's tiles:
                self.create_room(new_room)
                # center coordinates of new room, will be useful later
                (new_x, new_y) = new_room.center()
                center_of_last_room_x = new_x
                center_of_last_room_y = new_y
# **** add player : 
                if num_rooms == 0:# add player  {{{
                    # this is the first room, where the player starts t
                    player.x = new_x
                    player.y = new_y
                    #  }}}
# **** connect with tunnels : 
                else: # connect with tunnels  {{{
                    # all rooms after the first:
                    # connect it to the previous room with a tunnel
                    # center coordinates of previous room
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()
                    # flip a coin (random number that is either 0 or 1)
                    if randint(0, 1) == 1:
                        # first move horizontally, then vertically
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        # first move vertically, then horizontally
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)
                    #  }}}
# **** place_entities : 
                    self.place_entities(new_room, entities)
# **** finally, append the new room to the list : 
                rooms.append(new_room)
# **** }}} end of make rooms loop:
                num_rooms += 1
# *** add stairs  {{{:
        stairs_component = Stairs(self.dungeon_level + 1)
        down_stairs = Entity(center_of_last_room_x, center_of_last_room_y, '>', libtcod.white, 'Stairs',
                             render_order=RenderOrder.STAIRS, stairs=stairs_component)
        entities.append(down_stairs)

    
# ** create_h_tunnel : 
    def create_h_tunnel(self, x1, x2, y): # Folding {{{
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False
            
            
# ** create_v_tunnel : 
    def create_v_tunnel(self, y1, y2, x): # Folding {{{
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

            
# ** place_entities : 
    def place_entities(self, room, entities): 
# *** monster & item list chances : 
# **** monster_chances : 
        max_monsters_per_room = from_dungeon_level([[2, 1], [3, 4], [5, 6]], self.dungeon_level)
        monster_chances = {
            'orc': 80,
            'troll': from_dungeon_level([[15, 3], [30, 5], [60, 7]], self.dungeon_level)
        }
# **** item_chances : 
        max_items_per_room = from_dungeon_level([[1, 1], [2, 4]], self.dungeon_level)
        item_chances = {
            'healing_potion': 35,
            'sword': from_dungeon_level([[5, 4]], self.dungeon_level),
            'shield': from_dungeon_level([[15, 8]], self.dungeon_level),
            'lightning_scroll': from_dungeon_level([[25, 4]], self.dungeon_level),
            'fireball_scroll': from_dungeon_level([[25, 6]], self.dungeon_level),
            'confusion_scroll': from_dungeon_level([[10, 2]], self.dungeon_level)
        }
# *** Add items  {{{:
# **** start of_items loop: 
        number_of_items = randint(0, max_items_per_room)
        for i in range(number_of_items):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)
            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                item_choice = random_choice_from_dict(item_chances)
# **** add Healing Potion  {{{ : 
                if item_choice == 'healing_potion':
                    item_component = Item(use_function=heal, amount=40)
                    item = Entity(x, y, '!', libtcod.violet, 'Healing Potion', render_order=RenderOrder.ITEM,
                                  item=item_component)
# **** sword : 
                elif item_choice == 'sword':
                    equippable_component = Equippable(EquipmentSlots.MAIN_HAND, power_bonus=3)
                    item = Entity(x, y, '/', libtcod.sky, 'Sword', equippable=equippable_component)
# **** shield : 
                elif item_choice == 'shield':
                    equippable_component = Equippable(EquipmentSlots.OFF_HAND, defense_bonus=1)
                    item = Entity(x, y, '[', libtcod.darker_orange, 'Shield', equippable=equippable_component)

# **** add Fireball scroll {{{ : 
                elif item_choice == 'fireball_scroll':
                    item_component = Item(use_function=cast_fireball, targeting=True, targeting_message=Message(
                        'Left-click a target tile for the fireball(d25, r3), or right-click to cancel.', libtcod.light_cyan),
                                          damage=25, radius=3)
                    item = Entity(x, y, '#', libtcod.red, 'Fireball Scroll', render_order=RenderOrder.ITEM,
                                  item=item_component)
# **** Confusion Scroll   : 
                elif item_choice == 'confusion_scroll':
                    item_component = Item(use_function=cast_confuse,
                        targeting=True,
                        targeting_message=Message(
                            'Left-click an enemy to confuse it, or right-click to cancel.',
                            libtcod.light_cyan))
                    item = Entity(x, y, '#',
                                  libtcod.light_pink,
                                  'Confusion Scroll',
                                  render_order=RenderOrder.ITEM,
                                  item=item_component)
# **** add  Lightning Scroll  : 
                else: # add  Lightning Scroll {{{
                    item_component = Item(use_function=cast_lightning, damage=40, maximum_range=5)
                    item = Entity(x, y, '#', libtcod.yellow, 'Lightning Scroll', render_order=RenderOrder.ITEM,
                                  item=item_component)
                entities.append(item)
# *** add Monsters  {{{:
        number_of_monsters = randint(0, max_monsters_per_room)
        for i in range(number_of_monsters):
# **** Choose a random location in the room:
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)
            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                monster_choice = random_choice_from_dict(monster_chances)
# **** make Orc  {{{:
                if monster_choice == 'orc':
                    fighter_component = Fighter(hp=20, defense=0, power=4, xp=35)
                    ai_component = BasicMonster()
                    monster = Entity(
                        x, y,
                        'o', libtcod.desaturated_green, 'Orc',
                        blocks=True, render_order=RenderOrder.ACTOR,  
                        fighter=fighter_component, ai=ai_component)
# **** Make Trole  {{{:
                else:
                    fighter_component = Fighter(hp=30, defense=2, power=8, xp=100 )
                    ai_component = BasicMonster()
                    monster = Entity(
                        x, y,
                        'T', libtcod.darker_green, 'Troll',
                        blocks=True, render_order=RenderOrder.ACTOR, 
                        fighter=fighter_component, ai=ai_component)
                    #  }}}
                entities.append(monster)
                
            
# ** is_blocked : 
    def is_blocked(self, x, y): # Folding {{{
        if self.tiles[x][y].blocked:
            return True
        return False

        
# ** next_floor : 
    def next_floor(self, player, message_log, constants): #   {{{
        self.dungeon_level += 1
        entities = [player]
        self.tiles = self.initialize_tiles()
        self.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'],
                      constants['map_width'], constants['map_height'], player, entities)
        player.fighter.heal(player.fighter.max_hp // 2)
        message_log.add_message(Message('You take a moment to rest, and recover your strength.', libtcod.light_violet))
        return entities
