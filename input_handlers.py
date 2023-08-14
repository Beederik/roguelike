from __future__ import annotations
from typing import Any, Optional, TYPE_CHECKING
from enum import Enum
import tcod.event
from actions import Action, EscapeAction, BumpAction, WaitAction
if TYPE_CHECKING:
    from engine import Engine


class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    RIGHT = (1, 0)
    LEFT = (-1, 0)
    UP_LEFT = (-1, -1)
    UP_RIGHT = (1, -1)
    DOWN_RIGHT = (1, 1)
    DOWN_LEFT = (-1, 1)

    def as_tuple(self):
        return self.value

MOVE_KEYS = {
    # Arrow keys.
    tcod.event.KeySym.UP: Direction.UP,
    tcod.event.KeySym.DOWN: Direction.DOWN,
    tcod.event.KeySym.LEFT: Direction.LEFT,
    tcod.event.KeySym.RIGHT: Direction.RIGHT,
    tcod.event.KeySym.HOME: Direction.UP_LEFT,
    tcod.event.KeySym.END: Direction.DOWN_LEFT,
    tcod.event.KeySym.PAGEUP: Direction.UP_RIGHT,
    tcod.event.KeySym.PAGEDOWN: Direction.DOWN_RIGHT,
    # Numpad keys.
    tcod.event.KeySym.KP_1: Direction.DOWN_LEFT,
    tcod.event.KeySym.KP_2: Direction.DOWN,
    tcod.event.KeySym.KP_3: Direction.DOWN_RIGHT,
    tcod.event.KeySym.KP_4: Direction.LEFT,
    tcod.event.KeySym.KP_6: Direction.RIGHT,
    tcod.event.KeySym.KP_7: Direction.UP_LEFT,
    tcod.event.KeySym.KP_8: Direction.UP,
    tcod.event.KeySym.KP_9: Direction.UP_RIGHT,
    # Vi keys.
    tcod.event.KeySym.h: Direction.LEFT,
    tcod.event.KeySym.j: Direction.DOWN,
    tcod.event.KeySym.k: Direction.UP,
    tcod.event.KeySym.l: Direction.RIGHT,
    tcod.event.KeySym.y: Direction.UP_LEFT,
    tcod.event.KeySym.u: Direction.UP_RIGHT,
    tcod.event.KeySym.b: Direction.DOWN_LEFT,
    tcod.event.KeySym.n: Direction.DOWN_RIGHT,
}
WAIT_KEYS = {
    tcod.event.KeySym.PERIOD,
    tcod.event.KeySym.KP_5,
    tcod.event.KeySym.CLEAR,
}

class EventHandler(tcod.event.EventDispatch[Action]):
    def __init__(self, engine: Engine) -> None:
        self.self = self
        self.engine = engine
    
    def handle_events(self, context: tcod.context.Context) -> None:
        for event in tcod.event.wait():
            context.convert_event(event)
            self.dispatch(event)

    def on_render(self, console: tcod.console.Console):
        self.engine.render(console)

    def ev_mousemotion(self, event: tcod.event.MouseMotion) -> None:
        if self.engine.game_map.in_bounds(event.tile.x, event.tile.y):
            self.engine.mouse_location = event.tile.x, event.tile.y

    def ev_quit(self, event: tcod.event.Quit) -> Action | None:
        raise SystemExit()
    
class MainGameEventHandler(EventHandler):
    def handle_events(self, context: tcod.context.Context) -> None:
        for event in tcod.event.wait():
            context.convert_event(event)
            action = self.dispatch(event)

            if action is None:
                continue
            
            action.perform()

            self.engine.handle_enemy_turns()
            self.engine.update_fov()
    
    def ev_keydown(self, event: tcod.event.KeyDown) -> Action | None:
        action: Optional[Action] = None

        key = event.sym
        player = self.engine.player

        if key in MOVE_KEYS:
            dx, dy = MOVE_KEYS[key].as_tuple()
            action = BumpAction(player, dx, dy)

        elif key in WAIT_KEYS:
            action = WaitAction(player)

        elif key == tcod.event.KeySym.ESCAPE:
            action = EscapeAction(self.engine.player)

        return action


class GameOverEventHandler(EventHandler):
    def handle_events(self, context: tcod.context.Context) -> None:
        for event in tcod.event.wait():
            context.convert_event(event)
            action = self.dispatch(event)

            if action is None:
                continue
            
            action.perform()
    
    def ev_keydown(self, event: tcod.event.KeyDown) -> Action | None:
        action: Optional[Action] = None

        key = event.sym
        
        if key == tcod.event.KeySym.ESCAPE:
            action = EscapeAction(self.engine.player)

        return action