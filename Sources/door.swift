import Foundation

enum DoorType {
    case Single
    case Double
}

struct Door : CustomStringConvertible {
    let title : String
    let ohang : Fraction
    let owidth : Fraction
    let oheight : Fraction
    let rswidth : Fraction
    // let command: String
    let dtype : DoorType

    // TODO, do not need this yet
    var label: String

    // // Underlying Boards
    var rail: Board?
    var stile: Board?
    var panel: Board?

    var description: String {
        var desc = ""
        // Get the total width of door
        if self.dtype == .Double {
            desc = "Double Door - One Door Dimensions: \n"
        } else {
            desc = "Single Door Dimensions: "
        }

        if let panelWidth = self.panel?.width {
            desc += " Panel Width : \(panelWidth)\n"
        }

        if let panelHeight = self.panel?.height {
            desc += " Panel Height : \(panelHeight)\n"
        }

        if let railWidth = self.rail?.width {
            desc += " Rails Width : \(railWidth)\n"
        }

        if let stileHeight = self.stile?.height {
            desc += " Stiles Height : \(stileHeight)"
        }

        return desc
    }

    // Create Door Structure
    // Door("Title", 3, x 5)
    init(doorType: DoorType, called title: String, owidth: Fraction, x oheight: Fraction, with ohang: Fraction, and thickness: Fraction) {
        self.title = title
        self.owidth = owidth
        self.oheight = oheight
        self.ohang = ohang
        self.dtype = doorType
        self.rswidth = thickness
        self.label = ""

        self.panel = nil
        self.rail = nil
        self.stile = nil

        setRailsStiles()
    }

    mutating func setRailsStiles() {
        let twidth: Fraction

         if self.dtype == DoorType.Double {
            twidth = (self.owidth + (Fraction(2, 1) * self.ohang) - Fraction(1, 8)) * Fraction(1, 2)
         } else {
            twidth = self.owidth + (Fraction(2, 1) * self.ohang)
         }

         let theight = self.oheight + (Fraction(2, 1) * self.ohang)

         let rwidth = (twidth + Fraction(3, 4)) - (Fraction(2, 1) * self.rswidth)
         let pheight = (theight + Fraction(3, 4)) - (Fraction(2, 1) * self.rswidth)

         // Panel width and height
         let pwidth = rwidth - Fraction(1, 16)

        // Create Door
        self.panel = Board(pwidth, x:pheight)
        self.rail = Board(rwidth, x:Fraction(5, 2))
        self.stile = Board(Fraction(5, 2), x:theight)
     }

    func getDimensions(bd: Board, label: String, qty: Int = 1) -> [String: String] {
        var dict = bd.getDimensions()
        dict["l"] = label
        dict["q"] = String(qty)

        return dict
    }

    // func genpdf(pdf: PDF, currentx: Int, currenty: Int) -> [[String: String]] {
    //     guard let l = self.getLogger() else {
    //         return []
    //     }

    //     var clist: [[String: String]] = []
    //     let padding = 7

    //     // Draw door 1
    //     // Draw Stile
    //     debugPrint("d1 left stile x:\(currentx) y:\(currenty)")
    //     guard let (stilex, stiley) = self.stile?.drawpdf(pdf: pdf, currentx: currentx, currenty: currenty, ypad: (padding * 2) + 4, label: self.label + "1") else {
    //         return []
    //     }

    //     // Draw Rails
    //     debugPrint("d1 top rail x:\(stilex + padding) y:\(currenty)")
    //     guard let (currx, curry) = self.rail?.drawpdf(pdf: pdf, currentx: stilex + padding, currenty: currenty, label: self.label + "2") else {
    //         return []
    //     }

    //     // Draw Panel
    //     debugPrint("d1 panel x:\(stilex + padding) y:\(curry + padding)")
    //     guard let (panelx, panely) = self.panel?.drawpdf(pdf: pdf, currentx: stilex + padding, currenty: curry + padding, label: self.label + "3") else {
    //         return []
    //     }

    //     // Draw Stile
    //     debugPrint("d1 right stile x:\(panelx + padding) y:\(currenty)")
    //     self.stile?.drawpdf(pdf: pdf, currentx: panelx + padding, currenty: currenty, ypad: (padding * 2) + 4, label: self.label + "1")

    //     // Draw Rails
    //     debugPrint("d1 bottom rail x:\(stilex + padding) y:\(panely + padding)")
    //     guard let (stilex, stiley) = self.rail?.drawpdf(pdf: pdf, currentx: stilex + padding, currenty: panely + padding, label: self.label + "2") else {
    //         return []
    //     }

    //     if self.isdouble {
    //         clist.append(self.getDimensions(bd: self.stile!, label: self.label + "1", qty: 4))
    //         clist.append(self.getDimensions(bd: self.rail!, label: self.label + "2", qty: 4))
    //         clist.append(self.getDimensions(bd: self.panel!, label: self.label + "3", qty: 2))

    //         // Draw door 2
    //         // Draw Stile
    //         var currentx = stilex + 40
    //         debugPrint("d2 left stile x:\(currentx) y:\(currenty)")
    //         guard let (stilex, stiley) = self.stile?.drawpdf(pdf: pdf, currentx: currentx, currenty: currenty, ypad: (padding * 2) + 4, label: self.label + "1") else {
    //             return []
    //         }

    //         // Draw Rails
    //         debugPrint("d2 top rail x:\(stilex + padding) y:\(currenty)")
    //         guard let (currx, curry) = self.rail?.drawpdf(pdf: pdf, currentx: stilex + padding, currenty: currenty, label: self.label + "2") else {
    //             return []
    //         }

    //         // Draw Panel
    //         debugPrint("d2 panel x:\(stilex + padding) y:\(curry + padding)")
    //         guard let (panelx, panely) = self.panel?.drawpdf(pdf: pdf, currentx: stilex + padding, currenty: curry + padding, label: self.label + "3") else {
    //             return []
    //         }

    //         // Draw Stile
    //         debugPrint("d2 right stile x:\(panelx + padding) y:\(currenty)")
    //         self.stile?.drawpdf(pdf: pdf, currentx: panelx + padding, currenty: currenty, ypad: (padding * 2) + 4, label: self.label + "1")

    //         // Draw Rails
    //         debugPrint("d2 bottom rail x:\(stilex + padding) y:\(panely + padding)")
    //         guard let (stilex, stiley) = self.rail?.drawpdf(pdf: pdf, currentx: stilex + padding, currenty: panely + padding, label: self.label + "2") else {
    //             return []
    //         }
    //     } else {
    //         clist.append(self.getDimensions(bd: self.stile!, label: self.label + "1", qty: 2))
    //         clist.append(self.getDimensions(bd: self.rail!, label: self.label + "2", qty: 2))
    //         clist.append(self.getDimensions(bd: self.panel!, label: self.label + "3", qty: 1))
    //     }

    //     // Draw the command
    //     // cell.draw(self.command.....)
    //     return clist
    // }
}
