#!/home/castylx/miniconda3/envs/py311env/bin/python
from fpdf import FPDF
import sys
from cwood import CFrac
from cwood import Board
from fractions import Fraction

class Door:
    def __init__(self, title, isdouble=False):
        self.title = title
        self.label = ''
        self.rail  = None
        self.stile = None
        self.panel = None
        self.isdouble = isdouble

        self.ohang   = Fraction("1")
        self.owidth  = Fraction("1")
        self.oheight = Fraction("1")
        self.rsthick = Fraction("1")

    def set_logger(self, logger):
        self.logger = logger

    def get_logger(self):
        return self.logger

    def set_ohang(self, t):
        self.ohang = t

        # always update the stiles/rails with new dimensions
        self.update()        

    def set_opening(self, w, h):
        self.owidth  = w
        self.oheight = h

        # always update the stiles/rails with new dimensions
        self.update()        

    def set_rs_width(self, t):
        self.rsthick = t

        # always update the stiles/rails with new dimensions
        self.update()        

    def set_label(self, label):
        self.label = label

    def set_command(self, cmd):
        self.command = cmd

    def update(self):
        if (self.isdouble):
            twidth  = (self.owidth  + (Fraction("2") * self.ohang) - Fraction("1/8")) * Fraction("1/2")
        else:
            twidth  = self.owidth  + (Fraction("2") * self.ohang)

        theight = self.oheight + (Fraction("2") * self.ohang)

        rwidth  = (twidth + Fraction("3/4")) -  (Fraction("2")*self.rsthick)
        pheight = (theight + Fraction(3, 4)) - (Fraction("2")*self.rsthick)

        # Panel width and height
        pwidth  = rwidth - Fraction("1/16")
        pheight = pheight - Fraction("1/16")

        # Create Door
        self.panel = Board(pwidth, pheight)
        self.rail  = Board(rwidth, Fraction("2.5"))
        self.stile = Board(Fraction("2.5"), theight)

        self.panel.set_logger(self.logger)
        self.rail.set_logger(self.logger)
        self.stile.set_logger(self.logger)

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

        # Draw door 1
        # Draw Stile
        l.debug("d1 left stile x:{} y:{}".format(currentx, currenty))
        (stilex, stiley) = self.stile.drawpdf(pdf, currentx, currenty, ypad=(padding*2) + 4, label=self.label + "1")

        # Draw Rails
        l.debug("d1 top rail x:{} y:{}".format(stilex + padding, currenty))
        (currx, curry) = self.rail.drawpdf(pdf, stilex + padding, currenty, label=self.label + "2")
        
        # Draw Panel
        l.debug("d1 panel x:{} y:{}".format(stilex + padding, curry + padding))
        (panelx, panely) = self.panel.drawpdf(pdf, stilex + padding, curry + padding, label=self.label + "3")

        # Draw Stile
        l.debug("d1 right stile x:{} y:{}".format(panelx + padding, currenty))
        self.stile.drawpdf(pdf, panelx + padding, currenty, ypad=(padding*2) + 4, label=self.label + "1")

        # Draw Rails
        l.debug("d1 bottom rail x:{} y:{}".format(stilex + padding, panely+padding))
        (stilex, stiley) = self.rail.drawpdf(pdf, stilex + padding, panely+padding, label=self.label + "2")


        if (self.isdouble):
            clist.append(self.get_dimensions(self.stile, self.label + "1", 4))
            clist.append(self.get_dimensions(self.rail, self.label + "2", 4))
            clist.append(self.get_dimensions(self.panel, self.label + "3", 2))

            # Draw door 2
            # Draw Stile
            currentx = stilex + 40
            l.debug("d2 left stile x:{} y:{}".format(currentx, currenty))
            (stilex, stiley) = self.stile.drawpdf(pdf, currentx, currenty, ypad=(padding*2) + 4, label=self.label + "1")

            # Draw Rails
            l.debug("d2 top rail x:{} y:{}".format(stilex + padding, currenty))
            (currx, curry) = self.rail.drawpdf(pdf, stilex + padding, currenty, label=self.label + "2")
            
            # Draw Panel
            l.debug("d2 panel x:{} y:{}".format(stilex + padding, curry + padding))
            (panelx, panely) = self.panel.drawpdf(pdf, stilex + padding, curry + padding, label=self.label + "3")

            # Draw Stile
            l.debug("d2 right stile x:{} y:{}".format(panelx + padding, currenty))
            self.stile.drawpdf(pdf, panelx + padding, currenty, ypad=(padding*2) + 4, label=self.label + "1")

            # Draw Rails
            l.debug("d2 bottom rail x:{} y:{}".format(stilex + padding, panely+padding))
            (stilex, stiley) = self.rail.drawpdf(pdf, stilex + padding, panely+padding, label=self.label + "2")
        else:
            clist.append(self.get_dimensions(self.stile, self.label + "1", 2))
            clist.append(self.get_dimensions(self.rail, self.label + "2", 2))
            clist.append(self.get_dimensions(self.panel, self.label + "3", 1))

        # Draw the command
        # cell.draw(self.command.....)
        return clist  

    def print(self):
        # Get the total width of door
        if (self.isdouble):
            print ("Double Door - One Door Dimensions: ")
        else:
            print ("Single Door Dimensions: ")

        print (" Panel Width : {}".format( CFrac(self.panel.width) ))
        print (" Panel Height : {}\n".format( CFrac(self.panel.height) ))
        print (" Rails Width : {}".format( CFrac(self.rail.width) ))
        print (" Stiles Height : {}".format( CFrac(self.stile.height) ))

