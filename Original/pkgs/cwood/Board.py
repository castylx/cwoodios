#!/home/castylx/miniconda3/envs/py311env/bin/python
from fpdf import FPDF
import sys, math
from fractions import Fraction
from cwood import CFrac

class Board:
    # Assumed that the width and height are integers
    def __init__(self, width, height, label=None):
        self.width     = width
        self.height    = height
        self.thickness = None
        self.factor    = Fraction("3")
        self.label     = label

    def set_width(self, width):
        self.width = Fraction(width)
    
    def set_logger(self, logger):
        self.logger = logger
    
    def get_logger(self):
        return self.logger

    def set_height(self, height):
        self.height = Fraction(height)

    def set_thickness(self, thickness):
        self.thickness = Fraction(thickness)

    def get_width(self):
        return self.width
        
    def get_height(self):
        return self.height

    def get_thickness(self):
        return self.thickness

    # Returns the board dimensions as a dictionary
    def get_dimensions(self):
        dimensions = {}
        dimensions['w'] = CFrac(self.width).__str__()
        dimensions['h'] = CFrac(self.height).__str__()
    
        return dimensions
    
    # Factor is always 4 since we assume 200 points per page/width
    # Assumed that xpos and ypos are integers
    def drawpdf(self, pdf, xpos, ypos, xpad=0, ypad=0, label=''):
        l = self.get_logger()
    
        # Take factor into account
        neww = self.width * self.factor
        newh = self.height * self.factor

        l.debug("board height is {}".format(CFrac(self.height)))
        l.debug("board width is {}".format(CFrac(self.width)))
        l.debug("factor is {}".format(CFrac(self.factor))) 

        l.debug("new board width ceiling is {}".format(math.ceil(neww)) )
        l.debug("new board height ceiling is {}".format(math.ceil(newh)) )
        
        # Take factor into account
        neww = self.width * self.factor
        newh = self.height * self.factor

        # Print the board out
        pdf.rect(x=xpos, y=ypos, w=math.ceil(neww) + xpad, h=math.ceil(newh) + ypad )

        # Print the label on the board
        xlabel = xpos 
        ylabel = ypos + ((math.ceil(newh) + ypad) / 2)

        pdf.set_xy(xlabel, ylabel)
        pdf.cell(math.ceil(neww), 0, label, align = 'C')

        l.debug("DRAWING TEXT : " + CFrac(self.width).__str__() + "x" + CFrac(self.height).__str__())
        l.debug("original xpos is {}".format(xpos))
        l.debug("original ypos is {}".format(ypos))

        # Current cursor position
        currentx = xpos + math.ceil(neww)
        currenty = ypos + math.ceil(newh)

        l.debug("xpos for text is {}".format(xpos))
        l.debug("ypos for text is {}".format(currenty + 2))
        l.debug("text width is {}".format(math.ceil(neww)))

        pdf.set_xy(xpos, currenty + 4 + ypad)
        pdf.cell(math.ceil(neww), 0, CFrac(self.width).__str__() + " x " + CFrac(self.height).__str__(), align = 'C')

        # Generate the new y position with padding
        currenty = currenty + ypad

        l.debug("\n")

        # Convert x and y to integer
        return(currentx, currenty)

