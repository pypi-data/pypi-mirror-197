from typing import Union


class Coordinates:
    def __init__(
        self,
        x: Union[int, float, str],
        y: Union[int, float, str],
        z: Union[int, float, str],
        yaw: Union[int, float, str] = None,
        pitch: Union[int, float, str] = None,
    ):

        self.x = x
        self.y = y
        self.z = z
        self.yaw = yaw
        self.pitch = pitch

    def check_carets(self):
        coords = [self.x, self.y, self.z]

        if any(str(coord).startswith("^") for coord in coords):
            if not all(str(coord).startswith("^") for coord in coords):
                raise WrongCaretNotation(
                    "When using caret notation, every coordinates must start with a caret"
                )

    def offset(self, x=0, y=0, z=0, yaw=0, pitch=0) -> "Coordinates":
        """
        Offsets the coordinates by the given tuple and returns a new BlockCoordinates object.
        """
        
        if yaw and pitch and self.yaw and self.pitch:
          return Coordinates(self.x + x, self.y + y, self.z + z, self.yaw + yaw, self.pitch + pitch)
        if pitch and self.pitch:
          return Coordinates(self.x + x, self.y + y, self.z + z, self.pitch + pitch)
        if yaw and self.yaw:
          return Coordinates(self.x + x, self.y + y, self.z + z, self.yaw + yaw)
        
        return Coordinates(self.x + x, self.y + y, self.z + z)
        
    def __str__(self):
        self.check_carets()
        
        if self.yaw and self.pitch:
          return f"{self.x} {self.y} {self.z} {self.yaw} {self.pitch}"
        
        return f"{self.x} {self.y} {self.z}"


class WrongCaretNotation(Exception):
    pass
