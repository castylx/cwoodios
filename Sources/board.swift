import Foundation

struct Board {
    let width : Fraction
    let height : Fraction
    let thickness : Fraction?
    let label : String?
    let factor = Fraction(3, 1)

    init(_ width: Fraction, x height: Fraction, with thickness: Fraction, called label: String? = nil) {
        self.width = width
        self.height = height
        self.thickness = thickness
        self.label = label
    }

    init(_ width: Fraction, x height: Fraction) {
        self.width = width
        self.height = height
        self.thickness = nil
        self.label = nil
    }

    func getDimensions() -> [String: String] {
        var dimensions = [String: String]()
        dimensions["w"] = "\(self.width)"
        dimensions["h"] = "\(self.height)"
        
        return dimensions
    }
}

//     func drawpdf(pdf: PDF, xpos: Int, ypos: Int, xpad: Int = 0, ypad: Int = 0, label: String = "") {
//         guard let logger = self.logger else {
//             return
//         }
    
//         // Take factor into account
//         let neww = self.width * self.factor
//         let newh = self.height * self.factor

//         logger.debug("board height is \(CFrac(self.height))")
//         logger.debug("board width is \(CFrac(self.width))")
//         logger.debug("factor is \(CFrac(self.factor))") 

//         logger.debug("new board width ceiling is \(Int(ceil(neww)))")
//         logger.debug("new board height ceiling is \(Int(ceil(newh)))")
        
//         // Take factor into account
//         let neww = self.width * self.factor
//         let newh = self.height * self.factor

//         // Print the board out
//         pdf.rect(x: xpos, y: ypos, w: Int(ceil(neww)) + xpad, h: Int(ceil(newh)) + ypad)

//         // Print the label on the board
//         let xlabel = xpos 
//         let ylabel = ypos + ((Int(ceil(newh)) + ypad) / 2)

//         pdf.setXY(x: xlabel, y: ylabel)
//         pdf.cell(w: Int(ceil(neww)), h: 0, txt: label, align: .center)

//         logger.debug("DRAWING TEXT : \(CFrac(self.width)) x \(CFrac(self.height))")
//         logger.debug("original xpos is \(xpos)")
//         logger.debug("original ypos is \(ypos)")

//         // Current cursor position
//         let currentx = xpos + Int(ceil(neww))
//         let currenty = ypos + Int(ceil(newh))

//         logger.debug("xpos for text is \(xpos)")
//         logger.debug("ypos for text is \(currenty + 2)")
//         logger.debug("text width is \(Int(ceil(neww)))")

//         pdf.setXY(x: xpos, y: currenty + 4 + ypad)
//         pdf.cell(w: Int(ceil(neww)), h: 0, txt: "\(CFrac(self.width)) x \(CFrac(self.height))", align: .center)

//         // Generate the new y position with padding
//         let currenty = currenty + ypad

//         logger.debug("\n")

//         // Convert x and y to integer
//         return (currentx, currenty)
//     }
// }
