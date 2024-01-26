#!/home/castylx/miniconda3/envs/py311env/bin/python
import sys
from fpdf import FPDF, HTMLMixin
from string import ascii_lowercase as alc

class PDF(FPDF, HTMLMixin):

    def footer(self):
        # Go to 1.5 cm from bottom
        self.set_y(-15)
        # Select Arial italic 8
        self.set_font('times', 'I', 8)
        # Print centered page number
        if (self.pname is None):
            self.cell(0, 10, 'Page %s' % self.page_no(), 0, 0, 'C')
        else:
            self.cell(0, 10, 'Page %s' % self.page_no() + " - " +  self.pname, 0, 0, 'C')

    def set_project(self, pname):
        self.pname = pname

class Plans:
    def __init__(self, project_name, filename, cutlist=None):
        self.filename = filename
        self.pdf = PDF()
        self.pdf.set_project(project_name)
        self.cuts = []
        self.project_name = project_name

        if (cutlist != None):
            self.cuts.extend(cutlist)

    def add(self, cut):
        self.cuts.append(cut)

    # Go through all the cuts and genetate the pages of each cutlist
    # Each individual cut will generate the page themselves
    def generate(self):
        cut_table = []
        # print("generating output file {}".format(self.filename))
        firstpage = True

        self.currentx = 10
        self.currenty = 40

        alc_counter = 0
        for cut in self.cuts:
            self.pdf.add_page()

            if (firstpage):
                firstpage = False
                # Add the title of the document
                self.pdf.set_font('times', 'B', 24)
                self.pdf.cell(0, 20, self.project_name, 0, 1, 'C')

            # Set fount down to 12 for rest of the document
            self.pdf.set_font('times', size=12)
            # ctable should be a list of dictionary entries, with :
            # "l" "w", "h", "q"
            cut.set_label(alc[alc_counter].title())
            alc_counter = alc_counter + 1

            # Get an array of board cuts back from genpdf
            ctable = cut.genpdf(self.pdf, self.currentx, self.currenty)

            # Add array to the existing array
            cut_table.extend(ctable)

        # Print out the whole cut list
        self.pdf.add_page()
        # Add the title of the document
        self.pdf.set_font('Helvetica', 'B', 18)
        self.pdf.cell(0, 20, 'Cut List', 0, 1, 'C')

        greyscale = (240, 245, 245)
        with self.pdf.table(cell_fill_color=greyscale, cell_fill_mode="ROWS", text_align=("CENTER", "CENTER", "CENTER", "CENTER")) as table:
            self.pdf.set_font('courier', 'B', size=14)
            row = table.row()
            row.cell("Label")
            row.cell("Width")
            row.cell("Length")
            row.cell("Qty")
    
            for ccell in cut_table:
                self.pdf.set_font('courier', '', size=12)
                row = table.row()
                row.cell(ccell['l'])
                row.cell(ccell['w'])
                row.cell(ccell['h'])
                row.cell(ccell['q'])

        # Assumptions
        
        # Print out the complete cut list with labels that match the pictures
        self.pdf.output(self.filename) 

