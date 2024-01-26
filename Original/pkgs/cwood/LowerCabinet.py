from enum import Enum
from cwood import Door
from cwood import FaceFrame
from fractions import Fraction

class CabinetType(Enum):
    LOWER = 1
    UPPER = 2

# Can be upper cabinet or lower cabinet
class LowerCabinet:
    def __init__(self, lower=CabinetType.LOWER, width=0, height=0):
        self.lower = lower
        self.door  = None
        self.face  = FaceFrame(width, height)
        self.height = Frac("0")
        self.width  = Frac("0")

    # Generate the door dimensions
    # Need the opening width, opening height,
    #   overhang, and width of edges
    def gendoor(self):
        (owidth, oheight) = self.face.get_door_opening()

        overhang  = Fraction(".5")
        rswidth  = Fraction("2.5")

        self.door = Door("cabinet door")
        self.door.set_opening(owidth, oheight)
        self.door.set_rswidth(rswidth)
        self.door.set_ohang(Fraction("0.5"))

        self.door.set_opening(w,h)

    def update():
        pass
    
    def genpdf(self, pdf, currentx, currenty):
        pass

    def print(self):
        pass