from __future__ import annotations
from typing import Tuple, TypeVar, TYPE_CHECKING
import copy
if TYPE_CHECKING:
    from game_map import GameMap

EntityType = TypeVar("EntityType", bound="Entity")

class Entity:
    """
    A generic object to represent something in the game (players, entities, items).
    """
    def __init__(self, 
                 x: int=0, 
                 y: int=0, 
                 char: str="?", 
                 color: Tuple[int, int, int]=(255, 50, 255), 
                 name: str="<unnamed>", 
                 blocks_movement: bool=False
                 ) -> None:
        self.x =x
        self.y = y
        self.self = self
        self.char = char
        self.color = color
        self.name = name
        self.blocks_movement = blocks_movement

    def spawn(self: EntityType, game_map: GameMap, x: int, y: int):
        """
        spawn a copy of this instance at the given location on the game map
        """
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        game_map.entities.add(clone)
        return clone

    def move(self, dx: int, dy: int):
        self.self = self
        self.x += dx
        self.y += dy