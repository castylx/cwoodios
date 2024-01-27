import RationalModule
import Foundation

struct Fraction: CustomStringConvertible {
    var rational: Rational<Int>

    var description: String {
        let whole = rational.numerator / rational.denominator
        let remainder = rational.numerator % rational.denominator

        debugPrint("numerator: \(rational.numerator)")
        debugPrint("denominator: \(rational.denominator)")
        debugPrint("whole: \(whole)")
        debugPrint("remainder: \(remainder)")

        if remainder == 0 {
            return "\(whole)"
        } else if whole == 0 {
            return "\(rational.numerator)/\(rational.denominator)"
        } else {
            return "\(whole) \(rational.remainder)/\(rational.denominator)"
        }
    }

    // Initializer for a fraction
    init(_ rational : Rational<Int>) {
        self.rational = rational
    }

    // Initializer for a fraction
    init(_ numerator: Int, _ denominator: Int) {
        self.rational = Rational(numerator, denominator)
    }

    // Initializer for a whole number
    init(_ wholeNumber: Int) {
        self.rational = Rational(wholeNumber)
    }

    /*
    #################################################################
    # Takes a string and converts it into a Fraction value
    #################################################################
    */
    init?(_ value: String) {
        let lsvals = value.split(separator: " ")

        // Error checking in case we make a mistake when entering a Frac
        if lsvals.count > 2 {
            print("ERROR ==> Unable to get Frac values from \(value)")
            return nil
        }

        // Check to see what we should return
        if lsvals.count == 1 {
            // Check if this is a fraction or a whole number
            let fractions = lsvals[0].split(separator: "/")
        
            if (fractions.count == 2) {
                guard let numerator = Int(fractions[0]),
                    let denominator = Int(fractions[1]) else {
                    return nil
                }

                self.init(numerator, denominator)
            } else {
                guard let numerator = Int(lsvals[0]) else {
                    return nil
                }

                self.init(numerator)
            }

        } else {
            guard let digit = Int(lsvals[0]) else {
                print("ERROR ==> Cannot convert lsvals[0] into an Int")
                return nil
            }

            let fractions = lsvals[1].split(separator: "/").map(String.init)
            guard fractions.count == 2,
                let numerator = Int(fractions[0]),
                let denominator = Int(fractions[1]) else {
                return nil
            }

            // Calculate the complete numerator
            let cnumerator = denominator * digit + numerator
            self.init(cnumerator, denominator)
        }
    }

    static func + (lhs: Fraction, rhs: Fraction) -> Fraction {
        return Fraction( lhs.rational + rhs.rational )
    }

    static func - (lhs: Fraction, rhs: Fraction) -> Fraction {
        return Fraction( lhs.rational - rhs.rational )
    }

    static func * (lhs: Fraction, rhs: Fraction) -> Fraction {
        return Fraction( lhs.rational * rhs.rational )
    }

    static func / (lhs: Fraction, rhs: Fraction) -> Fraction {
        return Fraction( lhs.rational / rhs.rational )
    }
}
