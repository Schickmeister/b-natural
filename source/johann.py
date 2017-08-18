#!/usr/bin/env python3

import os
import sys
import Interpreter
import Parser

class Johann:
    def __init__(self, filename):
        self.parser = Parser.Parser()
        self.program = self.parser.parse(filename)

        self.interpreter = Interpreter.Interpreter(self.program)
        self.interpreter.run()

        #self.report()

    def report(self):
        print("Stack: " + str(self.interpreter.stack))
        print("Variables: " + str(self.interpreter.variables))
        print("Labels: " + str(self.interpreter.labels))
        print("Done")

if __name__ == "__main__":
    def main():
        if len(sys.argv) != 2:
            print("Usage: johann <path to file>")
            return
        J = Johann(sys.argv[1])
    main()