import os
import sys

#DEFINITELY AN ERROR: DOTTED NOTES

class ParseError(Exception):
    def __init__(self, msg):
        msg = "Parse Error: " + msg
        sys.exit(msg)

class txtParser:
    def parse(self, filename):
        try:
            f = open(filename, 'r')
            raw_text = f.read()
            f.close()
        except:
            raise ParseError("Unable to open file '%s'" % filename)

        strings_list = raw_text.split()

        def try_ints(s):
            try:
                return int(s)
            except:
                return s

        symbol_list = list(map(try_ints, strings_list))

        return symbol_list

class mscxParser:
    class Chord:
        pitch_note_dict = {0: "C", 1: "C#", 2: "D", 3: "D#", 4: "E", 5: "F", 
                           6: "F#",7: "G", 8: "G#", 9: "A", 10: "A#", 11: "B"}

        note_order_dict = {"R" : -1, "C" : 0, "C#" : 1, "D" : 2, "D#" : 3, 
                           "E" : 4, "F" : 5, "F#" : 6, "G" : 7, "G#" : 8, 
                           "A" : 9, "A#" : 10, "B" : 11}

        duration_time_dict = {"measure" : 128, "whole" : 128, "half" : 64, 
                              "quarter" : 32, "eighth" : 16, "16th" : 8, 
                              "32nd" : 4, "64th" : 2, "128th" : 1}

        def __init__(self, pitchList, duration, maxStaffTime):
            self.pitchList = sorted(pitchList)
            pitch_note_lambda = (lambda p : self.pitch_to_note(p))
            unsortedNoteList = list(map(pitch_note_lambda, pitchList))
            self.noteList = sorted(unsortedNoteList, key=self.note_key_fn)
            self.startTime = maxStaffTime + 1
            self.duration = self.duration_to_time(duration)

        def pitch_to_note(self, pitch):
            if (pitch == -1): return "R"
            return mscxParser.Chord.pitch_note_dict[(pitch % 12)]

        def duration_to_time(self, duration):
            duration = duration.split()
            if (len(duration) == 1):
                return mscxParser.Chord.duration_time_dict[(duration[0])]
            elif (len(duration) == 2):
                if (duration[0].lower() == "dotted"):
                    return (1.5 * duration_time_dict[(duration[1])])
                else:
                    raise ParseError("Unable to parse note duration '%s'"
                                     % duration)
            else:
                raise ParseError("Unable to parse note duration '%s'"
                                 % duration)

        def __repr__(self):
            return ("(" + str(self.noteList) + "," + str(self.startTime) + ")")

        def note_key_fn(self, note):
            return mscxParser.Chord.note_order_dict[note]

    def __init__(self):
        self.staff1List = []
        self.maxStaff1Time = 0
        self.staff2List = []
        self.maxStaff2Time = 0

        self.staff1Pointer = 0
        self.staff2Pointer = 0

        self.stack_manipulation_chord = []
        self.arithmetic_chord = []
        self.flow_control_chord = []
        self.variable_chord = []
        self.io_chord = []

        self.program = []

    def add_chord(self, staffList, pitchList, durationStr):
        if (staffList == 1):
            maxStaffTime = self.maxStaff1Time
        else:
            maxStaffTime = self.maxStaff2Time

        c = mscxParser.Chord(pitchList, durationStr, maxStaffTime)

        if (staffList == 1):
            self.staff1List.append(c)
            self.maxStaff1Time += c.duration
        else:
            self.staff2List.append(c)
            self.maxStaff2Time += c.duration

    def file_to_chordLists(self, filename):
        import xml.etree.ElementTree as ET
        tree = ET.parse(filename)
        root = tree.getroot()

        for staff in root.iter("Staff"):
            staffList = int(staff.attrib["id"])

            for measure in staff.iter("Measure"):
                for child in measure:
                    durationStr = 0
                    pitchList = []

                    if (child.tag == "Rest"):
                        d = child.find("durationType")
                        durationStr = d.text
                        pitchList.append(-1)

                        self.add_chord(staffList, pitchList, durationStr)

                    elif (child.tag == "Chord"):
                        d = child.find("durationType")
                        durationStr = d.text

                        for note in child.iter("Note"):
                            n = int(note.find("pitch").text)
                            pitchList.append(n)

                        self.add_chord(staffList, pitchList, durationStr)

        remove_rests = (lambda c : (not (c.noteList == ["R"])))
        self.staff1List = list(filter(remove_rests, self.staff1List))
        self.staff2List = list(filter(remove_rests, self.staff2List))

    ################################
    ###  List to Text Functions  ###
    ################################

    def chordList_to_text(self):
        self.STACK_MANIPULATION = 0
        self.ARITHMETIC = 1
        self.FLOW_CONTROL = 2
        self.VARIABLES = 3
        self.IO = 4

        self.stack_manipulation_chord = self.staff2List[0].noteList
        self.arithmetic_chord = self.staff2List[1].noteList
        self.flow_control_chord = self.staff2List[2].noteList
        self.variable_chord = self.staff2List[3].noteList
        self.io_chord = self.staff2List[4].noteList

        self.staff2Pointer = 4
        self.movePointerTo(1, self.staff2List[5].startTime)

        self.currentICM = self.findNextICM()

        variables = dict()
        nextVar = 0
        labels = dict()
        nextLabel = 0

        while (self.currentICM != None):
            self.movePointerTo(1, self.staff2List[self.staff2Pointer].startTime)

            if (self.currentICM == self.STACK_MANIPULATION):
                instruction = self.read_right_binary(3)
                if (instruction == '101'):
                    self.program.append("push")

                    terminator = self.findNextICM()
                    if (not terminator == self.STACK_MANIPULATION):
                        raise ParseError("Found unterminated integer")

                    timeStamp = self.staff2List[self.staff2Pointer].startTime
                    int_read = self.read_right_int(timeStamp)

                    self.program.append(int_read)
                elif (instruction == "111"):
                    self.program.append("dup")
                elif (instruction == "010"):
                    self.program.append("swap")
                elif (instruction == "011"):
                    self.program.append("rotl")
                elif (instruction == "100"):
                    self.program.append("rotl")
                elif (instruction == "110"):
                    self.program.append("drop")

            elif (self.currentICM == self.ARITHMETIC):
                subtype = self.read_right_binary(1)
                instruction = self.read_right_binary(3)

                if (subtype == "1"): #arithmetic manipulation
                    if (instruction == "111"):
                        self.program.append("plus")
                    if (instruction == "000"):
                        self.program.append("minus")
                    if (instruction == "100"):
                        self.program.append("times")
                    if (instruction == "101"):
                        self.program.append("idiv")
                    if (instruction == "110"):
                        self.program.append("div")
                    if (instruction == "010"):
                        self.program.append("mod")
                    if (instruction == "011"):
                        self.program.append("pow")

                elif (subtype == "0"): #comparison arithmetic
                    if (instruction == "111"):
                        self.program.append("less")
                    if (instruction == "110"):
                        self.program.append("greater")
                    if (instruction == "100"):
                        self.program.append("eq")
                    if (instruction == "000"):
                        self.program.append("neq")
                    if (instruction == "001"):
                        self.program.append("and")
                    if (instruction == "011"):
                        self.program.append("or")

            elif (self.currentICM == self.FLOW_CONTROL):
                instruction = self.read_right_binary(3)

                if (instruction == "111"):
                    self.program.append("set_lbl")
                elif (instruction == "110"):
                    self.program.append("call_sub")
                elif (instruction == "100"):
                    self.program.append("jmp_lbl")
                elif (instruction == "011"):
                    self.program.append("jmp_lbl_if")
                elif (instruction == "001"):
                    self.program.append("end_sub")
                elif (instruction == "000"):
                    self.program.append("exit")
                    self.currentICM = self.findNextICM()
                    continue
                elif (instruction == None):
                    self.currentICM = self.findNextICM()
                    continue

                terminator = self.findNextICM()
                if (not terminator == self.FLOW_CONTROL):
                    raise ParseError("Found unterminated label")

                timeStamp = self.staff2List[self.staff2Pointer].startTime
                lbl_str = self.read_right_notes(timeStamp)
                if (lbl_str in labels.keys()):
                    self.program.append(labels[lbl_str])
                else:
                    self.program.append(nextLabel)
                    labels[lbl_str] = nextLabel
                    nextLabel += 1

            elif (self.currentICM == self.VARIABLES):
                instruction = self.read_right_binary(1)

                if (instruction == "1"):
                    self.program.append("save_var")
                elif (instruction == "0"):
                    self.program.append("get_var")
                elif (instruction == None):
                    self.currentICM = self.findNextICM()
                    continue

                terminator = self.findNextICM()
                if (not terminator == self.VARIABLES):
                    raise ParseError("Found unterminated variable")

                timeStamp = self.staff2List[self.staff2Pointer].startTime
                var_str = self.read_right_notes(timeStamp)
                if (var_str in variables.keys()):
                    self.program.append(variables[var_str])
                else:
                    self.program.append(nextVar)
                    variables[var_str] = nextVar
                    nextVar += 1

            elif (self.currentICM == self.IO):
                instruction = self.read_right_binary(2)

                if (instruction == "11"):
                    self.program.append("print_char")
                elif (instruction == "10"):
                    self.program.append("print_int")
                elif (instruction == "01"):
                    self.program.append("read_char")
                elif (instruction == "00"):
                    self.program.append("read_int")

            self.currentICM = self.findNextICM()

        #print("Program  : ", self.program)
        #print("Variables: ", variables)
        #print("Labels   : ", labels)

    def movePointerTo(self, pointerNumber, timeStamp):
        try:
            if (pointerNumber == 1):
                while (self.staff1List[self.staff1Pointer].startTime < timeStamp):
                    self.staff1Pointer += 1
            else:
                while (self.staff2List[self.staff2Pointer].startTime < timeStamp):
                    self.staff2Pointer += 1
        except:
            raise ParseError("Reached the end of the program unexpectedly")

    def binStringToInt(self, binString):
        if (len(binString) < 2):
            raise ParseError("Invalid string literal '%s'" % binString)

        if (binString[0] == '0'):
            return (int(binString[1:], 2))
        else:
            return (-1 * int(binString[1:], 2))

    def findNextICM(self):
        self.staff2Pointer += 1
        if (self.staff2Pointer == len(self.staff2List)): return None
        currentNotes = self.staff2List[self.staff2Pointer].noteList

        while (currentNotes != self.stack_manipulation_chord
               and currentNotes != self.arithmetic_chord
               and currentNotes != self.flow_control_chord
               and currentNotes != self.variable_chord
               and currentNotes != self.io_chord):

            self.staff2Pointer += 1
            if (self.staff2Pointer == len(self.staff2List)): return None
            currentNotes = self.staff2List[self.staff2Pointer].noteList

        if (currentNotes == self.stack_manipulation_chord):
            return self.STACK_MANIPULATION
        elif (currentNotes == self.arithmetic_chord):
            return self.ARITHMETIC
        elif (currentNotes == self.flow_control_chord):
            return self.FLOW_CONTROL
        elif (currentNotes == self.variable_chord):
            return self.VARIABLES
        elif (currentNotes == self.io_chord):
            return self.IO
        else:
            return None

    def chord_compare(self, c1, c2):
        diffs = []

        for i in range(len(c1.pitchList)):
            diffs.append(c2.pitchList[i] - c1.pitchList[i])

        largest_jump = sorted(diffs, key=(lambda x : abs(x)), reverse=True)[0]

        if (largest_jump > 0):
            return 1
        else:
            return 0

    def read_right_binary(self, length):
        try:
            previous = self.staff1List[self.staff1Pointer]

            binString = []
            while(len(binString) < length):
                self.staff1Pointer += 1
                current = self.staff1List[self.staff1Pointer]

                if (len(previous.pitchList) == len(current.pitchList)):
                    binString.append(str(self.chord_compare(previous, current)))

                previous = current

            return ''.join(binString)
        except:
            return None

    def read_right_notes(self, timeStamp):
        try:
            notes = ["|"]

            #self.staff1Pointer += 1
            while(self.staff1List[self.staff1Pointer].startTime <= timeStamp):
                notes += self.staff1List[self.staff1Pointer].noteList
                notes += ["|"]
                self.staff1Pointer += 1
            return ''.join(notes)
        except:
            return None

    def read_right_int(self, timeStamp):
        try:
            previous = self.staff1List[self.staff1Pointer]

            binList = []

            self.staff1Pointer += 1
            while(self.staff1List[self.staff1Pointer].startTime <= timeStamp):
                current = self.staff1List[self.staff1Pointer]

                if (len(previous.pitchList) == len(current.pitchList)):
                    binList.append(str(self.chord_compare(previous, current)))

                previous = current
                self.staff1Pointer += 1

            binString = ''.join(binList)
            return self.binStringToInt(binString)
        except:
            return None

    ################################
    ###          Parse           ###
    ################################

    def parse(self, filename):
        self.file_to_chordLists(filename)
        self.chordList_to_text()
        return self.program

class Parser:
    def parse(self, filename):
        (_, extension) = os.path.splitext(filename)
        if extension == ".txt":
            T = txtParser()
            return T.parse(filename)
        elif extension == ".mscx":
            M = mscxParser()
            return M.parse(filename)
        else:
            raise ParseError("Unable to parse this kind of file.")

if __name__ == "__main__":
    P = Parser()
    P.parse("test_files/print1.mscx")