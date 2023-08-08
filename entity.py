from __future__ import annotations
from typing import Optional, Tuple, TypeVar, TYPE_CHECKING
import copy
if TYPE_CHECKING:
    from game_map import GameMap

EntityType = TypeVar("EntityType", bound="Entity")

class Entity:
    """
    A generic object to represent something in the game (players, entities, items).
    """

    game_map: GameMap

    def __init__(self, 
                 game_map: Optional[GameMap] = None, 
                 x: int=0, 
                 y: int=0, 
                 char: str="?", 
                 color: Tuple[int, int, int]=(255, 50, 255), 
                 name: str="<unnamed>", 
                 blocks_movement: bool=False
                 ) -> None:
        self.x = x
        self.y = y
        self.self = self
        self.char = char
        self.color = color
        self.name = name
        self.blocks_movement = blocks_movement
        if game_map:
            self.game_map = game_map
            game_map.entities.add(self)

    def spawn(self: EntityType, game_map: GameMap, x: int, y: int):
        """
        spawn a copy of this instance at the given location on the game map
        """
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        clone.game_map = game_map
        game_map.entities.add(clone)
        return clone

    def place(self, x: int, y: int, game_map: Optional[GameMap]=None):
        """
        place this entity at a new location. Handles moving across game maps.
        """
        self.x = x
        self.y = y
        if game_map:
            if hasattr(self, "game_map"):
                self.game_map.entities.remove(self)
            self.game_map = game_map

            game_map.entities.add(self)

    def move(self, dx: int, dy: int):
        self.self = self
        self.x += dx
        self.y += dy