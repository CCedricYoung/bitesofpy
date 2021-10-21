from random import random
from time import sleep


def cached_property(func):
    """decorator used to cache expensive object attribute lookup"""
    key = f"_cached_{func.__name__}"

    @property
    def lookup(self):
        if hasattr(self, key):
            return getattr(self, key)

        value = func(self)
        setattr(self, key, value)
        return value

    return lookup


class Planet:
    """the nicest little orb this side of Orion's Belt"""

    GRAVITY_CONSTANT = 42
    TEMPORAL_SHIFT = 0.12345
    SOLAR_MASS_UNITS = "M\N{SUN}"

    def __init__(self, color):
        self.color = color
        self._mass = None

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.color)})"

    @cached_property
    def mass(self):
        scale_factor = random()
        sleep(self.TEMPORAL_SHIFT)
        self._mass = (
            f"{round(scale_factor * self.GRAVITY_CONSTANT, 4)} "
            f"{self.SOLAR_MASS_UNITS}"
        )
        return self._mass
