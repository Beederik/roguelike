from __future__ import annotations

from typing import TYPE_CHECKING

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov
from input_handlers import EventHandler
if TYPE_CHECKING:
    from entity import Entity
    from game_map import GameMap

class Engine:
    def __init__(self, player: Entity) -> None:
        self.self = self
        self.event_handler: EventHandler = EventHandler(self)
        self.player = player
        self.fov_radius = 8

    def handle_enemy_turns(self):
        for entity in set(self.game_map.actors) - {self.player}:
            if entity.ai:
                entity.ai.perform()


    def update_fov(self):
        """recompute the visible area based on the players point of view"""
        self.game_map.visible = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=self.fov_radius
        )
        self.game_map.explored |= self.game_map.visible

    def render(self, console: Console, context: Context):
        self.game_map.render(console=console)
        context.present(console)
        console.clear()
