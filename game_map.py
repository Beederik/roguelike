from __future__ import annotations
from typing import Iterable, Optional, TYPE_CHECKING
import numpy as np
from tcod.console import Console
import tile_types
if TYPE_CHECKING:
    from entity import Entity
    from engine import Engine

class GameMap:
    def __init__(self, engine: Engine, width, height, entities: Iterable[Entity]=()) -> None:
        self.self = self
        self.engine = engine
        self.width = width
        self.height = height
        self.entities = set(entities)

        self.tiles = np.full((width, height), fill_value=tile_types.wall, order="F")
        self.visible = np.full((width, height), fill_value=False, order="F")
        self.explored = np.full((width, height), fill_value=False, order="F")

    def get_blocking_entity_at_location(self, x: int, y: int)->Optional[Entity]:
        for entity in self.entities:
            if not entity.blocks_movement:
                continue
            if entity.x == x and entity.y == y:
                return entity
            
        return None
        
    def in_bounds(self, x, y):
        """returns true if x and y are inside the bounds of the map"""
        return 0 <= x < self.width and 0 <= y < self.height
    
    def render(self, console: Console):
        console.rgb[0:self.width, 0:self.height] = np.select(
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles["light"], self.tiles["dark"]],
            default=tile_types.SHROUD
        )
        for entity in self.entities:
            #only print entities in the fov
            if self.visible[entity.x, entity.y]:
                console.print(entity.x, entity.y, entity.char, fg=entity.color)