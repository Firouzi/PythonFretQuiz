import pygame
from Gui import GuiButton, GuiContainer
from Modes.Note_quiz import GameNoteQuiz
from Modes.Find_note import GameFindNote
from Modes.Int_quiz  import GameIntQuiz
from Fretboard import fretboard, rotated_image

class FretGame:
    def __init__(self,
                 screen):
        self.screen = screen

        self.fretboard = fretboard
        self.fretboard_image = rotated_image
        self.mode = "SETUP" #["SETUP, "GAME"]

        self.game = None

        #Build the main menu gui
        buttonfont = pygame.font.SysFont('Comic Sans MS', 50)
        notequiz_surface = buttonfont.render('Note Quiz', False, (200, 200, 0))
        findnote_surface = buttonfont.render('Find Note', False, (200, 200, 0))
        intquiz_surface = buttonfont.render('Interval Quiz', False, (200, 200, 0))
        stop_surface = buttonfont.render('STOP', False, (200, 200, 0))
        notequiz_button = GuiButton("NOTE_QUIZ", notequiz_surface, (750, 25), "SETUP")
        findnote_button = GuiButton("FIND_NOTE", findnote_surface, (750, 125), "SETUP")
        intquiz_button = GuiButton("INT_QUIZ", intquiz_surface, (750, 220), "SETUP")
        stop_button = GuiButton("STOP", stop_surface, (800, 25), "GAME")
        gui_widgets = (notequiz_button, stop_button, findnote_button, intquiz_button)
        self.gui_container = GuiContainer(gui_widgets, self.screen)

    def initialize(self):
        self.fretboard.setActiveNotes()

    def setMode(self, mode):
        self.mode = mode
        self.gui_container.setMode(mode)

    def receiveClick(self, pos):
        if self.mode == "SETUP":
            self.clickModeSetup(pos)
        elif self.mode == "GAME":
            self.clickModeGame(pos)

    def clickModeSetup(self, pos):
        target = self.gui_container.checkClick(pos)
        if target is not None:
            if target.name == "NOTE_QUIZ":
                if len(self.fretboard.active_notes) < 2:
                    print("Choose atleast 2 notes for the game")
                    return
                self.mode = "GAME"
                self.gui_container.setMode("GAME")
                self.game = GameNoteQuiz(self.fretboard, self.screen)
            if target.name == "FIND_NOTE":
                self.mode = "GAME"
                self.gui_container.setMode("GAME")
                self.game = GameFindNote(self.fretboard,self.screen)
            if target.name == "INT_QUIZ":
                self.mode = "GAME"
                self.gui_container.setMode("GAME")
                self.game = GameIntQuiz(self.fretboard,self.screen)
        else:
            target = self.fretboard.checkClick(pos)
            if target is not None:
                if target.type == "STRING" or target.type == "NOTE" or target.type == "FRET":
                    target.toggleActive()
                    self.fretboard.setActiveNotes()

    def clickModeGame(self, pos):
        target = self.gui_container.checkClick(pos)
        if target is not None:
            if target.name == "STOP":
                self.game.stop()
                self.mode = "SETUP"
                self.gui_container.setMode("SETUP")
        else:
            self.game.receiveClick(pos)

    def receiveKeydown(self, key, keysdown):
        if self.mode == "SETUP":
            self.keydownModeSetup(key, keysdown)
        elif self.mode == "GAME":
            self.keydownModeNoteQuiz(key, keysdown)

    def keydownModeSetup(self, key, keysdown):
        pass

    def keydownModeNoteQuiz(self, key, keysdown):
        self.game.receiveKeydown(key, keysdown)

    def render(self):
        self.screen.blit(self.fretboard_image, (-50, -110))
        self.gui_container.render()
        if self.mode == "SETUP":
            self.renderNoteSelection()
            self.renderStringPosition()
            self.renderFretPosition()
        #render the game, or results from previous game
        if self.game is not None:
            self.game.render()

    def renderFretPosition(self):
        for fret in self.fretboard.frets:
            if fret.is_active:
                size = 10
            else:
                size = 5
            pygame.draw.circle(self.screen,
                               (255, 0, 255),
                               fret.position,
                               size)

    def renderStringPosition(self):
        for string in self.fretboard.strings:
            if string.is_active:
                size = 10
            else:
                size = 5
            pygame.draw.circle(self.screen,
                               (0, 0, 255),
                               string.position,
                               size)

    def renderNoteSelection(self):
        for string in self.fretboard.strings:
            for note in string.notes:
                if note.is_active:
                    pygame.draw.circle(self.screen,
                                       (255, 0, 0),
                                       note.position,
                                       10)
                else:
                    pygame.draw.circle(self.screen,
                                       (255,255,255),
                                       note.position,
                                       5)