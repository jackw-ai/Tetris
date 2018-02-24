# Tetris game
# (c) 2018 Tingda Wang

import pygame, sys, random, time
from pygame.locals import *

# Game Object Constants
FPS = 30
WIN_W = 640 # in pixels
WIN_H = 480 # in pixels
SQ_SIZE = 20
BOARD_W = 10 # in squares
BOARD_H = 20 # in squares
NIL = '.' # nothin'

# board margins within window
SIDE_MARGINS = int((WIN_W - (BOARD_W * SQ_SIZE)) / 2)
TOP_MARGIN = WIN_H - (BOARD_H * SQ_SIZE) - 5

''' Difficulty constants'''
# how fast piece moves (FALL_FREQ not constant, will change based on difficulty)
SIDEWAY_FREQ = 0.15
DOWN_FREQ = 0.1
# inverse of rate in which blocks speed up (the lower the faster)
ACCELERATION = 5 

# Fonts
FONT_SIZE = 25
SMALL = 'game_font/thin_pixel.ttf'
BIG = 'game_font/arcadeclassic.ttf'
TITLE = 'game_font/tetro.ttf'

# Music!
MUSIC = ('game_music/theme.ogg', 'game_music/sad_tetris.mp3', 'game_music/scary_tetris.mp3')

# Colors!
WHITE = (252, 252, 252)
PALE = (247, 247, 247)
GRAY = (225, 225, 225)
BLACK = (10, 20, 87)
NOIR =  (31, 35, 38) #(15, 15, 15)
NEO_NOIR = (45, 49, 61)
RED = (237, 28, 91)
LIGHT_RED = (255, 48, 13)
GREEN = (0, 155, 0)
LIGHT_GREEN = (20, 175, 20)
BLUE = (0, 108, 224)
LIGHT_BLUE = (10, 137, 255)
AQUA = (0, 166, 237)
LIGHT_AQUA = (39, 200, 237) 
YELLOW = (245, 236, 136)
LIGHT_YELLOW = (255, 245, 71)
PINK = (241, 71, 255)
LIGHT_PINK = (245, 145, 255)
TURQUOISE = (40, 211, 183)
LIGHT_TURQ = (47, 252, 218) 
ORANGE = (255, 141, 27)
LIGHT_ORANGE = (255, 176, 0)
LEAF = (133, 190, 0)
LIGHT_LEAF = (146, 255, 0)
DARK_PURPLE = (55, 33, 255)
LIGHT_PURPLE = (89, 71, 255)

# piece colors
DARK_COLORS = (BLUE, GREEN, RED, YELLOW, PINK, TURQUOISE, ORANGE, NOIR, PALE, AQUA, LEAF)
LIGHT_COLORS = (LIGHT_BLUE, LIGHT_GREEN, LIGHT_RED, LIGHT_YELLOW, LIGHT_PINK, 
                LIGHT_TURQ, LIGHT_ORANGE, NEO_NOIR, WHITE, LIGHT_AQUA, LIGHT_LEAF)
assert len(DARK_COLORS) == len(LIGHT_COLORS)


# Set UI Color Theme
BORDER = DARK_PURPLE
BORDER_SHADE = LIGHT_PURPLE
BACKGROUND = BLACK
TEXT_COLOR = WHITE
TEXT_SHADOW = GRAY
TITLE_COLOR = LIGHT_AQUA
TITLE_SHADOW = LIGHT_RED

# Templates for each shape
TEMPLATE_W = 5
TEMPLATE_H = 5

S_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '..OO.',
                     '.OO..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '...O.',
                     '.....']]

Z_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '.O...',
                     '.....']]

I_SHAPE_TEMPLATE = [['..O..',
                     '..O..',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     'OOOO.',
                     '.....',
                     '.....']]

O_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '.OO..',
                     '.....']]

J_SHAPE_TEMPLATE = [['.....',
                     '.O...',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..OO.',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '...O.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '.OO..',
                     '.....']]

L_SHAPE_TEMPLATE = [['.....',
                     '...O.',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '.O...',
                     '.....'],
                    ['.....',
                     '.OO..',
                     '..O..',
                     '..O..',
                     '.....']]

T_SHAPE_TEMPLATE = [['.....',
                     '..O..',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '..O..',
                     '.....']]

# dictionary to get corresponding piece template
PIECES = {
    'S': S_SHAPE_TEMPLATE,
    'Z': Z_SHAPE_TEMPLATE,
    'J': J_SHAPE_TEMPLATE,
    'L': L_SHAPE_TEMPLATE,
    'I': I_SHAPE_TEMPLATE,
    'O': O_SHAPE_TEMPLATE,
    'T': T_SHAPE_TEMPLATE
    }

class Piece:
    ''' Piece class that stores shape, rotation, color and coordinate of piece'''

    def __init__(self): 
        ''' initializes empty piece starting in the middle top of board'''
        self.shape = None
        self.rotation = 0
        self.x = int(BOARD_W / 2) - int(TEMPLATE_W / 2)
        self.y = -2
        self.color = None
    
    def get_random(self): 
        ''' randomizes shape, rotation, and color'''
        self.shape = random.choice(list(PIECES.keys()))
        self.rotation = random.randint(0, len(PIECES[self.shape]) - 1)
        self.color = random.randint(0, len(LIGHT_COLORS) - 1)
        return self

class Tetris:
    ''' Tetris class'''

    def __init__(self):
        ''' initializes pygame settings'''
        pygame.init()
        random.seed(1998)
        
        # FPS clock
        self.clock = pygame.time.Clock()

        # display surface
        self.display = pygame.display.set_mode((WIN_W, WIN_H))
        pygame.display.set_caption('Tetris - wtingda')

        # mouse not in the way
        pygame.mouse.set_visible(0)

        # fonts
        if pygame.font:                                 
            self.font = pygame.font.Font(SMALL, FONT_SIZE)           
            self.large_font = pygame.font.Font(BIG, FONT_SIZE * 3)
            self.title_font = pygame.font.Font(TITLE, FONT_SIZE * 4)
        else:      
            self.font = None  
            self.large_font = None

    def run(self):
        ''' main game loop, with music!'''
        self.display.fill(BACKGROUND)
        self.display_text("Tetris", title = True)
        while True: 
            self.music()

            # difficulty variables
            self.score = 0
            self.difficulty = self.speed = 0
            self.set_difficulty() # sets these values

            self.play()
            pygame.mixer.music.stop()
            self.display_text('Game Over')

    def music(self):
        ''' plays music randomly'''
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        
        # plays random music
        pygame.mixer.music.load(random.choice(MUSIC))
        pygame.mixer.music.play(-1, 0.0) # infinite loops, start at beginning

    def get_textobj(self, text, font, color):
        ''' helper for creating text objects'''
        surf = font.render(text, True, color)
        return surf, surf.get_rect()

    def display_text(self, text, title = False): 
        ''' Prints text until key is pressed '''

        # determines color and font used depending on type of text
        if title is True:
            font = self.title_font
            color = (TITLE_COLOR, TITLE_SHADOW)
        else:
            font = self.large_font
            color = (TEXT_COLOR, TEXT_SHADOW)

        # draw text shadow
        title_surf, title_rect = self.get_textobj(text, font, color[1])
        title_rect.center = (int(WIN_W / 2), int(WIN_H / 2))
        self.display.blit(title_surf, title_rect)

        # draw text
        title_surf, title_rect = self.get_textobj(text, font, color[0])
        title_rect.center = (int(WIN_W / 2) - 3, int(WIN_H / 2) - 3)
        self.display.blit(title_surf, title_rect)

        # displays (Press any key to continue)
        title_surf, title_rect = self.get_textobj("(Press any key to continue)", self.font, TEXT_COLOR)
        title_rect.center = (int(WIN_W / 2), int(WIN_H / 2) - 80)
        self.display.blit(title_surf, title_rect)
        
        # wait for keyboard hit to continue
        while self.hit_kb() is None:
            pygame.display.update()
            self.clock.tick()
        
    def hit_kb(self):        
        ''' 
        handles hitting a key in keyboard
        also takes care of checking for quit events such as pressing esc
        '''
        # quit game
        for event in pygame.event.get(QUIT):
            pygame.quit()
            sys.exit()

        for event in pygame.event.get([KEYDOWN, KEYUP]):
            if event.type is KEYUP: # must have finished pressing
                if event.key is K_ESCAPE: # esc to quite
                    pygame.quit()
                    sys.exit()
                else: # otherwise return the key pressed
                    return event.key
        return None

    def set_difficulty(self):
        ''' sets the difficulty and speed variables ''' 
        self.difficulty = int(self.score /ACCELERATION) + 1
        self.speed = 0.27 - (self.difficulty * 0.02)
    
    def get_piece(self):
        ''' gets random piece'''
        piece = Piece()
        return piece.get_random()

    def not_on_board(self, x, y):
        ''' 
        helper for free_space(), checks if coordinates are valid board coordinates 
        '''
        return not (x >= 0 and x < BOARD_W and y < BOARD_H)

    def is_free(self, piece, x_adj = 0, y_adj = 0):
        ''' 
        determins if the piece occupies all free space
        supports optional adjustments x_adj and y_adj
        '''
        for x in range(TEMPLATE_W):
            for y in range(TEMPLATE_H):
                not_fallen_yet = (y + piece.y + y_adj < 0)
                square = PIECES[piece.shape][piece.rotation][y][x]
                if not_fallen_yet or square == NIL: 
                    # coordinate is empty
                    continue
                if self.not_on_board(x + piece.x + x_adj, y + piece.y + y_adj):
                    # coordinate not valid
                    return False
                if self.board[x + piece.x + x_adj][y + piece.y + y_adj] != NIL:
                    # piece on occupied space
                    return False
        return True

    def get_board(self):
        ''' returns an empty board '''
        board = []
        for i in range(BOARD_W):
            board.append([NIL] * BOARD_H)
        return board
    
    def add(self, piece):
        ''' fills in a piece onto board '''
        for x in range(TEMPLATE_W):
            for y in range(TEMPLATE_H):
                if PIECES[piece.shape][piece.rotation][y][x] != NIL:
                    # each element in 2D array boards stores a color
                    self.board[x + piece.x][y + piece.y] = piece.color
        
    def is_full(self, y):
        ''' helper to check is given line is full'''
        for x in range(BOARD_W):
            if self.board[x][y] == NIL:
                return False
        return True

    def delete_full_level(self):
        ''' deletes a full level if there is one and moves everything down'''
        lines_removed = 0
        y = BOARD_H - 1 # start at bottom
        while y >= 0:
            if self.is_full(y):
                # pull everything down one level
                for i in range(y, 0, -1):
                    for j in range(BOARD_W):
                        self.board[j][i] = self.board[j][i - 1]
                # clear top level in case
                for x in range(BOARD_W):
                    self.board[x][0] = NIL
                lines_removed += 1
                # go through loop to check if there is another level to be removed
            else:
                y -= 1 # we know this row isn't full, can go up now
        return lines_removed

    def get_display_coords(self, x, y):
        ''' for given board coord, find relevant coordinates on display'''
        return (SIDE_MARGINS + (x * SQ_SIZE)), (TOP_MARGIN + (y * SQ_SIZE))

    def draw_square(self, x, y, color, disp_x = None, disp_y = None):
        ''' 
        draws a square on the screen at location (x, y) on board 
        supports board coordinates (default) and display coordinates
        '''
        if disp_x is None and disp_y is None:
            disp_x, disp_y = self.get_display_coords(x, y)

        # draws the squares
        pygame.draw.rect(self.display, DARK_COLORS[color], (disp_x + 1, disp_y + 1, SQ_SIZE - 1, SQ_SIZE - 1))
        pygame.draw.rect(self.display, LIGHT_COLORS[color], (disp_x + 4, disp_y + 4, SQ_SIZE - 2 , SQ_SIZE - 2))

    def draw_board(self):
        ''' draws the entire board '''
        # draws the board border
        pygame.draw.rect(self.display, BORDER, (SIDE_MARGINS - 3, TOP_MARGIN - 7, (BOARD_W * SQ_SIZE) + 8, (BOARD_H * SQ_SIZE) + 8), 5)

        pygame.draw.rect(self.display, BORDER_SHADE, (SIDE_MARGINS + 1, TOP_MARGIN - 3, (BOARD_W * SQ_SIZE) + 8, (BOARD_H * SQ_SIZE) + 8), 5)

        # draws the background
        pygame.draw.rect(self.display, BACKGROUND, (SIDE_MARGINS, TOP_MARGIN, SQ_SIZE * BOARD_W, SQ_SIZE * BOARD_H))

        # draws the squares
        for i in range(BOARD_W):
            for j in range(BOARD_H):
                if self.board[i][j] is not NIL:
                    self.draw_square(i, j, self.board[i][j])

    def draw_score(self):
        ''' displays the score and difficulty at top of screen'''
        # score
        surf = self.font.render("Score: %s" %self.score, True, TEXT_COLOR)
        self.display.blit(surf, (80, 140))

        # difficulty
        surf = self.font.render("Difficulty: %s" %self.difficulty, True, TEXT_COLOR)
        self.display.blit(surf, (80, 180))

    def draw_piece(self, piece, disp_x = None, disp_y = None):
        ''' draws each piece on board '''
        shape = PIECES[piece.shape][piece.rotation]
        if disp_x is None and disp_y is None:
            disp_x, disp_y = self.get_display_coords(piece.x, piece.y)
        
        # draws piece
        for i in range(TEMPLATE_W):
            for j in range(TEMPLATE_H):
                if shape[j][i] is not NIL:
                    self.draw_square(None, None, piece.color, disp_x + (i * SQ_SIZE), disp_y + (j * SQ_SIZE))
    
    def draw_next(self, piece):
        ''' shows the next piece to drop (though you probably won't look at it) '''
        surf = self.font.render("Next Piece:", True, TEXT_COLOR)
        self.display.blit(surf, (WIN_W - 160, 140))
        self.draw_piece(piece, disp_x = WIN_W - 150, disp_y = 170)

    def play(self):
        ''' main game loop'''
        self.board = self.get_board()
        down_time = time.time()
        sideway_time = time.time()
        fall_time = time.time()
        
        # direction moving in
        down = False
        left = False
        right = False        

        game_over = False

        # get current and upcoming pieces
        curr_piece = self.get_piece()
        next_piece = self.get_piece()

        while not game_over: # game loop
            if curr_piece is None:
                curr_piece = next_piece
                next_piece = self.get_piece()
                fall_time = time.time()
    
            if not self.is_free(curr_piece):
                game_over = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYUP:
                    if(event.key == K_p): # pause
                        self.display.fill(BACKGROUND)
                        pygame.mixer.music.pause()
                        self.display_text("GAME PAUSED")
                        pygame.mixer.music.unpause()
                        fall_time = down_time = sideway_time = time.time()
                    # press r changes music
                    elif(event.key == K_r):
                        self.music()
                    # stops going in that direction
                    elif (event.key == K_LEFT or event.key == K_a):
                        left = False
                    elif (event.key == K_RIGHT or event.key == K_d):
                        right = False
                    elif (event.key == K_DOWN or event.key == K_s):
                        down = False

                elif event.type == KEYDOWN:
                    # change direction (left and right)
                    if (event.key == K_LEFT or event.key == K_a):
                        if self.is_free(curr_piece, x_adj = -1):
                            curr_piece.x -= 1
                        left = True
                        right = False
                        sideway_time = time.time()
                    elif (event.key == K_RIGHT or event.key == K_d):
                        if self.is_free(curr_piece, x_adj = 1):
                            curr_piece.x += 1
                        right = True
                        left = False
                        sideway_time = time.time()
                    elif (event.key == K_DOWN or event.key == K_s):
                        down = True
                        if self.is_free(curr_piece, y_adj = 1):
                            curr_piece.y += 1
                        down_time = time.time()
                    # up is rotation, move to next element in group
                    elif (event.key == K_UP or event.key == K_w):
                        temp = curr_piece.rotation
                        curr_piece.rotation = (curr_piece.rotation + 1) % len(PIECES[curr_piece.shape])
                        if not self.is_free(curr_piece):
                            curr_piece.rotation = temp
                    # e or q rotates in other direction
                    elif (event.key == K_e or event.key == K_q):
                        temp = curr_piece.rotation
                        curr_piece.rotation = (curr_piece.rotation - 1) % len(PIECES[curr_piece.shape])
                        if not self.is_free(curr_piece):
                            curr_piece.rotation = temp

                    # Space bar sends piece to bottom
                    elif (event.key == K_SPACE):
                        down = left = right = False
                        for i in range(1, BOARD_H):
                            if not self.is_free(curr_piece, y_adj = i):
                                break
                        curr_piece.y += i - 1

            # holding down the left right keys will still move block
            if (left or right) and (time.time() - sideway_time > SIDEWAY_FREQ):
                if left and self.is_free(curr_piece, x_adj = -1):
                    curr_piece.x -= 1
                elif right and self.is_free(curr_piece, x_adj = 1):
                    curr_piece.x += 1
                sideway_time = time.time()
            
            # hold down down key moves block down
            if down and (time.time() - down_time > DOWN_FREQ):
                if self.is_free(curr_piece, y_adj = 1):
                    curr_piece.y += 1
                down_time = time.time()

            # will fall regardless of input
            if time.time() - fall_time > self.speed:
                if not self.is_free(curr_piece, y_adj = 1):
                    # piece landed
                    self.add(curr_piece) # add to board
                    self.score += self.delete_full_level() 
                    self.set_difficulty()
                    curr_piece = None
                else: # piece still falling
                    curr_piece.y += 1
                    fall_time = time.time()
                    
            self.display.fill(BACKGROUND)
            self.draw_board()
            self.draw_score()
            self.draw_next(next_piece)
            if curr_piece is not None:
               self.draw_piece(curr_piece)
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game = Tetris()
    game.run()
