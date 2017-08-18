import os
import sys

class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items)-1]

    def size(self):
        return len(self.items)

    def __repr__(self):
        return str(self.items)

class RuntimeError(Exception):
    def __init__(self, msg, position):
        msg = "Runtime Error: " + msg
        sys.exit(msg)

class Interpreter:
    def __init__(self, program):
        self.program = program
        self.pointer = 0
        self.stack = Stack()
        self.callStack = Stack()
        self.variables = dict()
        self.labels = dict()

    def evaluate(self):
        currentCommand = self.program[self.pointer]

        ############################
        ##   Stack Manipulation   ##
        ############################

        if (currentCommand == "push"):
            try:
                self.pointer += 1
                int_to_push = int(self.program[self.pointer])
                self.stack.push(int_to_push)
            except ValueError:
                raise RuntimeError("'push' expected an integer, but got '%s'" %
                                    self.program[self.pointer], self.pointer)
            except:
                raise RuntimeError("Could not retrieve the next element" \
                                   "to be pushed.", self.pointer)

        elif (currentCommand == "dup"):
            try:
                self.stack.push(self.stack.peek())
            except:
                raise RuntimeError("Could not duplicate top item", self.pointer)

        elif (currentCommand == "swap"):
            try:
                e1 = self.stack.pop()
                e2 = self.stack.pop()
                self.stack.push(e1)
                self.stack.push(e2)
            except:
                raise RuntimeError("Could not swap items", self.pointer)

        elif (currentCommand == "rotl"):
            try:
                e1 = self.stack.pop()
                e2 = self.stack.pop()
                e3 = self.stack.pop()
                self.stack.push(e1)
                self.stack.push(e3)
                self.stack.push(e2)
            except:
                raise RuntimeError("Could not rotate items", self.pointer)

        elif (currentCommand == "rotr"):
            try:
                e1 = self.stack.pop()
                e2 = self.stack.pop()
                e3 = self.stack.pop()
                self.stack.push(e2)
                self.stack.push(e1)
                self.stack.push(e3)
            except:
                raise RuntimeError("Could not rotate items", self.pointer)

        elif (currentCommand == "drop"):
            try:
                self.stack.pop()
            except:
                raise RuntimeError("Drop from an empty stack", self.pointer)

        ############################
        ##       Arithmetic       ##
        ############################

                ############################
                ##      Manipulation      ##
                ############################

        elif (currentCommand == "plus"):
            try:
                e1 = self.stack.pop()
                e2 = self.stack.pop()
            except:
                raise RuntimeError("Not enough arguments on stack to add", 
                                    self.pointer)
            try:
                e1 = int(e1)
            except:
                raise RuntimeError("First argument of plus " \
                                   "is not a number", self.pointer)
            try:
                e2 = int(e2)
            except:
                raise RuntimeError("Second argument of plus " \
                                   "is not a number", self.pointer)
            self.stack.push((e2 + e1))

        elif (currentCommand == "minus"):
            try:
                e1 = self.stack.pop()
                e2 = self.stack.pop()
            except:
                raise RuntimeError("Not enough arguments on stack to subtract", 
                                    self.pointer)
            try:
                e1 = int(e1)
            except:
                raise RuntimeError("First argument of minus " \
                                   "is not a number", self.pointer)
            try:
                e2 = int(e2)
            except:
                raise RuntimeError("Second argument of minus " \
                                   "is not a number", self.pointer)
            self.stack.push((e2 - e1))

        elif (currentCommand == "times"):
            try:
                e1 = self.stack.pop()
                e2 = self.stack.pop()
            except:
                raise RuntimeError("Not enough arguments on stack to multiply", 
                                    self.pointer)
            try:
                e1 = int(e1)
            except:
                raise RuntimeError("First argument of times " \
                                   "is not a number", self.pointer)
            try:
                e2 = int(e2)
            except:
                raise RuntimeError("Second argument of times " \
                                   "is not a number", self.pointer)
            self.stack.push((e2 * e1))

        elif (currentCommand == "idiv"):
            try:
                e1 = self.stack.pop()
                e2 = self.stack.pop()
            except:
                raise RuntimeError("Not enough arguments on stack to divide", 
                                    self.pointer)
            try:
                e1 = int(e1)
            except:
                raise RuntimeError("First argument of division " \
                                   "is not a number", self.pointer)
            try:
                e2 = int(e2)
            except:
                raise RuntimeError("Second argument of division " \
                                   "is not a number", self.pointer)
            self.stack.push((e2 // e1))

        elif (currentCommand == "div"):
            try:
                e1 = self.stack.pop()
                e2 = self.stack.pop()
            except:
                raise RuntimeError("Not enough arguments on stack to divide", 
                                    self.pointer)
            try:
                e1 = int(e1)
            except:
                raise RuntimeError("First argument of division " \
                                   "is not a number", self.pointer)
            try:
                e2 = int(e2)
            except:
                raise RuntimeError("Second argument of division " \
                                   "is not a number", self.pointer)
            self.stack.push((e2 / e1))

        elif (currentCommand == "mod"):
            try:
                e1 = self.stack.pop()
                e2 = self.stack.pop()
            except:
                raise RuntimeError("Not enough arguments on stack to mod", 
                                    self.pointer)
            try:
                e1 = int(e1)
            except:
                raise RuntimeError("First argument of mod " \
                                   "is not a number", self.pointer)
            try:
                e2 = int(e2)
            except:
                raise RuntimeError("Second argument of mod " \
                                   "is not a number", self.pointer)
            self.stack.push((e2 % e1))

        elif (currentCommand == "pow"):
            try:
                e1 = self.stack.pop()
                e2 = self.stack.pop()
            except:
                raise RuntimeError("Not enough arguments on stack to "\
                                   "exponentiate", self.pointer)
            try:
                e1 = int(e1)
            except:
                raise RuntimeError("First argument of exponentiation " \
                                   "is not a number", self.pointer)
            try:
                e2 = int(e2)
            except:
                raise RuntimeError("Second argument of exponentiation " \
                                   "is not a number", self.pointer)
            self.stack.push((e2 ** e1))

                ############################
                ##       Comparison       ##
                ############################

        elif (currentCommand == "less" or currentCommand == "greater"
              or currentCommand == "eq" or currentCommand == "neq"
              or currentCommand == "and" or currentCommand == "or"):
            try:
                e1 = self.stack.pop()
                e2 = self.stack.pop()
            except:
                raise RuntimeError("Not enough arguments on stack to "\
                                   "compare", self.pointer)
            try:
                e1 = int(e1)
            except:
                raise RuntimeError("First argument of comparison " \
                                   "is not a number", self.pointer)
            try:
                e2 = int(e2)
            except:
                raise RuntimeError("Second argument of comparison " \
                                   "is not a number", self.pointer)
            
            if (currentCommand == "less"):
                self.stack.push(1) if (e2 < e1) else self.stack.push(0)
            elif (currentCommand == "greater"):
                self.stack.push(1) if (e2 > e1) else self.stack.push(0)
            elif (currentCommand == "eq"):
                self.stack.push(1) if (e2 == e1) else self.stack.push(0)
            elif (currentCommand == "neq"):
                self.stack.push(1) if (e2 != e1) else self.stack.push(0)
            elif (currentCommand == "and"):
                self.stack.push(1) if (e2 and e1) else self.stack.push(0)
            elif (currentCommand == "or"):
                self.stack.push(1) if (e2 or e1) else self.stack.push(0)

        ############################
        ##      Flow Control      ##
        ############################

        elif (currentCommand == "set_lbl"):
            self.pointer += 1

        elif (currentCommand == "jmp_lbl"):
            try:
                label_name = (self.program[self.pointer+1])
                self.pointer = self.labels[label_name]
            except IndexError:
                raise RuntimeError("Reached the end of the program " \
                                   "unexpectedly", self.pointer)
            except KeyError:
                raise RuntimeError("Tried to jump to a label that has not " \
                                   "been set", self.pointer)

        elif (currentCommand == "jmp_lbl_if"):
            try:
                e = self.stack.pop()
            except:
                raise RuntimeError("Could not read from stack for " \
                                   "conditional jump", self.pointer)

            if (e == 0): 
                self.pointer += 1
                return

            try:
                label_name = (self.program[self.pointer+1])
                self.pointer = self.labels[label_name]
            except IndexError:
                raise RuntimeError("Reached the end of the program " \
                                   "unexpectedly", self.pointer)
            except KeyError:
                raise RuntimeError("Tried to jump to a label that has not " \
                                   "been set", self.pointer)

        elif (currentCommand == "call_sub"):
            try:
                label_name = (self.program[self.pointer+1])
                self.callStack.push(self.pointer+1)
                self.pointer = self.labels[label_name]
            except IndexError:
                raise RuntimeError("Reached the end of the program " \
                                   "unexpectedly", self.pointer)
            except KeyError:
                raise RuntimeError("Tried to jump to a label that has not " \
                                   "been set", self.pointer)

        elif (currentCommand == "end_sub"):
            try:
                self.pointer = self.callStack.pop()
            except IndexError:
                raise RuntimeError("Tried to return to caller on an empty "\
                                   "call stack", self.pointer)

        ############################
        ##        Variables       ##
        ############################

        elif (currentCommand == "save_var"):
            try:
                variable_name = (self.program[self.pointer+1])
                self.variables[variable_name] = self.stack.pop()
                self.pointer += 1
            except IndexError:
                raise RuntimeError("Reached the end of the program " \
                                   "unexpectedly", self.pointer)
        elif (currentCommand == "get_var"):
            try:
                variable_name = (self.program[self.pointer+1])
                self.stack.push(self.variables[variable_name])
                self.pointer += 1
            except IndexError:
                raise RuntimeError("Reached the end of the program " \
                                   "unexpectedly", self.pointer)
            except KeyError:
                raise RuntimeError("Tried to access an undefined variable",
                                    self.pointer)

        ############################
        ##           I/O          ##
        ############################

        elif (currentCommand == "read_int"):
            try:
                input_str = input()
                e = int(input_str)
                self.stack.push(e)
            except:
                raise RuntimeError("Expected an integer input, but " \
                                   "receieved '%s'" % input_str, self.pointer)

        elif (currentCommand == "read_char"):
            try:
                input_str = input()
                self.stack.push(ord(e))
            except:
                raise RuntimeError("Unable to read character " \
                                   "input", self.pointer)

        elif (currentCommand == "print_int"):
            try:
                e = self.stack.pop()
                print(e)
            except:
                raise RuntimeError("Could not print integer", self.pointer)

        elif (currentCommand == "print_char"):
            try:
                e = self.stack.pop()
                print(chr(e))
            except:
                raise RuntimeError("Could not print character", self.pointer)

        ############################
        ##          Error         ##
        ############################

        else:
            raise RuntimeError("Invalid token '%s'" % currentCommand, 
                                self.pointer)

    def run(self):
        self.set_labels()

        while (self.program[self.pointer] != "exit"):
            self.evaluate()
            self.pointer += 1

            if (self.pointer == len(self.program)):
                raise RuntimeError("Reached the end of the program " \
                                   "unexpectedly", self.pointer)

    def set_labels(self):
        label_pointer = 0
        while (label_pointer < len(self.program)):
            currentCommand = self.program[label_pointer]

            if (currentCommand == "set_lbl"):
                try:
                    label_name = (self.program[label_pointer+1])
                    self.labels[label_name] = (label_pointer+1)
                    label_pointer += 2
                except IndexError:
                    raise RuntimeError("Reached the end of the program " \
                                       "unexpectedly", self.pointer)

            label_pointer += 1