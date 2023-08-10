from __future__ import annotations
from typing import TYPE_CHECKING
import color
if TYPE_CHECKING:
    from tcod.console import Console


def render_health_bar(
        console: Console,
        current_health: int, 
        maximum_health: int
):
    x = 0
    y = 46
    total_width = 20

    calculated_width = int(float(current_health/maximum_health * total_width))
    print(calculated_width)
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