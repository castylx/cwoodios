// The Swift Programming Language
// https://docs.swift.org/swift-book

import RationalModule

let half = Rational<Int>(1,2)
let value = Rational<Int>(8)

var compl = half * value

print("Value of 8 * 1/2 is \(compl)")
