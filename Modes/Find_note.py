import pygame
import random
from Gui import GuiButton, GuiContainer
from Staff import DrawStaff

class GameFindNote:
    def __init__(self, fretboard, screen):
        self.fretboard = fretboard
        self.screen = screen

        self._draw_staff = DrawStaff(self.screen, position = (50, 400), height = 100, width = 150)

        #gui widgets
        self.game_font = pygame.font.SysFont('Comic Sans MS', 50)
        self.instruction_font = pygame.font.SysFont('Comic Sans MS', 20)
        self.render_incorrect = self.game_font.render('Incorrect', False, (255, 0, 0))
        self.render_correct = self.game_font.render('Correct!', False, (255, 0, 255))
        self.instructions1 = self.instruction_font.render('Click fretboard to find note', False, (200, 200, 0))
        self.instructions2 = self.instruction_font.render('Find all note positions', False, (200, 200, 0))
        self.instructions3 = self.instruction_font.render('Use Keyboard: ABCDEFG to toggle note', False, (200, 200, 0))
        self.instructions4 = self.instruction_font.render('Hold UP arrow to make #', False, (200, 200, 0))
        self.instructions5 = self.instruction_font.render('Hold DOWN arrow to make b', False, (200, 200, 0))
        self.instructions6 = self.instruction_font.render('Keyboard O to toggle Octives', False, (200, 200, 0))
        next_surface = self.game_font.render('NEXT', False, (200, 200, 0))
        next_button = GuiButton("NEXT_GAME", next_surface, (50, 950), "ANY")
        gui_widgets = (next_button,)
        self.gui_container = GuiContainer(gui_widgets, self.screen)

        #display variables
        self.active_notes = {
            'A' : True,
            'Ab' : True,
            'A#' : True,
            'B' : True,
            'Bb' : True,
            'C' : True,
            'C#' : True,
            'D' : True,
            'Db' : True,
            'D#' : True,
            'E' : True,
            'Eb' : True,
            'F' : True,
            'F#' : True,
            'G' : True,
            'Gb' : True,
            'G#' : True,
        }
        self.is_octaves = True #if true, have to select the specific octave
        self.active_note_display = None
        self.updateActiveNoteDisplay()
        self.octave_display = None
        self.progress_display = None
        self.updateIsOctaveDisplay()
        self.is_incorrect = False #if you made a wrong guess
        self.is_correct = False #you got all of them!

        #quiz variables
        self.current_note = None
        self.current_octave = 3
        self.current_octave_display = None
        self.current_note_display = None
        self.selected_notes = list() #the current correct notes that are selected
        self.number_notes_target = 0 #This is how many of the current notes there are to find
        self.setCurrentNote()

        self.mode = "RUN"

    def setCurrentOctave(self):
        min_oct = 3
        max_oct = 4
        if self.current_note in ["E", "F", "F#","Gb", "G", "G#", "Ab", "A", "A#", "Bb", "B"]:
            min_oct = 2
        if self.current_note in ["C", "C#", "Db", "D", "D#", "Eb", "E"]:
            max_oct = 5
        self.current_octave = random.randint(min_oct, max_oct)
        self.current_octave_display = self.game_font.render("Octave: " + str(self.current_octave), False, (0, 0, 255))

    def updateCurrentNoteDisplay(self):
        self.current_note_display = self.game_font.render("Find all: " + str(self.current_note), False, (0, 0, 255))

    def updateIsOctaveDisplay(self):
        if self.is_octaves:
            self.octave_display = self.instruction_font.render("Specify Octave", False, (200, 200, 0))
        else:
            self.octave_display = self.instruction_font.render("All Octaves", False, (200, 200, 0))
        self.next()

    def updateActiveNoteDisplay(self):
        display_string = "Notes: "
        count = 0
        for note, active in self.active_notes.items():
            if active:
                display_string += note + " "
                count += 1
        #require at least 1 active note
        if count < 1:
            self.active_notes['A'] = True
            display_string = "Notes: A"
        self.active_note_display = self.instruction_font.render(display_string, False, (200, 200, 0))

    def setCurrentNote(self):
        note_list = list()
        for key, active in self.active_notes.items():
            if active:
                note_list.append(key)
        index = random.randint(0, len(note_list)-1)
        self.current_note = str(note_list[index])
        self.setCurrentOctave()
        self.setTargetNumber()
        self.selected_notes = list()
        self.updateCurrentNoteDisplay()
        self.is_incorrect = False
        self.is_correct =  False
        self.updateProgressDisplay()

    def updateProgressDisplay(self):
        text = str(len(self.selected_notes)) + "/" + str(self.number_notes_target)
        self.progress_display = self.game_font.render(text, False, (0, 0, 255))

    def setTargetNumber(self):
        min_oct = 2
        max_oct = 5
        if self.is_octaves:
            min_oct = self.current_octave
            max_oct = self.current_octave
        self.number_notes_target = 0
        num_notes=self.fretboard.num_notes
        for i in range(min_oct, max_oct+1):
            if num_notes.get((self.current_note, i)) is not None:
                self.number_notes_target += num_notes.get((self.current_note, i))
        if self.number_notes_target < 1:
            #should not get here
            self.number_notes_target = 1
            print("numb notes error!")

    def next(self):
        self.setCurrentNote()

    def checkGuess(self, note):
        if note not in self.selected_notes and not self.is_correct:
            if self.current_note in note.names:
                if self.is_octaves:
                    if note.octave == self.current_octave:
                        self.selected_notes.append(note)
                        self.is_incorrect = False
                    else:
                        self.is_incorrect = True
                else:
                    self.selected_notes.append(note)
                    self.is_incorrect = False
            else:
                self.is_incorrect = True
            if len(self.selected_notes) == self.number_notes_target:
                self.is_correct = True
            self.updateProgressDisplay()

    def receiveClick(self, pos):
        target = self.fretboard.checkClick(pos)
        if target is not None:
            if target.type == "NOTE":
                if self.mode == "RUN":
                    self.checkGuess(target)
        else:
            target = self.gui_container.checkClick(pos)
            if target is not None:
                if target.name == "NEXT_GAME":
                    self.next()

    def receiveKeydown(self, key, keysdown):
        if self.mode != "RUN":
            return
        toggle = False
        sharp = keysdown[pygame.K_UP]
        flat = keysdown[pygame.K_DOWN]
        if key == pygame.K_a:
            toggle = True
            if sharp:
                self.active_notes['A#'] = not self.active_notes['A#']
            elif flat:
                self.active_notes['Ab'] = not self.active_notes['Ab']
            else:
                self.active_notes['A'] = not self.active_notes['A']
        elif key == pygame.K_b:
            toggle = True
            if sharp:
                toggle = False
            elif flat:
                self.active_notes['Bb'] = not self.active_notes['Bb']
            else:
                self.active_notes['B'] = not self.active_notes['B']
        elif key == pygame.K_c:
            toggle = True
            if sharp:
                self.active_notes['C#'] = not self.active_notes['C#']
            elif flat:
                toggle = False
            else:
                self.active_notes['C'] = not self.active_notes['C']
        elif key == pygame.K_d:
            toggle = True
            if sharp:
                self.active_notes['D#'] = not self.active_notes['D#']
            elif flat:
                self.active_notes['Db'] = not self.active_notes['Db']
            else:
                self.active_notes['D'] = not self.active_notes['D']
        elif key == pygame.K_e:
            toggle = True
            if sharp:
                toggle = False
            elif flat:
                self.active_notes['Eb'] = not self.active_notes['Eb']
            else:
                self.active_notes['E'] = not self.active_notes['E']
        elif key == pygame.K_f:
            toggle = True
            if sharp:
                self.active_notes['F#'] = not self.active_notes['F#']
            elif flat:
                toggle = False
            else:
                self.active_notes['F'] = not self.active_notes['F']
        elif key == pygame.K_g:
            toggle = True
            if sharp:
                self.active_notes['G#'] = not self.active_notes['G#']
            elif flat:
                self.active_notes['Gb'] = not self.active_notes['Gb']
            else:
                self.active_notes['G'] = not self.active_notes['G']
        if toggle:
            self.updateActiveNoteDisplay()
            return
        if key == pygame.K_o:
            self.is_octaves = not self.is_octaves
            self.updateIsOctaveDisplay()

    def render(self):
        if self.mode == "RUN":
            #self.screen.blit(self.current_note_display, (50, 600))
            if self.is_octaves:
                self._draw_staff.renderStaff()
                self._draw_staff.renderNote(self.current_note, self.current_octave)
                self.screen.blit(self.current_octave_display, (50, 655))
            #self.screen.blit(self.progress_display, (50, 710))
            self.screen.blit(self.instructions1, (700, 100))
            self.screen.blit(self.instructions2, (700, 135))
            self.screen.blit(self.instructions3, (700, 170))
            self.screen.blit(self.instructions4, (775, 205))
            self.screen.blit(self.instructions5, (775, 240))
            self.screen.blit(self.instructions6, (700, 275))
            self.screen.blit(self.active_note_display, (550, 305))
            self.screen.blit(self.octave_display, (700, 340))
            for string in self.fretboard.strings:
                for note in string.notes:
                    if note in self.selected_notes:
                        pygame.draw.circle(self.screen,
                                           (0, 0, 255),
                                           note.position,
                                           10)
                    else:
                        pygame.draw.circle(self.screen,
                                           (255, 255, 255),
                                           note.position,
                                           5)
            if self.is_incorrect:
                self.screen.blit(self.render_incorrect, (50, 800))
            elif self.is_correct:
                self.screen.blit(self.render_correct, (50, 800))
            self.gui_container.render()

    def stop(self):
        self.mode = "STOP"