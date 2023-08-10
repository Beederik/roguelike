from __future__ import annotations

from typing import TYPE_CHECKING

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov
from input_handlers import MainGameEventHandler
from render_functions import render_health_bar
from message_log import MessageLog
if TYPE_CHECKING:
    from entity import Actor
    from game_map import GameMap
    from input_handlers import EventHandler

class Engine:
    def __init__(self, player: Actor) -> None:
        self.self = self
        self.event_handler: EventHandler = MainGameEventHandler(self)
        self.player = player
        self.fov_radius = 8
        self.message_log = MessageLog()

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

        self.message_log.render(console=console, x=21, y=45, width=40, height=5)

        render_health_bar(console=console, current_health=self.player.fighter.hp, maximum_health=self.player.fighter.max_hp)
        
        context.present(console)
        console.clear()
