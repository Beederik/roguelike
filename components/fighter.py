from __future__ import annotations
from components.base_component import BaseComponent
from typing import TYPE_CHECKING
from render_order import RenderOrder
from input_handlers import GameOverEventHandler
import color
if TYPE_CHECKING:
    from entity import Actor


class Fighter(BaseComponent):
    entity: Actor
    
    def __init__(self, hp, defense, power) -> None:
        self.max_hp = hp
        self._hp = hp
        self.defense = defense
        self.power = power

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, value: int):
        self._hp = max(0, min(value, self.max_hp))

        if self._hp == 0 and self.entity.ai:
            self.die()

    def die(self) -> None:
        if self.engine.player is self.entity:
            death_msg = "You died!"
            death_msg_color = color.player_die
            self.engine.event_handler = GameOverEventHandler(self.engine)

        else:
            death_msg = f"You killed the {self.entity.name}"
            death_msg_color = color.enemy_die
        self.entity.char = "%"
        self.entity.color = (171, 1, 2)
        self.entity.blocks_movement = False
        self.entity.ai = None
        self.entity.name = f"remains of {self.entity.name}"
        self.entity.render_order = RenderOrder.CORPSE
        self.engine.message_log.add_message(death_msg, death_msg_color)