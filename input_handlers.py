from __future__ import annotations
from typing import Any, Optional, TYPE_CHECKING
from enum import Enum
from tcod import libtcodpy
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

        elif key == tcod.event.KeySym.v:
            self.engine.event_handler = HistoryViewer(self.engine)

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
    
CURSOR_Y_KEYS = {
    tcod.event.KeySym.UP: 1,
    tcod.event.KeySym.DOWN: -1,
    tcod.event.KeySym.KP_8: 1,
    tcod.event.KeySym.KP_2: -1,
    tcod.event.KeySym.PAGEUP: 10,
    tcod.event.KeySym.PAGEDOWN: -10,
}


class HistoryViewer(EventHandler):
    """Print the history on a larger window which can be navigated."""

    def __init__(self, engine: Engine):
        super().__init__(engine)
        self.log_length = len(engine.message_log.messages)
        self.cursor = self.log_length - 1

    def on_render(self, console: tcod.Console) -> None:
        super().on_render(console)  # Draw the main state as the background.

        log_console = tcod.console.Console(console.width - 6, console.height - 6)

        # Draw a frame with a custom banner title.
        log_console.draw_frame(0, 0, log_console.width, log_console.height)
        log_console.print_box(
            0, 0, log_console.width, 1, "┤Message history├", alignment=libtcodpy.CENTER
        )

        # Render the message log using the cursor parameter.
        self.engine.message_log.render_messages(
            log_console,
            1,
            1,
            log_console.width - 2,
            log_console.height - 2,
            self.engine.message_log.messages[: self.cursor + 1],
        )
        log_console.blit(console, 3, 3)

    def ev_keydown(self, event: tcod.event.KeyDown) -> None:
        # Fancy conditional movement to make it feel right.
        if event.sym in CURSOR_Y_KEYS:
            adjust = CURSOR_Y_KEYS[event.sym]
            if adjust < 0 and self.cursor == 0:
                # Only move from the top to the bottom when you're on the edge.
                self.cursor = self.log_length - 1
            elif adjust > 0 and self.cursor == self.log_length - 1:
                # Same with bottom to top movement.
                self.cursor = 0
            else:
                # Otherwise move while staying clamped to the bounds of the history log.
                self.cursor = max(0, min(self.cursor + adjust, self.log_length - 1))
        elif event.sym == tcod.event.KeySym.HOME:
            self.cursor = 0  # Move directly to the top message.
        elif event.sym == tcod.event.KeySym.END:
            self.cursor = self.log_length - 1  # Move directly to the last message.
        else:  # Any other key moves back to the main game state.
            self.engine.event_handler = MainGameEventHandler(self.engine)
