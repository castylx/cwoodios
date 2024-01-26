#!/home/castylx/miniconda3/envs/py311env/bin/python
from fpdf import FPDF
import sys
from cwood import CFrac
from cwood import Board
from fractions import Fraction
from enum import Enum

class SlideType(Enum):
    BLUM563H533   = 21
    BLUM563H457   = 18
    BLUM563H381   = 15
    BLUM563H305   = 12
    BLUM563H229   = 9
    UNKNOWN       = 0

class Mount(Enum):
    FACEFRAME   = 0
    PANEL       = 1

#################################################################
# Takes a string and returns a Fraction value
#################################################################
def genf(value):
    lsvals = value.split()

    # Error checking in case we make a mistake when entering a Frac
    if (len(lsvals) > 2):
        print("ERROR ==> Unable to get Frac values from {}".format(value))
    # elif (len(lsvals) == 1) and ()

    # Check to see what we should return
    if (len(lsvals) == 1):
        num = lsvals[0]
        return Fraction(num)
    else:
        digit = int(lsvals[0])
        (numerators, denomitors) = lsvals[1].split("/")
        numerator = int(numerators)
        denomitor = int(denomitors)

        numerator = (denomitor*digit) + numerator
        return Fraction(numerator, denomitor)
    
    return None

class Drawer:

    def __init__(self, title, isdouble=False):
        self.title = title
        self.label = ''

        self.ohang   = Fraction("1")
        self.owidth  = Fraction("1")
        self.oheight = Fraction("1")
        self.odepth  = Fraction("11")
        self.install = Mount.FACEFRAME

        self.width  = Fraction("1")
        self.length = Fraction("1")
        self.wthick = Fraction("1")

        self.bpanel    = None
        self.sidewall  = None
        self.fbwall    = None
        self.frontface = None

    def set_install(self, install):
        self.install = None

        # Update since we changed the installation type
        self.update()

    def set_logger(self, logger):
        self.logger = logger

    def get_logger(self):
        return self.logger

    def set_ohang(self, t):
        self.ohang = t

        # always update the stiles/rails with new dimensions
        self.update()        

    def set_opening(self, w, h, d):
        self.owidth  = w
        self.oheight = h
        self.odepth  = d

        # always update the stiles/rails with new dimensions
        self.update()        

    def set_label(self, label):
        self.label = label

    def set_command(self, cmd):
        self.command = cmd

    def set_slidetype(self, stype):
        self.stype = stype

    def get_slidetype(self):
        return self.stype

    def set_wthickness(self, thickness):
        self.wthick = thickness

    # Dimensions for face installation
    # 599 (23-19/32") 557 (21-15/16") = BLUM563H533
    # 522 (20-9/16") 480 (18-29/32")  = BLUM563H457
    # 446 (17-9/16") 404 (15-29/32")  = BLUM563H381
    # 370 (14-9/16") 328 (12-29/32")  = BLUM563H305
    # 299 (11-25/32") 266 (10-15/32") = BLUM563H229
    # assume 12mm thickness baltic birch 15/32
    def update(self):
        # Figure out which drawer slide to use
        if ( (self.depth > genf("21 15/16")) and ( self.depth < genf("23 19/32")) ):
            self.set_slidetype(SlideType.BLUM563H533)
            self.length = Fraction("21")
        elif ( (self.depth > genf("18 29/32")) and ( self.depth < genf("20 9/16")) ):
            self.set_slidetype(SlideType.BLUM563H457)
            self.length = Fraction("18")
        elif ( (self.depth > genf("15 29/32")) and ( self.depth < genf("17 9/16")) ):
            self.set_slidetype(SlideType.BLUM563H381)
            self.length = Fraction("15")
        elif ( (self.depth > genf("12 29/32")) and ( self.depth < genf("14 9/16")) ):
            self.set_slidetype(SlideType.BLUM563H305)
            self.length = Fraction("12")
        elif ( (self.depth > genf("10 15/32")) and ( self.depth < genf("11 25/32")) ):
            self.set_slidetype(SlideType.BLUM563H229)
            self.length = Fraction("9")
        else:
            self.set_slidetype(SlideType.UKNOWN)
            self.length = Fraction("100")

        # Height of the drawer itself
        self.height = self.oheight - Fraction("25/32")

        # Width of the drawer
        self.width  = self.owdith - genf("1 21/31") + (self.wthick * 2)

        # Create Door
        self.bpanel    = Board(pwidth, pheight)
        self.sidewall  = Board(rwidth, Fraction("2.5"))
        self.fbwall    = Board(Fraction("2.5"), theight)

        self.bpanel.set_logger(self.logger)
        self.sidewall.set_logger(self.logger)
        self.fbwall.set_logger(self.logger)

    def get_dimensions(self, bd, label, qty=1):
        dict = bd.get_dimensions()
        dict['l'] = label
        dict['q'] = str(qty)

        return dict

    # pdf is the pdf object
    # currentx is the current x position of the drawing
    # currenty is the current y position of the drawing
    def genpdf(self, pdf, currentx, currenty):
        l = self.get_logger()
        clist = []
        padding = 7

        # Left Side Wall
        l.debug("d1 left wall  x:{} y:{}".format(currentx, currenty))
        (stilex, stiley) = self.sidewall.drawpdf(pdf, currentx, currenty, ypad=(padding*2) + 4, label=self.label + "1")

        # Back Wall
        l.debug("d1 back wall  x:{} y:{}".format(stilex + padding, currenty))
        (currx, curry) = self.fbwall.drawpdf(pdf, stilex + padding, currenty, label=self.label + "2")
        
        # Draw Back Panel
        l.debug("d1 bottom panel x:{} y:{}".format(stilex + padding, curry + padding))
        (panelx, panely) = self.bpanel.drawpdf(pdf, stilex + padding, curry + padding, label=self.label + "3")

        # Right Side Wall
        l.debug("d1 right wall  x:{} y:{}".format(panelx + padding, currenty))
        self.sidewall.drawpdf(pdf, panelx + padding, currenty, ypad=(padding*2) + 4, label=self.label + "1")

        # Front Wall
        l.debug("d1 front wall  x:{} y:{}".format(stilex + padding, panely+padding))
        (stilex, stiley) = self.fbwall.drawpdf(pdf, stilex + padding, panely+padding, label=self.label + "2")

        clist.append(self.get_dimensions(self.bpanel, self.label + "1", 2))
        clist.append(self.get_dimensions(self.fbwall, self.label + "2", 2))
        clist.append(self.get_dimensions(self.bpanel, self.label + "3", 1))
        clist.append(self.get_dimensions(self.frontface, self.label + "4", 1))

        # Draw the command
        # cell.draw(self.command.....)
        return clist  

    def print(self):
        # Get the total width of door
        print ("Drawer Dimensions: ")

        print (" Front Face Width : {}".format( CFrac(self.frontface.width) ))
        print (" Front Face Height : {}\n".format( CFrac(self.frontface.height) ))
        print (" Panel Width : {}".format( CFrac(self.bpanel.width) ))
        print (" Panel Height : {}\n".format( CFrac(self.bpanel.height) ))
        print (" Side Walls Width : {}".format( CFrac(self.sidewall.width) ))
        print (" Side Walls Height : {}".format( CFrac(self.sidewall.width) ))
        print (" Front & Back Height : {}".format( CFrac(self.fbwall.height) ))
        print (" Front & Back Width : {}".format( CFrac(self.fbwall.height) ))

