from __future__ import annotations
from components.base_component import BaseComponent
from typing import TYPE_CHECKING
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
            print (f"You died!")

        else:
            print(f"You killed the {self.entity.name}")

        self.entity.char = "%"
        self.entity.color = (171, 1, 2)
        self.entity.blocks_movement = False
        self.entity.ai = None
        self.entity.name = (f"remains of {self.entity.name}")