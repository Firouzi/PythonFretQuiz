import pygame

WHOLE_NOTE = 0
HALF_NOTE = 1
QUARTER_NOTE = 2


class DrawStaff:
    def __init__(self, screen, position = (100,100), height = 100, width = 150):
        self.screen = screen
        self.position = position
        self.height = height
        self.width = width

        self._staff_color = (255, 255, 255)
        self._note_color = (255, 255, 255)
        self._staff_thickness = 2
        self.half_gap = 0 #space between the lines
        self._staff_positions = dict() #just the Y coord, X coord is same for all
        self._accidental_font = None
        self._flatstring = None
        self._sharpstring = None
        self._setupStaff()

    def _setupStaff(self):
        self._accidental_font = pygame.font.SysFont('arial', int(self.height/4))
        self._flatstring = self._accidental_font.render('b', False, self._note_color)
        self._sharpstring = self._accidental_font.render('#', False, self._note_color)
        y = self.position[1]
        #LINES
        #above the staff
        self._staff_positions["E5"] = int(y - (0.75*self.height))
        self._staff_positions["C5"] = int(y - (0.5*self.height))
        self._staff_positions["A4"] = int(y - (0.25*self.height))
        #the visible staff lines: EGBDF
        self._staff_positions["F4"] = int(y)
        self._staff_positions["D4"] = int(y + (0.25*self.height))
        self._staff_positions["B3"] = int(y + (0.5*self.height))
        self._staff_positions["G3"] = int(y + (0.75*self.height))
        self._staff_positions["E3"] = int(y + self.height)
        #below the staff
        self._staff_positions["C3"] = int(y + (1.25 * self.height))
        self._staff_positions["A2"] = int(y + (1.5 * self.height))
        self._staff_positions["F2"] = int(y + (1.75 * self.height))
        #SPACES
        self.half_gap = int(0.5*(self._staff_positions["C5"] - self._staff_positions["E5"]))
        #above the staff
        self._staff_positions["D5"] = self._staff_positions["E5"] + self.half_gap
        self._staff_positions["B4"] = self._staff_positions["C5"] + self.half_gap
        #on the staff
        self._staff_positions["G4"] = self._staff_positions["A4"] + self.half_gap
        self._staff_positions["E4"] = self._staff_positions["F4"] + self.half_gap
        self._staff_positions["C4"] = self._staff_positions["D4"] + self.half_gap
        self._staff_positions["A3"] = self._staff_positions["B3"] + self.half_gap
        self._staff_positions["F3"] = self._staff_positions["G3"] + self.half_gap
        self._staff_positions["D3"] = self._staff_positions["E3"] + self.half_gap
        #below the staff
        self._staff_positions["B2"] = self._staff_positions["C3"] + self.half_gap
        self._staff_positions["G2"] = self._staff_positions["A2"] + self.half_gap
        self._staff_positions["E2"] = self._staff_positions["F2"] + self.half_gap



    def setPosition(self, position):
        self.position = position
        self._setupStaff()

    def setHeight(self, height):
        self.height = height
        self._setupStaff()

    def setWidth(self, width):
        self.width = width
        self._setupStaff()

    def renderStaff(self):
        x1 = self.position[0]
        x2 = self.position[0] + self.width

        pygame.draw.line(self.screen,
                         self._staff_color,
                         (x1,self._staff_positions["E3"]), #start pos
                         (x2,self._staff_positions["E3"]), #end pos
                         self._staff_thickness)
        pygame.draw.line(self.screen,
                         self._staff_color,
                         (x1,self._staff_positions["G3"]), #start pos
                         (x2,self._staff_positions["G3"]), #end pos
                         self._staff_thickness)
        pygame.draw.line(self.screen,
                         self._staff_color,
                         (x1,self._staff_positions["B3"]), #start pos
                         (x2,self._staff_positions["B3"]), #end pos
                         self._staff_thickness)
        pygame.draw.line(self.screen,
                         self._staff_color,
                         (x1,self._staff_positions["D4"]), #start pos
                         (x2,self._staff_positions["D4"]), #end pos
                         self._staff_thickness)
        pygame.draw.line(self.screen,
                         self._staff_color,
                         (x1,self._staff_positions["F4"]), #start pos
                         (x2,self._staff_positions["F4"]), #end pos
                         self._staff_thickness)

        vert_x = int(0.1*(x2-x1) + x1)
        vert_y1 = int(self.position[1] - 0.1*self.height)
        vert_y2 = int(self.position[1] + self.height + 0.1*self.height)

        pygame.draw.line(self.screen,
                         self._staff_color,
                         (vert_x,vert_y1), #start pos
                         (vert_x, vert_y2), #end pos
                         self._staff_thickness-1)


    def renderNote(self, note_name, octave, note_type = QUARTER_NOTE):
        is_sharp = False
        is_flat = False
        if len(note_name) > 1:
            if note_name[1] == "#":
                is_sharp=True
            else:
                is_flat=True

        key=""
        key+= note_name[0]
        key+= str(octave)
        x_position = int(self.position[0] + (0.5*self.width))
        y_position = self._staff_positions[key]

        #we are above the staff, need to draw more lines
        if y_position < self.position[1]:
            lines = 1
            if key == "E5":
                lines = 3
            elif key == "D5" or key == "C5":
                lines = 2
            elif key == "G4":
                lines = 0 #it just sits right on top
            if lines == 3:
                pygame.draw.line(self.screen,
                                 self._staff_color,
                                 (x_position - (2*self.half_gap), self._staff_positions["E5"]),  # start pos
                                 (x_position + (2*self.half_gap), self._staff_positions["E5"]),  # end pos
                                 self._staff_thickness)
            if lines >=2:
                pygame.draw.line(self.screen,
                                 self._staff_color,
                                 (x_position - (2 * self.half_gap), self._staff_positions["C5"]),  # start pos
                                 (x_position + (2 * self.half_gap), self._staff_positions["C5"]),  # end pos
                                 self._staff_thickness)
            if lines >=1:
                pygame.draw.line(self.screen,
                                 self._staff_color,
                                 (x_position - (2 * self.half_gap), self._staff_positions["A4"]),  # start pos
                                 (x_position + (2 * self.half_gap), self._staff_positions["A4"]),  # end pos
                                 self._staff_thickness)
        #we are below the staff, need more lines
        elif y_position > self.position[1] + self.height:
            lines = 1
            if key == "F2" or key == "E2":
                lines = 3
            elif key == "G2" or key == "A2":
                lines = 2
            elif key == "D3":
                lines = 0
            if lines == 3:
                pygame.draw.line(self.screen,
                                 self._staff_color,
                                 (x_position - (2 * self.half_gap), self._staff_positions["F2"]),  # start pos
                                 (x_position + (2 * self.half_gap), self._staff_positions["F2"]),  # end pos
                                 self._staff_thickness)
            if lines >=2:
                pygame.draw.line(self.screen,
                                 self._staff_color,
                                 (x_position - (2 * self.half_gap), self._staff_positions["A2"]),  # start pos
                                 (x_position + (2 * self.half_gap), self._staff_positions["A2"]),  # end pos
                                 self._staff_thickness)
            if lines >=1:
                pygame.draw.line(self.screen,
                                 self._staff_color,
                                 (x_position - (2 * self.half_gap), self._staff_positions["C3"]),  # start pos
                                 (x_position + (2 * self.half_gap), self._staff_positions["C3"]),  # end pos
                                 self._staff_thickness)
        if note_type == QUARTER_NOTE or True:
            pygame.draw.circle(self.screen,
                               self._note_color,
                               (x_position, y_position),
                               self.half_gap)
            #draw the stem
            if y_position > self._staff_positions["B3"]:
                #stem up
                pygame.draw.line(self.screen,
                                 self._note_color,
                                 (x_position + (self.half_gap), y_position),  # start pos
                                 (x_position + (self.half_gap), y_position - (self.height/2)),  # end pos
                                 self._staff_thickness)
            else:
                # stem down
                pygame.draw.line(self.screen,
                                 self._note_color,
                                 (x_position - (self.half_gap), y_position),  # start pos
                                 (x_position - (self.half_gap), y_position + (self.height / 2)),  # end pos
                                 self._staff_thickness)
        if is_sharp:
            self.screen.blit(self._sharpstring, (x_position - (2.2 * self.half_gap), y_position - self.half_gap))
        elif is_flat:
            self.screen.blit(self._flatstring, (x_position - (2.2 * self.half_gap), y_position- self.half_gap))
