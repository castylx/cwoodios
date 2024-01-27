// The Swift Programming Language
// https://docs.swift.org/swift-book

import RationalModule
import Foundation

var isDebugMode = false

func debugPrint(_ items: Any...) {
    guard isDebugMode else { return }
    print(items)
}

/*
    ####################################################################
    # Asks the question from user and returns a Fraction representation
    #####################################################################
*/
func getf(prompt: String, fallback: String? = nil) -> Fraction? {
    var selection: Fraction? = nil

    while selection == nil {
        var input: String? = nil
        if let fallback = fallback {
            print("\(prompt)(default: \(fallback)) > ", terminator: "")
            input = readLine()
            if input?.isEmpty ?? true {
                input = fallback
            }
        } else {
            print(String(prompt + " >"), terminator: "")
            input = readLine()
        }

        if let input = input {
            selection = Fraction(input)
        }

        if selection == nil {
            print("Unable to process number, please enter again")
        }
    }

    return selection
}

func doubleDoor() -> Cut? {
    print("Double Door Selected")
    print("Double Doors Description > ", terminator: "")
    guard let title = readLine() else { return nil }
    guard let width = getf(prompt: "Opening Width") else { return nil }
    guard let height = getf(prompt: "Opening Height") else { return nil }
    guard let overhang = getf(prompt: "Overhang", fallback: "1/2") else { return nil }
    guard let rswidth = getf(prompt: "Rails/Stiles Width ", fallback: "2 1/2") else { return nil}

    // Create Door
    let doors = Door(doorType:.Double, called:title, owidth:width, x:height, with:overhang, and:rswidth)

    print("=====================  Double Door Cutlist ====================")
    print("     Assuming whitehead router bits w/ 3/8 inch channel      \n")
    print("title : \(title)")
    print("width : \(width)")
    print("height: \(height)")
    print("overhang: \(overhang)")
    print("rswidth: \(rswidth)")
    print("\(doors)")
    print("=============================================================")

    return doors
}

var cutlist: [Cut] = []

while true {
    print("Please select an option below :")
    print("\t (1) Single Door")
    print("\t (2) Double Door")
    print("\t (3) Drawer")
    print("\t (4) Upper Cabinet")
    print("\t (5) Lower Cabinet")
    print("\t (6) Generate PDF")
    print("\t (7) Exit")
    print("")
    guard let selection = readLine() else { continue }

    switch selection {
    case "1":
        print("Single Door Selected")
        // let door = singleDoor()
        // cutlist.append(door)
    case "2":
        if let doors = doubleDoor() {
            cutlist.append(doors)
        } else {
            print("Failed to create double door")
        }
    case "3":
        print("Drawer Selected")
        // let drawer = drawer()
        // cutlist.append(drawer)
    case "4":
        print("Upper Cabinet Selected")
        // let cabinet = upperCabinet()
        // cutlist.append(contentsOf: cabinet)
    case "5":
        print("Lower Cabinet Selected")
        // let cabinet = lowerCabinet()
        // cutlist.append(contentsOf: cabinet)
    case "6":
        if cutlist.isEmpty {
            print("Unable to generate cutlist, nothing has been generated thus far")
        } else {
            print("Generating pdf for all projects")
            print("Enter Project Name > ", terminator: "")
            guard let project = readLine() else { continue }

            print("Enter Filename > ", terminator: "")
            guard let filename = readLine() else { continue }

            let plan = Plans(projectName: project, filename: filename, cutlist: cutlist)
            plan.generate()
            PDF.createFlyer()
            print("Done generating pdf for project \(project)")
        }
    case "7", "exit":
        exit(0)
    default:
        print("Selection \(selection) does not exist")
    }
}
