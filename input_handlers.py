from typing import Optional
import tcod
import tcod.event
from actions import Action, EscapeAction, BumpAction

class EventHandler(tcod.event.EventDispatch[Action]):
    def ev_quit(self, event: tcod.event.Quit) -> Action | None:
        raise SystemExit()
    
    def ev_keydown(self, event: tcod.event.KeyDown) -> Action | None:
        action: Optional[Action] = None

        key = event.sym

        if key == tcod.event.KeySym.UP:
            action = BumpAction(dx = 0, dy = -1)
        elif key == tcod.event.KeySym.DOWN:
            action = BumpAction(dx = 0, dy = 1)
        elif key == tcod.event.KeySym.RIGHT:
            action = BumpAction(dx = 1, dy = 0)
        elif key == tcod.event.KeySym.LEFT:
            action = BumpAction(dx = -1, dy = 0)

        elif key == tcod.event.KeySym.ESCAPE:
            action = EscapeAction()

        return action
        