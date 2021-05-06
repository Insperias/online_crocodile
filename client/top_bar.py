import pygame
#-20

class TopBar:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.word = ""
        self.round = 1
        self.max_round = 8
        self.round_font = pygame.font.SysFont("comiscans", 30)
        self.BORDER_THICKNESS = 3
        self.time = 75
        self.drawing = False

    def draw(self, win):
        pygame.draw.rect(win, (0, 0, 0), (self.x, self.y, self.width, self.height), self.BORDER_THICKNESS)
        # round
        text = self.round_font.render(f"Round {self.round} of {self.max_round}", 1, (0, 0, 0))
        win.blit(text, (self.x + 10, self.y + self.height/2 - text.get_height()/2))

        # underscores
        if self.drawing:
            wrd = self.word
        else:
            wrd = TopBar.underscore_text(self.word)
        text = self.round_font.render(wrd, 1, (0, 0, 0))
        win.blit(text, (self.x + self.width/2 - text.get_width()/2, self.y + self.height/2 - text.get_height()/2 + 10))

        pygame.draw.circle(win, (0, 0, 0), (self.x + self.width - 30, self.y + round(self.height/2)), 20, self.BORDER_THICKNESS)
        timer = self.round_font.render(str(self.time), 1, (0, 0, 0))
        win.blit(timer, (self.x + self.width - 30 - timer.get_width()/2, self.y + self.height/2 - timer.get_height()/2))

    @staticmethod
    def underscore_text(text):
        new_str = ""

        for char in text:
            if char != " ":
                new_str += " _ "
            else:
                new_str += "   "
        return new_str

    def change_word(self, word):
        self.word = word

    def change_round(self, round):
        self.round = round