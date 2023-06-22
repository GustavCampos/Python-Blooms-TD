from enum import Enum

class MonkeyType(Enum):
    DART_MONKEY = (170, 30, 3, 1, 0.1, 10, 3, False)
    
    def __init__(self, 
                 cost: int, 
                 size: int, 
                 attack_speed: float, #Seconds between each attack
                 damage: int,
                 shoot_range: float,
                 bullet_velocity: int,
                 pierce: int,
                 pass_when_die: bool) -> None:
        
        self.cost = cost
        self.size = size
        self.attack_speed = attack_speed
        self.damage = damage
        self.shoot_range =shoot_range
        self.bullet_velocity = bullet_velocity
        self.pierce = pierce
        self.pass_when_die = pass_when_die