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
    def __init__(self, x: int, y: int, char: str, color: Tuple[int, int, int]) -> None:
        self.x =x
        self.y = y
        self.self = self
        self.char = char
        self.color = color

    def move(self, dx: int, dy: int):
        self.self = self
        self.x += dx
        self.y += dy