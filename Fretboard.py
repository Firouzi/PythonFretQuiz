import random
import pygame

class Note:
    def __init__(self, tone, names, octave, string, fret, position, id):
        self.tone = tone
        self.names = names
        self.octave = octave
        self.string = string
        self.fret = fret
        self.position = position
        self.id = id #give each fret position a unique ID
        self.is_active = True
        self.type ="NOTE"

    #return true if this click is within the position of the note
    def checkClick(self, pos):
        if self.position[0]-11 < pos[0] < self.position[0]+11: #check X radius
            if self.position[1] - 15 < pos[1] < self.position[1] + 15: #check Y radius
                return True
        return False

    def toggleActive(self):
        self.is_active = not self.is_active

class String:
    def __init__(self, number, notes, position):
        self.number = number
        self.notes = notes
        #display slightly above open fret to allow toggle of entire string
        self.position = position

        self.is_active = True
        self.type = "STRING"

    def toggleActive(self):
        if self.is_active:
            for note in self.notes:
                note.is_active = False
        else:
            for note in self.notes:
                note.is_active = True
        self.is_active = not self.is_active

    #return a note if clicked on
    def checkClick(self, pos):
        #See if the string is being clicked
        if self.position[0]-11 < pos[0] < self.position[0]+11: #check X radius
            if self.position[1] - 15 < pos[1] < self.position[1] + 15: #check Y radius
                return self
        #See if any notes on the string are being clicked
        for note in self.notes:
            if note.checkClick(pos):
                return note
        return None

class Fret:
    def __init__(self, number, notes, position):
        self.number = number
        self.notes = notes
        self.position = position

        self.is_active = True
        self.type = "FRET"

    def toggleActive(self):
        if self.is_active:
            for note in self.notes:
                note.is_active = False
        else:
            for note in self.notes:
                note.is_active = True
        self.is_active = not self.is_active

    #we check the notes on the strings, so just check if the fret was selected here
    def checkClick(self, pos):
        if self.position[0]-11 < pos[0] < self.position[0]+11: #check X radius
            if self.position[1] - 15 < pos[1] < self.position[1] + 15: #check Y radius
                return self

class Fretboard:
    def __init__(self, strings, frets):
        self.strings = strings
        self.frets = frets
        #for random not quizzes, choose the set of active notes
        self.active_notes = list()

        #define the number instances of each note on the fretboard
        self.num_notes = dict() #{(note name, octave) : count}
        self.init_num_notes()

    #go along the strings and add each note (each name of a note if applicable)/octave pair
    def init_num_notes(self):
        for string in self.strings:
            for note in string.notes:
                for name in note.names:
                    if self.num_notes.get((name, note.octave)) is None:
                        self.num_notes[(name, note.octave)] = 1
                    else:
                        self.num_notes[(name, note.octave)]+=1

    #updates the current active notes for the quiz, returns FALSE if not active
    def setActiveNotes(self):
        self.active_notes = list()
        for string in self.strings:
            for note in string.notes:
                if note.is_active:
                    self.active_notes.append(note)
        if len(self.active_notes) < 1:
            return False
        return True

    def getRandomNote(self):
        index =  random.randint(0, len(self.active_notes)-1)
        return self.active_notes[index]

    #return a note if clicked on
    def checkClick(self, pos):
        for string in self.strings:
            found_target = string.checkClick(pos)
            if found_target is not None:
                return found_target
        for fret in self.frets:
            found_target = fret.checkClick(pos)
            if found_target is not None:
                return found_target
        return None

#note_<String#>_<Fret#>
#String 6
             #tone    name   octave  string  fret #position   id
note_6_0 =  Note(0,  ("E",),    2,      6,      0, (115,39),   0)
note_6_1 =  Note(1,  ("F",),    2,      6,      1, (143,83),   1)
note_6_2 =  Note(2,  ("F#","Gb"), 2,    6,      2, (209,174),  2)
note_6_3 =  Note(3,  ("G",),      2,    6,      3, (268,256),  3)
note_6_4 =  Note(4,  ("G#","Ab"), 2,    6,      4, (331,345),  4)
note_6_5 =  Note(5,  ("A",),      2,    6,      5, (393,435),  5)
note_6_6 =  Note(6,  ("A#","Bb"), 2,    6,      6, (459,520),  6)
note_6_7 =  Note(7,  ("B",),      2,    6,      7, (519,612),  7)
note_6_8 =  Note(8,  ("C",),      3,    6,      8, (586,702),  8)
note_6_9 =  Note(9,  ("C#","Db"), 3,    6,      9, (655,792),  9)
note_6_10 = Note(10, ("D",),      3,    6,      10, (719,884),  10)
note_6_11 = Note(11, ("D#","Eb"), 3,    6,      11, (783,976),  11)
note_6_12 = Note(12, ("E",),      3,    6,      12, (849,1062), 12)
string6_notes = (note_6_0, note_6_1, note_6_2, note_6_3, note_6_4, note_6_5,
                 note_6_6, note_6_7, note_6_8, note_6_9, note_6_10, note_6_11, note_6_12)
string_6 = String(6, string6_notes, (107,21))

#String 5
note_5_0 =  Note(5,   ("A",),      2,   5,  0, (142,40),   13)
note_5_1 =  Note(6,   ("A#","Bb"), 2,   5,  1,  (171,83),   14)
note_5_2 =  Note(7,   ("B",),      2,   5,  2,  (234,170),  15)
note_5_3 =  Note(8,   ("C",),      3,   5,  3,  (297,255),  16)
note_5_4 =  Note(9,   ("C#","Db"), 3,   5,  4,  (358,340),  17)
note_5_5 =  Note(10,  ("D",),      3,   5,  5,  (423,426),  18)
note_5_6 =  Note(11,  ("D#","Eb"), 3,   5,  6,  (487,510),  19)
note_5_7 =  Note(12,  ("E",),      3,   5,  7,  (552,596),  20)
note_5_8 =  Note(13,  ("F",),      3,   5,  8,  (617,688),  21)
note_5_9 =  Note(14,  ("F#","Gb"), 3,   5,  9,  (681,772),  22)
note_5_10 = Note(15,  ("G",),      3,   5,  10,  (748,863),  23)
note_5_11 = Note(16,  ("G#","Ab"), 3,   5,  11,  (809,951),  24)
note_5_12 = Note(17,  ("A",),      3,   5,  12,  (876,1037), 25)
string5_notes = (note_5_0, note_5_1, note_5_2, note_5_3, note_5_4, note_5_5,
                 note_5_6, note_5_7, note_5_8, note_5_9, note_5_10, note_5_11, note_5_12)
string_5 = String(5, string5_notes, (134,22))

#String 4
note_4_0 =  Note(10,  ("D",),      3,   4,  0, (170,46),   26)
note_4_1 =  Note(11,  ("D#","Eb"), 3,   4,  1,  (197,88),   27)
note_4_2 =  Note(12,  ("E",),      3,   4,  2,  (259,171),  28)
note_4_3 =  Note(13,  ("F",),      3,   4,  3,  (323,251),  29)
note_4_4 =  Note(14,  ("F#","Gb"), 3,   4,  4,  (386,337),  30)
note_4_5 =  Note(15,  ("G",),      3,   4,  5,  (447,421),  31)
note_4_6 =  Note(16,  ("G#","Ab"), 3,   4,  6,  (512,510),  32)
note_4_7 =  Note(17,  ("A",),      3,   4,  7,  (573,587),  33)
note_4_8 =  Note(18,  ("A#","Bb"), 3,   4,  8,  (643,678),  34)
note_4_9 =  Note(19,  ("B",),      3,   4,  9,  (705,758),  35)
note_4_10 = Note(20,  ("C",),      4,   4,  10,  (769,843),  36)
note_4_11 = Note(21,  ("C#","Db"), 4,   4,  11,  (832,927),  37)
note_4_12 = Note(22,  ("D",),      4,   4,  12,  (895,1014), 38)
string4_notes = (note_4_0, note_4_1, note_4_2, note_4_3, note_4_4, note_4_5,
                 note_4_6, note_4_7, note_4_8, note_4_9, note_4_10, note_4_11, note_4_12)
string_4 = String(4, string4_notes, (162,26))

#String 3
note_3_0 =  Note(15, ("G",),       3,   3,  0, (193,50),  39)
note_3_1 =  Note(16, ("G#","Ab"),  3,   3,  1,  (223,94),  40)
note_3_2 =  Note(17, ("A",),       3,   3,  2,  (283,171), 41)
note_3_3 =  Note(18, ("A#","Bb"),  3,   3,  3,  (344,250), 42)
note_3_4 =  Note(19, ("B",),       3,   3,  4,  (407,330), 43)
note_3_5 =  Note(20, ("C",),       4,   3,  5,  (471,417), 44)
note_3_6 =  Note(21, ("C#","Db"),  4,   3,  6,  (535,503), 45)
note_3_7 =  Note(22, ("D",),       4,   3,  7,  (596,578), 46)
note_3_8 =  Note(23, ("D#","Eb"),  4,   3,  8,  (664,668), 47)
note_3_9 =  Note(24, ("E",),       4,   3,  9,  (726,746), 48)
note_3_10 = Note(25, ("F",),       4,   3,  10,  (790,828), 49)
note_3_11 = Note(26, ("F#","Gb"),  4,   3,  11,  (852,910), 50)
note_3_12 = Note(27, ("G",),       4,   3,  12,  (914,990), 51)
string3_notes = (note_3_0, note_3_1, note_3_2, note_3_3, note_3_4, note_3_5,
                 note_3_6, note_3_7, note_3_8, note_3_9, note_3_10, note_3_11, note_3_12)
string_3 = String(3, string3_notes, (186,30))

#String 2
note_2_0 =  Note(19, ("B",),       3,   2,  0, (217,53),  52)
note_2_1 =  Note(20, ("C",),       4,   2,  1,  (245,94),  53)
note_2_2 =  Note(21, ("C#","Db"),  4,   2,  2,  (306,172), 54)
note_2_3 =  Note(22, ("D",),       4,   2,  3,  (365,249), 55)
note_2_4 =  Note(23, ("D#","Eb"),  4,   2,  4,  (430,334), 56)
note_2_5 =  Note(24, ("E",),       4,   2,  5,  (493,413), 57)
note_2_6 =  Note(25, ("F",),       4,   2,  6,  (558,496), 58)
note_2_7 =  Note(26, ("F#","Gb"),  4,   2,  7,  (616,573), 59)
note_2_8 =  Note(27, ("G",),       4,   2,  8,  (683,658), 60)
note_2_9 =  Note(28, ("G#","Ab"),  4,   2,  9,  (748,735), 61)
note_2_10 = Note(29, ("A",),       4,   2,  10,  (809,815), 62)
note_2_11 = Note(30, ("A#","Bb"),  4,   2,  11,  (869,895), 63)
note_2_12 = Note(31, ("B",),       4,   2,  12,  (931,974), 64)
string2_notes = (note_2_0, note_2_1, note_2_2, note_2_3, note_2_4, note_2_5,
                 note_2_6, note_2_7, note_2_8, note_2_9, note_2_10, note_2_11, note_2_12)
string_2 = String(2, string2_notes, (210,33))

#String 1
note_1_0 =  Note(24, ("E",),          4,    1,  0, (238,57),  65)
note_1_1 =  Note(25, ("F",),          4,    1,  1,  (268,99),  66)
note_1_2 =  Note(26, ("F#","Gb"),     4,    1,  2,  (328,179), 67)
note_1_3 =  Note(27, ("G",),          4,    1,  3,  (386,249), 68)
note_1_4 =  Note(28, ("G#","Ab"),     4,    1,  4,  (452,333), 69)
note_1_5 =  Note(29, ("A",),          4,    1,  5,  (513,412), 70)
note_1_6 =  Note(30, ("A#","Bb"),     4,    1,  6,  (579,493), 71)
note_1_7 =  Note(31, ("B",),          4,    1,  7,  (639,566), 72)
note_1_8 =  Note(32, ("C",),          5,    1,  8,  (705,650), 73)
note_1_9 =  Note(33, ("C#","Db"),     5,    1,  9,  (770,730), 74)
note_1_10 = Note(34, ("D",),          5,    1,  10,  (830,807), 75)
note_1_11 = Note(35, ("D#","Eb"),     5,    1,  11,  (889,878), 76)
note_1_12 = Note(36, ("E",),          5,    1,  12,  (949,957), 77)
string1_notes = (note_1_0, note_1_1, note_1_2, note_1_3, note_1_4, note_1_5,
                 note_1_6, note_1_7, note_1_8, note_1_9, note_1_10, note_1_11, note_1_12)
string_1 = String(1, string1_notes, (230,37))
strings = (string_1, string_2, string_3, string_4, string_5, string_6)

fret0_notes =  (note_1_0,  note_2_0,  note_3_0,  note_4_0,  note_5_0,  note_6_0)
fret1_notes =  (note_1_1,  note_2_1,  note_3_1,  note_4_1,  note_5_1,  note_6_1)
fret2_notes =  (note_1_2,  note_2_2,  note_3_2,  note_4_2,  note_5_2,  note_6_2)
fret3_notes =  (note_1_3,  note_2_3,  note_3_3,  note_4_3,  note_5_3,  note_6_3)
fret4_notes =  (note_1_4,  note_2_4,  note_3_4,  note_4_4,  note_5_4,  note_6_4)
fret5_notes =  (note_1_5,  note_2_5,  note_3_5,  note_4_5,  note_5_5,  note_6_5)
fret6_notes =  (note_1_6,  note_2_6,  note_3_6,  note_4_6,  note_5_6,  note_6_6)
fret7_notes =  (note_1_7,  note_2_7,  note_3_7,  note_4_7,  note_5_7,  note_6_7)
fret8_notes =  (note_1_8,  note_2_8,  note_3_8,  note_4_8,  note_5_8,  note_6_8)
fret9_notes =  (note_1_9,  note_2_9,  note_3_9,  note_4_9,  note_5_9,  note_6_9)
fret10_notes = (note_1_10, note_2_10, note_3_10, note_4_10, note_5_10, note_6_10)
fret11_notes = (note_1_11, note_2_11, note_3_11, note_4_11, note_5_11, note_6_11)
fret12_notes = (note_1_12, note_2_12, note_3_12, note_4_12, note_5_12, note_6_12)
fret0 =  Fret(0,  fret0_notes,  (260,60))
fret1 =  Fret(1,  fret1_notes,  (288,99))
fret2 =  Fret(2,  fret2_notes,  (348,179))
fret3 =  Fret(3,  fret3_notes,  (406,249))
fret4 =  Fret(4,  fret4_notes,  (472,333))
fret5 =  Fret(5,  fret5_notes,  (533,412))
fret6 =  Fret(6,  fret6_notes,  (599,485))
fret7 =  Fret(7,  fret7_notes,  (659,560))
fret8 =  Fret(8,  fret8_notes,  (725,640))
fret9 =  Fret(9,  fret9_notes,  (790,720))
fret10 = Fret(10, fret10_notes, (850,790))
fret11 = Fret(11, fret11_notes, (909,865))
fret12 = Fret(12, fret12_notes, (969,940))
frets = (fret0, fret1, fret2, fret3, fret4, fret5, fret6,
         fret7, fret8, fret9, fret10, fret11, fret12)
fretboard = Fretboard(strings, frets)

# image is 432x1358
image = pygame.image.load("C:\\Users\\Robert\\Repos\\FretQuiz\\fretboard_resize2.jpg")
rotated_image = pygame.transform.rotate(image, 40)
new_rect = rotated_image.get_rect(center = (216, 679))