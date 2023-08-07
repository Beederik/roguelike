from typing import Iterable, Any

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

from actions import EscapeAction, MovementAction
from entity import Entity
from input_handlers import EventHandler
from game_map import GameMap

class Engine:
    def __init__(self, event_handler: EventHandler, player: Entity, game_map: GameMap) -> None:
        self.self = self
        self.event_handler = event_handler
        self.player = player
        self.game_map = game_map
        self.fov_radius = 8
        self.update_fov()

    def handle_events(self, events: Iterable[Any]):
        for event in events:
            action = self.event_handler.dispatch(event)
            if action is None:
                continue

            action.perform(self, self.player)
            self.update_fov()

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
