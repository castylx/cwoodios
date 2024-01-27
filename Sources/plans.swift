
struct Plans {
    var filename: String
    // var pdf: PDF
    var cuts: [Cut]
    var projectName: String
    var currentX: Int
    var currentY: Int

    init(projectName: String, filename: String, cutList: [Cut]?) {
        self.filename = filename
        // self.pdf = PDF()
        self.pdf.setProject(projectName)
        self.cuts = []
        self.projectName = projectName
        self.currentX = 10
        self.currentY = 40

        if let cutList = cutList {
            self.cuts.append(contentsOf: cutList)
        }
    }

    func add(cut: Cut) {
        self.cuts.append(cut)
    }

    func generate() {
        var cutTable: [[String: Any]] = []
        var firstPage = true
        var alcCounter = 0

        for cut in self.cuts {
            self.pdf.addPage()

            if firstPage {
                firstPage = false
                self.pdf.setFont("times", style: "B", size: 24)
                self.pdf.cell(0, 20, self.projectName, 0, 1, "C")
            }

            self.pdf.setFont("times", size: 12)
            cut.setLabel(alc[alcCounter].title())
            alcCounter += 1

            let ctable = cut.genpdf(self.pdf, self.currentX, self.currentY)
            cutTable.append(contentsOf: ctable)
        }

        self.pdf.addPage()
        self.pdf.setFont("Helvetica", style: "B", size: 18)
        self.pdf.cell(0, 20, "Cut List", 0, 1, "C")

        let greyscale = (240, 245, 245)
        // Replace with actual table creation code
        let table = self.pdf.table(cellFillColor: greyscale, cellFillMode: "ROWS", textAlign: ("CENTER", "CENTER", "CENTER", "CENTER"))

        self.pdf.setFont("courier", style: "B", size: 14)
        // Replace with actual row creation code
        var row = table.row()
        row.cell("Label")
        row.cell("Width")
        row.cell("Length")
        row.cell("Qty")

        for ccell in cutTable {
            self.pdf.setFont("courier", style: "", size: 12)
            row = table.row()
            row.cell(ccell["l"] as! String)
            row.cell(ccell["w"] as! String)
            row.cell(ccell["h"] as! String)
            row.cell(ccell["q"] as! String)
        }

        self.pdf.output(self.filename)
    }
}