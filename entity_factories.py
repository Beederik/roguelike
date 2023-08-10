from entity import Actor
from components.ai import HostileEnemy
from components.fighter import Fighter

player = Actor(char="@", 
                color=(255, 255, 255), 
                name="Player", 
                ai_class=HostileEnemy,
                fighter=Fighter(hp=150, defense=2, power=15))

orc = Actor(char="o", 
             color=(63, 127, 63), 
             name="Orc", 
             ai_class=HostileEnemy, 
             fighter=Fighter(hp=30, defense=0, power=4))

troll = Actor(char="T", 
               color=(0, 127, 0), 
               name="Troll", 
               ai_class=HostileEnemy, 
               fighter=Fighter(hp=50, defense=3, power=7))

