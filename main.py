import pygame
import asyncio

class ChessGame:
    def __init__(self):
        pygame.init()

        self.Width = 900
        self.Height = 750

        self.screen = pygame.display.set_mode([self.Width,self.Height])
        pygame.display.set_caption('Two Player Chess Game !!!')
        self.font=pygame.font.Font('freesansbold.ttf',20)
        self.small_font = pygame.font.Font('freesansbold.ttf', 30)
        self.medium_font = pygame.font.Font('freesansbold.ttf', 40)
        self.big_font=pygame.font.Font('freesansbold.ttf',50)
        self.timer=pygame.time.Clock()
        self.fps = 60

        # game variable and images
        self.white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                        'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
        self.white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                        (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
        self.black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                        'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
        self.black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                        (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
        self.captured_pieces_white = []
        self.captured_pieces_black = []

        self.turn_step = 0
        self.selection = 100
        self.valid_moves = []
        self.black_options = self.check_options(self.black_pieces, self.black_locations, 'black')
        self.white_options = self.check_options(self.white_pieces,self.white_locations,'white')

        self.selected_white_piece = None
        self.selected_white_piece_original_pos = None
        self.selected_black_piece = None
        self.selected_black_piece_original_pos = None

        self.load_images()
    def load_images(self):
        # Load the game piece images
        self.black_queen=pygame.image.load('assets/images/black queen.png')
        self.black_queen = pygame.transform.scale(self.black_queen, (60, 60))
        self.black_queen_small = pygame.transform.scale(self.black_queen, (40, 40))
        self.black_king = pygame.image.load('assets/images/black king.png')
        self.black_king = pygame.transform.scale(self.black_king, (60, 60))
        self.black_king_small = pygame.transform.scale(self.black_king, (40, 40))
        self.black_rook = pygame.image.load('assets/images/black rook.png')
        self.black_rook = pygame.transform.scale(self.black_rook, (60, 60))
        self.black_rook_small = pygame.transform.scale(self.black_rook, (40, 40))
        self.black_bishop = pygame.image.load('assets/images/black bishop.png')
        self.black_bishop = pygame.transform.scale(self.black_bishop, (60, 60))
        self.black_bishop_small = pygame.transform.scale(self.black_bishop, (40, 40))
        self.black_knight = pygame.image.load('assets/images/black knight.png')
        self.black_knight = pygame.transform.scale(self.black_knight, (60, 60))
        self.black_knight_small = pygame.transform.scale(self.black_knight, (40, 40))
        self.black_pawn = pygame.image.load('assets/images/black pawn.png')
        self.black_pawn = pygame.transform.scale(self.black_pawn, (50, 50))
        self.black_pawn_small = pygame.transform.scale(self.black_pawn, (30, 30))
        self.white_queen = pygame.image.load('assets/images/white queen.png')
        self.white_queen = pygame.transform.scale(self.white_queen, (60, 60))
        self.white_queen_small = pygame.transform.scale(self.white_queen, (40, 40))
        self.white_king = pygame.image.load('assets/images/white king.png')
        self.white_king = pygame.transform.scale(self.white_king, (60, 60))
        self.white_king_small = pygame.transform.scale(self.white_king, (40, 40))
        self.white_rook = pygame.image.load('assets/images/white rook.png')
        self.white_rook = pygame.transform.scale(self.white_rook, (60, 60))
        self.white_rook_small = pygame.transform.scale(self.white_rook, (40, 40))
        self.white_bishop = pygame.image.load('assets/images/white bishop.png')
        self.white_bishop = pygame.transform.scale(self.white_bishop, (60, 60))
        self.white_bishop_small = pygame.transform.scale(self.white_bishop, (40, 40))
        self.white_knight = pygame.image.load('assets/images/white knight.png')
        self.white_knight = pygame.transform.scale(self.white_knight, (60, 60))
        self.white_knight_small = pygame.transform.scale(self.white_knight, (40, 40))
        self.white_pawn = pygame.image.load('assets/images/white pawn.png')
        self.white_pawn = pygame.transform.scale(self.white_pawn, (50, 50))
        self.white_pawn_small = pygame.transform.scale(self.white_pawn, (30, 30))

        self.white_images = [self.white_pawn, self.white_queen, self.white_king, self.white_knight, self.white_rook, self.white_bishop]
        self.small_white_images = [self.white_pawn_small, self.white_queen_small, self.white_king_small, self.white_knight_small,
                            self.white_rook_small, self.white_bishop_small]
        self.black_images = [self.black_pawn, self.black_queen, self.black_king, self.black_knight, self.black_rook, self.black_bishop]
        self.small_black_images = [self.black_pawn_small, self.black_queen_small, self.black_king_small, self.black_knight_small,
                            self.black_rook_small, self.black_bishop_small]

        self.piece_list = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']
        # check variables/ flashing counter
        self.counter = 0
        self.winner = ''
        self.game_over = False


## Color -> Yellow : '#F0FA79' & Brown : '#FA8D79'

# Draw main Game Board

    def draw_board(self):
        for i in range(32):
            column=i%4
            row=i//4
            if row%2==0:
                pygame.draw.rect(self.screen,'#FA8D79',[480-(column*160),row*80,80,80])
            else:
                pygame.draw.rect(self.screen,'#FA8D79',[560-(column*160),row*80,80,80])
            pygame.draw.rect(self.screen,'white',[0,640,self.Width,160])
            pygame.draw.rect(self.screen,'#7D7D7D',[0,640,self.Width,160],2)
            pygame.draw.rect(self.screen,'#7D7D7D',[640,0,260,self.Height],2)
            status_text = ['Chess Game : White Turn !!!', 'Chess Game : White Turn !!!',
                        'Chess Game : Black Trun !!!', 'Chess Game : Black Turn !!!']
            self.screen.blit(self.medium_font.render(status_text[self.turn_step], True, 'black'), (20, 680))
            for i in range(9):
                pygame.draw.line(self.screen, '#7D7D7D', (0, 80 * i), (640, 80 * i), 2)
                pygame.draw.line(self.screen, '#7D7D7D', (80 * i, 0), (80 * i, 640), 2)
            self.screen.blit(self.small_font.render('FORFEIT', True, 'black'), (710, 680))

# Draw pieces onto board
    def draw_pieces(self):
        for i in range(len(self.white_pieces)):
            index = self.piece_list.index(self.white_pieces[i])
            if index is not None:
                if self.white_pieces[i] == 'pawn':
                    self.screen.blit(self.white_pawn, (self.white_locations[i][0] * 80 + 16, self.white_locations[i][1] * 80 + 20))
                else:
                    self.screen.blit(self.white_images[index], (self.white_locations[i][0] * 80 + 10, self.white_locations[i][1] * 80 + 10))
                if self.turn_step < 2:
                    if self.selection == i:
                        pygame.draw.rect(self.screen, '#1477D5', [self.white_locations[i][0] * 80 + 1, self.white_locations[i][1] * 80 + 1,
                                                        80, 80], 3)

        for i in range(len(self.black_pieces)):
            index = self.piece_list.index(self.black_pieces[i])
            if index is not None:
                if self.black_pieces[i] == 'pawn':
                    self.screen.blit(self.black_pawn, (self.black_locations[i][0] * 80 + 16, self.black_locations[i][1] * 80 + 20))
                else:
                    self.screen.blit(self.black_images[index], (self.black_locations[i][0] * 80 + 10, self.black_locations[i][1] * 80 + 10))
                if self.turn_step >= 2:
                    if self.selection == i:
                        pygame.draw.rect(self.screen, 'blue', [self.black_locations[i][0] * 80 + 1, self.black_locations[i][1] * 80 + 1,
                                                        80, 80], 2)

        if self.selected_white_piece is not None:
            x, y = self.white_locations[self.selection]
            piece_index = self.piece_list.index(self.selected_white_piece)
            piece_image = self.white_images[piece_index]
            


        if self.selected_black_piece is not None:
            x, y = self.black_locations[self.selection]
            piece_index = self.piece_list.index(self.selected_black_piece)
            piece_image = self.black_images[piece_index] 
        

# Function to check all pieces of valid options on board
    def check_options(self,pieces,locations,turn): 
        moves_list = []
        all_moves_list = []
        for i in range((len(pieces))):
            location = locations[i]
            piece = pieces[i]
            if piece == 'pawn':
                moves_list = self.check_pawn(location, turn)
            elif piece == 'rook':
                moves_list = self.check_rook(location, turn)
            elif piece == 'knight':
                moves_list = self.check_knight(location, turn)
            elif piece == 'bishop':
                moves_list = self.check_bishop(location, turn)
            elif piece == 'queen':
                moves_list = self.check_queen(location, turn)
            elif piece == 'king':
                moves_list = self.check_king(location, turn)
            all_moves_list.append(moves_list)
        return all_moves_list

# Function to check valid pawn moves
    def check_pawn(self,position,color):
        moves_list = []
        if color == 'white':
            if (position[0], position[1] + 1) not in self.white_locations and \
                    (position[0], position[1] + 1) not in self.black_locations and position[1] < 7:
                moves_list.append((position[0], position[1] + 1))
            if (position[0], position[1] + 2) not in self.white_locations and \
                    (position[0], position[1] + 2) not in self.black_locations and position[1] == 1:
                moves_list.append((position[0], position[1] + 2))
            if (position[0] + 1, position[1] + 1) in self.black_locations:
                moves_list.append((position[0] + 1, position[1] + 1))
            if (position[0] - 1, position[1] + 1) in self.black_locations:
                moves_list.append((position[0] - 1, position[1] + 1))
        else:
            if (position[0], position[1] - 1) not in self.white_locations and \
                    (position[0], position[1] - 1) not in self.black_locations and position[1] > 0:
                moves_list.append((position[0], position[1] - 1))
            if (position[0], position[1] - 2) not in self.white_locations and \
                    (position[0], position[1] - 2) not in self.black_locations and position[1] == 6:
                moves_list.append((position[0], position[1] - 2))
            if (position[0] + 1, position[1] - 1) in self.white_locations:
                moves_list.append((position[0] + 1, position[1] - 1))
            if (position[0] - 1, position[1] - 1) in self.white_locations:
                moves_list.append((position[0] - 1, position[1] - 1))
        return moves_list 

# Function to check valid rook moves
    def check_rook(self,position,color):
        moves_list = []
        if color == 'white':
            enemies_list = self.black_locations
            friends_list = self.white_locations
        else:
            enemies_list = self.white_locations
            friends_list = self.black_locations
            
        for i in range(4):  
            path = True
            chain = 1
            if i == 0:
                x = 0
                y = 1
            elif i == 1:
                x = 0
                y = -1
            elif i == 2:
                x = 1
                y = 0
            else:
                x = -1
                y = 0
            while path:
                if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                        0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                    moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))
                    if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                        path = False
                    chain += 1
                else:
                    path = False
        return moves_list

# Function to check valid knight moves
    def check_knight(self,position,color):
        moves_list = []
        if color == 'white':
            friends_list = self.white_locations
        else:
            friends_list = self.black_locations

        # 8 squares to check for knights, 
        # they can go two squares in one direction and one in another  
        targets = [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
        for i in range(8):
            target = (position[0] + targets[i][0], position[1] + targets[i][1])
            if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
                moves_list.append(target)
        return moves_list

    # Function to check valid bishop moves
    def check_bishop(self,position,color):
        moves_list = []
        if color == 'white':
            enemies_list = self.black_locations
            friends_list = self.white_locations
        else:
            friends_list = self.black_locations
            enemies_list = self.white_locations
        for i in range(4):  
            path = True
            chain = 1
            if i == 0:
                x = 1
                y = -1
            elif i == 1:
                x = -1
                y = -1
            elif i == 2:
                x = 1
                y = 1
            else:
                x = -1
                y = 1
            while path:
                if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                        0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                    moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))
                    if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                        path = False
                    chain += 1
                else:
                    path = False
        return moves_list

    # Function to check valid queen moves
    def check_queen(self,position,color):
        moves_list = self.check_bishop(position, color)
        second_list = self.check_rook(position, color)
        for i in range(len(second_list)):
            moves_list.append(second_list[i])
        return moves_list

# Function to check valid king moves
    def check_king(self,position,color):
        moves_list = []
        if color == 'white':
            friends_list = self.white_locations
        else:
            friends_list = self.black_locations
        # 8 squares to check for kings, 
        # they can go one square any direction
        targets = [(1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1)]
        for i in range(8):
            target = (position[0] + targets[i][0], position[1] + targets[i][1])
            if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
                moves_list.append(target)
        return moves_list

    # Function to check for valid moves for selected piece
    def check_valid_moves(self):
        if self.turn_step < 2:
            options_list = self.white_options
        else:
            options_list = self.black_options
        valid_options = options_list[self.selection]
        return valid_options 

    # Function to draw a valid moves on Screen
    def draw_valid(self,moves):
        if self.turn_step < 2:
            color = 'red'
        else:
            color = 'blue'
        for i in range(len(moves)):
            pygame.draw.circle(self.screen, color, (moves[i][0] * 80 + 40, moves[i][1] * 80 + 40), 5)

    # Function to draw captured pieces onto the screen
    def draw_captured(self):
        for i in range(len(self.captured_pieces_white)):
            captured_piece = self.captured_pieces_white[i]
            index = self.piece_list.index(captured_piece)
            self.screen.blit(self.small_black_images[index], (640, 5 + 42 * i))
        for i in range(len(self.captured_pieces_black)):
            captured_piece = self.captured_pieces_black[i]
            index = self.piece_list.index(captured_piece)
            self.screen.blit(self.small_white_images[index], (760, 5 + 42 * i))

# Function to check flashing square on King for Check or Check-Mate
    def draw_check(self):
        if self.turn_step < 2:
            if 'king' in self.white_pieces:
                king_index = self.white_pieces.index('king')
                king_location = self.white_locations[king_index]
                for i in range(len(self.black_options)):
                    if king_location in self.black_options[i]:
                        if self.counter < 15:
                            pygame.draw.rect(self.screen, 'dark red', [self.white_locations[king_index][0] * 80 + 1,
                                                                self.white_locations[king_index][1] * 80 + 1, 80, 80], 8)
        else:
            if 'king' in self.black_pieces:
                king_index = self.black_pieces.index('king')
                king_location = self.black_locations[king_index]
                for i in range(len(self.white_options)):
                    if king_location in self.white_options[i]:
                        if self.counter < 15:
                            pygame.draw.rect(self.screen, 'dark blue', [self.black_locations[king_index][0] * 80 + 1,
                                                                self.black_locations[king_index][1] * 80 + 1, 80, 80], 8)

# Function to draw pop up on Game Over
    def draw_game_over(self):
        pygame.draw.rect(self.screen, 'black', [280, 280, 350, 70])
        self.screen.blit(self.font.render(f'{self.winner} won the game!!!', True, 'white'), (290, 290))
        self.screen.blit(self.font.render(f'Press ENTER to Restart!', True, 'white'), (290, 320))
    async def run(self):
        run = True
        while run:
            self.timer.tick(self.fps)
            if self.counter < 30:
                self.counter += 1
            else:
                self.counter = 0
            self.screen.fill('#F0FA79')
            self.draw_board()
            self.draw_pieces()
            self.draw_captured()
            self.draw_check()
            if self.selection!=100:
                self.valid_moves=self.check_valid_moves()
                self.draw_valid(self.valid_moves)
            # event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run=False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x_coord = event.pos[0] // 80
                    y_coord = event.pos[1] // 80
                    click_coords=(x_coord,y_coord)
                    if self.turn_step <= 1:
                        if click_coords == (8, 8) or click_coords == (9, 8):
                            self.winner = 'Black'
                        elif click_coords in self.white_locations:
                            self.selection = self.white_locations.index(click_coords)
                            if self.turn_step == 0:
                                self.turn_step=1
                                self.selected_white_piece = self.white_pieces[self.selection]
                                self.selected_white_piece_original_pos = self.white_locations[self.selection]
                        else:
                            continue
                    elif self.turn_step >= 2:
                        if click_coords == (8, 8) or click_coords == (9, 8):
                            self.winner = 'White'
                        elif click_coords in self.black_locations:
                            self.selection = self.black_locations.index(click_coords)
                            if self.turn_step == 2:
                                self.selected_black_piece = self.black_pieces[self.selection]
                                self.selected_black_piece_original_pos = self.black_locations[self.selection]
                        else:
                            continue
                elif event.type == pygame.MOUSEMOTION:
                    x_coord, y_coord = event.pos
                    x_coord //= 80
                    y_coord //= 80
                    if self.selected_white_piece is not None and self.turn_step in [0, 1]:
                        self.white_locations[self.selection] = (x_coord, y_coord)
                    elif self.selected_black_piece is not None and self.turn_step in [2, 3]:
                        self.black_locations[self.selection] = (x_coord, y_coord)
                # Modify the MOUSEBUTTONUP part to handle placement and validation for the selected piece.
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    x_coord, y_coord = event.pos
                    x_coord //= 80
                    y_coord //= 80
                    if self.turn_step <= 1:
                        if (x_coord,y_coord) == (8,8) or (x_coord,y_coord) == (9,8):
                            self.winner='Black'
                        if (x_coord, y_coord) in self.valid_moves and self.selection != 100:
                            self.white_locations[self.selection] = (x_coord, y_coord)
                            if (x_coord, y_coord) in self.black_locations:
                                black_piece = self.black_locations.index((x_coord, y_coord))
                                self.captured_pieces_white.append(self.black_pieces[black_piece])
                                if self.black_pieces[black_piece] == 'king':
                                    self.winner = 'White'
                                self.black_pieces.pop(black_piece)
                                self.black_locations.pop(black_piece)
                            self.black_options = self.check_options(self.black_pieces, self.black_locations, 'black')
                            self.white_options = self.check_options(self.white_pieces, self.white_locations, 'white')
                            self.turn_step = 2
                            self.selection=100
                            self.valid_moves=[]
                        elif 0 <= self.selection < len(self.white_locations):
                            if self.selected_white_piece is not None:
                                self.white_locations[self.selection] = self.selected_white_piece_original_pos
                        self.selected_white_piece = None
                        self.selected_white_piece_original_pos = None
                    elif self.turn_step >= 2:
                        if (x_coord,y_coord) == (8,8) or (x_coord,y_coord) == (9,8):
                            self.winner='White'
                        if (x_coord, y_coord) in self.valid_moves and self.selection != 100:
                            self.black_locations[self.selection] = (x_coord, y_coord)
                            if (x_coord, y_coord) in self.white_locations:
                                white_piece = self.white_locations.index((x_coord, y_coord))
                                self.captured_pieces_black.append(self.white_pieces[white_piece])
                                if self.white_pieces[white_piece] == 'king':
                                    self.winner = 'Black'
                                self.white_pieces.pop(white_piece)
                                self.white_locations.pop(white_piece)
                            
                            self.black_options = self.check_options(self.black_pieces, self.black_locations, 'black')
                            self.white_options = self.check_options(self.white_pieces, self.white_locations, 'white')
                            self.turn_step=0
                            self.selection=100
                            self.valid_moves=[]
                        elif 0 <= self.selection < len(self.black_locations):
                            if self.selected_black_piece is not None:
                                self.black_locations[self.selection] = self.selected_black_piece_original_pos
                        self.selected_black_piece = None
                        self.selected_black_piece_original_pos = None


                if event.type == pygame.KEYDOWN and self.game_over:
                    if event.key == pygame.K_RETURN:
                        self.game_over = False
                        self.winner = ''
                        self.white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                        'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                        self.white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                                        (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
                        self.black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                        'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                        self.black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                                        (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
                        self.captured_pieces_white = []
                        self.captured_pieces_black = []
                        self.turn_step = 0
                        self.selection = 100
                        self.valid_moves = []
                        self.black_options = self.check_options(self.black_pieces, self.black_locations, 'black')
                        self.white_options = self.check_options(self.white_pieces, self.white_locations, 'white')

            if self.winner!='':
                self.game_over=True
                self.draw_game_over()
            await asyncio.sleep(0)

            pygame.display.flip()
        pygame.quit()
if __name__ == "__main__":
    chess_game = ChessGame()
    asyncio.run(chess_game.run())