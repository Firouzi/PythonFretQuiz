import pygame
import random
from Gui import GuiButton, GuiContainer

MAX_STRINGS = 5
MAX_FRETS = 12
MAX_INTERVALS = 24

class GameIntQuiz:
    def __init__(self, fretboard, screen):
        self.fretboard = fretboard
        self.screen = screen
        self.mode = "RUN"
        self.max_interval = 9 #TODO CAN CHANGE THIS?
        self.max_string_gap = 1 #TODO CAN CHANGE THIS? (0 - same string, 1 = neighbor strings, etc)
        self.max_fret_gap = 5 #TODO CAN CHANGE THIS? (0 - same fret, 1 = neighbor frets, etc)
        self.current_interval = 0
        self.current_note1 = None
        self.current_note2 = None
        self.compound = False
        self.next()

        self.myfont = pygame.font.SysFont('Comic Sans MS', 20)
        self.render_incorrect = self.myfont.render('Incorrect', False, (255, 0, 0))

        self.instruction_font = pygame.font.SysFont('Comic Sans MS', 20)
        self.instructions1 = self.instruction_font.render('Interval Keys 1-8, t (1 = Uni, 8 = Oct, t= TT)', False, (200, 200, 0))
        self.instructions2 = self.instruction_font.render('Up = Major/Aug, Down = minor/dim', False, (200, 200, 0))
        self.instructions3 = self.instruction_font.render('Compound int, Shift key + interval', False, (200, 200, 0))
        self.instructions4 = self.instruction_font.render('n: next interval', False, (200, 200, 0))
        self.instructions5 = self.instruction_font.render('s: change max string gap', False, (200, 200, 0))
        self.instructions6 = self.instruction_font.render('f: change max fret gap', False, (200, 200, 0))
        self.instructions7 = self.instruction_font.render('i: change max intervel gap', False, (200, 200, 0))


    def next(self):
        self.has_guessed = False
        self.current_note1 = self.fretboard.getRandomNote()
        self.current_note2 = self.fretboard.getRandomNote()
        while self.current_note1 == self.current_note2 or \
                abs(self.current_note1.tone - self.current_note2.tone) > self.max_interval or \
                abs(self.current_note1.string - self.current_note2.string) > self.max_string_gap or \
                abs(self.current_note1.fret - self.current_note2.fret) > self.max_fret_gap :
            self.current_note1 = self.fretboard.getRandomNote()
            self.current_note2 = self.fretboard.getRandomNote()
        self.current_interval = abs(self.current_note1.tone - self.current_note2.tone)
        if abs(self.current_note1.tone - self.current_note2.tone) > 12:
            self.compound = True
        else:
            self.compound = False

    def updateMaxString(self):
        self.max_string_gap +=1
        if self.max_string_gap > MAX_STRINGS:
            self.max_string_gap = 0

    def updateMaxFret(self):
        self.max_fret_gap += 1
        if self.max_fret_gap > MAX_FRETS:
            self.max_fret_gap = 0

    def updateMaxInterval(self):
        self.max_interval += 1
        if self.max_interval > MAX_INTERVALS:
            self.max_interval = 0

    def receiveClick(self, pos):
        pass

    def receiveKeydown(self, key, keysdown):
        if self.mode != "RUN":
            return
        guess = None
        major = keysdown[pygame.K_UP]
        minor = keysdown[pygame.K_DOWN]
        guess_compound = False
        if keysdown[pygame.KMOD_SHIFT]:
            guess_compound = True

        if key == pygame.K_1:
            if major:
                guess = None #invalid, this is unison
            elif minor:
                guess = None #invalid, this is unison
            else:
                guess = 0
        elif key == pygame.K_2:
            if minor:
                guess = 1
            elif major:
                guess = 2
            else:
                guess = None  # invalid, need to choose major/minor
        elif key == pygame.K_3:
            if minor:
                guess = 3
            elif major:
                guess = 4
            else:
                guess = None  # invalid, need to choose major/minor
        elif key == pygame.K_4:
            if minor:
                guess = None # invalid, not including dim 4th
            elif major:
                guess = None #Choose T for Tri tone
            else:
                guess = 5  # Perfect 4th
        elif key == pygame.K_t:
            if minor:
                guess = None #tt
            elif major:
                guess = None #tt
            else:
                guess = 6 #tt
        elif key == pygame.K_5:
            if minor:
                guess = None #Choose T for Tri tone
            elif major:
                guess = None #invalid not including Aug 5th
            else:
                guess = 7  # Perfect 4th
        elif key == pygame.K_6:
            if minor:
                guess = 8 #Choose T for Tri tone
            elif major:
                guess = 9 #invalid not including Aug 5th
            else:
                guess = None  # invalid, need to choose major/minor
        elif key == pygame.K_7:
            if minor:
                guess = 10 #Choose T for Tri tone
            elif major:
                guess = 11 #invalid not including Aug 5th
            else:
                guess = None  # invalid, need to choose major/minor
        elif key == pygame.K_8:
            if minor:
                guess = None #invalid for octave
            elif major:
                guess = None #invalid for octave
            else:
                guess = 12  #PO
        elif key == pygame.K_s: #change string number
            self.updateMaxString()
            return
        elif key == pygame.K_f: #change string number
            self.updateMaxFret()
            return
        elif key == pygame.K_i: #change string number
            self.updateMaxInterval()
            return
        elif key == pygame.K_n: #next interval
            self.next()
            return


        if guess is None:
            return

        if guess == self.current_interval and guess_compound == self.compound:
            self.next()
        else:
            self.has_guessed = True

    def render(self):
        if self.mode == "RUN":
            self.render_maxstrings = self.myfont.render(str(self.max_string_gap), False, (0, 0, 255))
            self.render_maxfrets = self.myfont.render(str(self.max_fret_gap), False, (0, 0, 255))
            self.render_maxintervals = self.myfont.render(str(self.max_interval), False, (0, 0, 255))
            self.screen.blit(self.instructions1, (700, 100))
            self.screen.blit(self.instructions2, (700, 135))
            self.screen.blit(self.instructions3, (700, 170))
            self.screen.blit(self.instructions4, (700, 205))
            self.screen.blit(self.instructions5, (700, 240))
            self.screen.blit(self.render_maxstrings, (950, 240))
            self.screen.blit(self.instructions6, (700, 275))
            self.screen.blit(self.render_maxfrets, (950, 275))
            self.screen.blit(self.instructions7, (700, 310))
            self.screen.blit(self.render_maxintervals, (950, 310))


            pygame.draw.circle(self.screen,
                               (255, 0, 0),
                               self.current_note1.position,
                               10)

            pygame.draw.circle(self.screen,
                               (255, 0, 0),
                               self.current_note2.position,
                               10)

            if self.has_guessed:
                self.screen.blit(self.render_incorrect, (50, 600))

    def stop(self):
        self.mode = "STOP"