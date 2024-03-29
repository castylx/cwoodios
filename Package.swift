// swift-tools-version: 5.9
// The swift-tools-version declares the minimum version of Swift required to build this package.

import PackageDescription

let package = Package(
    name: "CWood",
    dependencies: [
      .package(url: "https://github.com/abdel-17/swift-rational", from: "1.0.0"),
    ],
    targets: [
        // Targets are the basic building blocks of a package, defining a module or a test suite.
        // Targets can depend on other targets in this package and products from dependencies.
        .executableTarget(
            name: "CWood",
	    dependencies: [
		.product(name: "RationalModule", package: "swift-rational")
	   ],
	   path: "Sources"),
    ]
)

