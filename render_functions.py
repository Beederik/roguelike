from __future__ import annotations
from typing import TYPE_CHECKING
import color
if TYPE_CHECKING:
    from tcod.console import Console
    from engine import  Engine
    from game_map import GameMap


def get_names_at_location(x, y, game_map):
    if not game_map.in_bounds(x, y) or not game_map.visible[x, y]:
        return ""
    
    names = ", ".join(entity.name for entity in game_map.entities if entity.x == x and entity.y == y)
    return names.capitalize()

def render_names_at_mouse_location(console: Console, x: int, y: int, engine: Engine):
    mouse_x, mouse_y = engine.mouse_location
    names_at_location = get_names_at_location(mouse_x, mouse_y, engine.game_map)
    console.print(x, y, names_at_location)

def render_health_bar(
        console: Console,
        current_health: int, 
        maximum_health: int
):
    x = 0
    y = 46
    total_width = 20

    calculated_width = int(float(current_health/maximum_health * total_width))
    console.draw_rect(x=x,
                      y=y, 
                      width=total_width, 
                      height=1, 
                      ch=1, 
                      bg=color.bar_empty
    )

    if calculated_width > 0:
        console.draw_rect(x=x,
                      y=y, 
                      width=calculated_width, 
                      height=1, 
                      ch=1, 
                      bg=color.bar_filled
        )

    console.print(x=x+1, y=y, string=f"HP: {current_health}/{maximum_health}", fg=color.bar_text)