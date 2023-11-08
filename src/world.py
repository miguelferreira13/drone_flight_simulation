from dataclasses import dataclass


@dataclass
class World:
    min_x : float
    max_x : float
    min_y : float
    max_y : float

    def get_sector_by_coordinates(self, x:float, y:float) -> str:
        if self.min_x <= x < self.max_x/2 and self.min_y <= y < self.max_y/2:
            return "A"
        elif self.max_x/2 <= x <= self.max_x and self.min_y <= y < self.max_y/2:
            return "B"
        elif self.min_x <= x < self.max_x/2 and self.max_y/2 <= y <= self.max_y:
            return "C"
        elif self.max_x/2 <= x <= self.max_x and self.max_y/2 <= y <= self.max_y:
            return "D"
        else:
            return None
