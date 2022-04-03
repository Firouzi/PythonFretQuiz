import pygame
import time
from Gui import GuiButton, GuiContainer

class GameNoteQuiz:
    def __init__(self, fretboard, screen):
        self.fretboard = fretboard
        self.screen = screen

        #using floats to calc accuracy %
        self.num_correct = 0.0
        self.num_wrong = 0.0
        #track time played and avg time to get answer
        self.time_start = time.time()
        self.play_time = 0.0
        self.avg_time = 0.0
        self.accuracy = 0.0
        self.render_accuracy = None
        self.render_playtime = None
        self.render_avgtime = None
        self.myfont = pygame.font.SysFont('Comic Sans MS', 50)
        self.render_incorrect = self.myfont.render('Incorrect', False, (255, 0, 0))
        self.render_complete = self.myfont.render('COMPLETE', False, (0, 0, 255))
        #this is the note that we are supposed to name
        self.current_note = self.fretboard.getRandomNote()
        #only mark a guess wrong once
        self.has_guessed = False
        self.mode = "RUN"

        #build the game gui
        buttonfont = pygame.font.SysFont('Comic Sans MS', 50)
        instruction_font = pygame.font.SysFont('Comic Sans MS', 20)
        next_surface = buttonfont.render('NEXT', False, (200, 200, 0))
        next_button = GuiButton("NEXT_GAME", next_surface, (50, 950), "ANY")
        gui_widgets = (next_button,)
        self.instructions1 = instruction_font.render('Use Keyboard: ABCDEFG to guess note', False, (200, 200, 0))
        self.instructions2 = instruction_font.render('Hold UP arrow to make #', False, (200, 200, 0))
        self.instructions3 = instruction_font.render('Hold DOWN arrow to make b', False, (200, 200, 0))
        self.gui_container = GuiContainer(gui_widgets, self.screen)

    def receiveClick(self, pos):
        target = self.gui_container.checkClick(pos)
        if target is not None:
            if target.name == "NEXT_GAME":
                self.next()

    def receiveKeydown(self, key, keysdown):
        if self.mode != "RUN":
            return
        guess = None
        sharp = keysdown[pygame.K_UP]
        flat = keysdown[pygame.K_DOWN]
        if key == pygame.K_a:
            if sharp:
                guess ="A#"
            elif flat:
                guess ="Ab"
            else:
                guess ="A"
        elif key == pygame.K_b:
            if sharp:
                guess ="B#"
            elif flat:
                guess ="Bb"
            else:
                guess ="B"
        elif key == pygame.K_c:
            if sharp:
                guess ="C#"
            elif flat:
                guess ="Cb"
            else:
                guess ="C"
        elif key == pygame.K_d:
            if sharp:
                guess ="D#"
            elif flat:
                guess ="Db"
            else:
                guess ="D"
        elif key == pygame.K_e:
            if sharp:
                guess ="E#"
            elif flat:
                guess ="Eb"
            else:
                guess ="E"
        elif key == pygame.K_f:
            if sharp:
                guess ="F#"
            elif flat:
                guess ="Fb"
            else:
                guess ="F"
        elif key == pygame.K_g:
            if sharp:
                guess ="G#"
            elif flat:
                guess ="Gb"
            else:
                guess ="G"
        elif key == pygame.K_n:
            self.next()

        if guess is not None:
            if guess in self.current_note.names:
                self.num_correct+=1.0
                self.has_guessed = False
                #don't repeat the same note twice in a row
                candidate_note = self.fretboard.getRandomNote()
                while candidate_note == self.current_note:
                    candidate_note = self.fretboard.getRandomNote()
                self.current_note = candidate_note
            else:
                if not self.has_guessed:
                    self.has_guessed = True
                    self.num_wrong += 1.0

    def next(self):
        self.has_guessed = False
        # don't repeat the same note twice in a row
        candidate_note = self.fretboard.getRandomNote()
        while candidate_note == self.current_note:
            candidate_note = self.fretboard.getRandomNote()
        self.current_note = candidate_note

    def results(self):
        if self.num_correct + self.num_wrong > 0.5:
            self.play_time = time.time() - self.time_start
            self.avg_time = round(self.play_time / (self.num_correct + self.num_wrong), 2)
            self.accuracy = round(self.num_correct / (self.num_correct + self.num_wrong) * 100, 2)
            self.accuracyString(self.num_correct, self.num_wrong)
            self.timeString(self.time_start, self.num_correct + self.num_wrong)

    def accuracyString(self, num_currect, num_wrong):
        accuracy = round(num_currect / (num_currect + num_wrong) * 100, 2)
        render_string = str(int(num_currect)) + "/" + str(int(num_wrong + num_currect)) + " = " + str(accuracy) + "%"
        self.render_accuracy = self.myfont.render(render_string, False, (0, 0, 255))

    def timeString(self, start_time, numb_trials):
        play_time = time.time() - start_time
        avg_time = round(play_time / numb_trials, 2)
        render_playtime = "Play time: " + str(round(play_time, 2)) + "s"
        render_avgtime = "Avg per note: " + str(avg_time) + "s"
        self.render_playtime = self.myfont.render(render_playtime, False, (0, 0, 255))
        self.render_avgtime = self.myfont.render(render_avgtime, False, (0, 0, 255))

    def render(self):
        if self.mode == "RUN":
            self.screen.blit(self.instructions1, (700, 110))
            self.screen.blit(self.instructions2, (700, 150))
            self.screen.blit(self.instructions3, (700, 190))
            pygame.draw.circle(self.screen,
                               (255, 0, 0),
                               self.current_note.position,
                               10)
            if self.has_guessed:
                self.screen.blit(self.render_incorrect, (50, 600))
            self.gui_container.render()
        if self.mode == "RESULTS":
            if self.num_correct + self.num_wrong > 0.5:
                self.screen.blit(self.render_complete, (15, 430))
                self.screen.blit(self.render_accuracy, (15, 485))
                self.screen.blit(self.render_playtime, (15, 540))
                self.screen.blit(self.render_avgtime, (15, 595))

    def stop(self):
        self.results()
        self.mode = "RESULTS"