import pygame 
import itertools
import sys
from game_rules import constants as c
from game_rules.board import Board
import game_rules.game_logic as game
from dataclasses import dataclass


@dataclass
class Interface:
    rows: int = c.ROWS
    columns: int = c.COLUMNS
    pixels: int = c.SQUARESIZE
    width: int = c.WIDTH
    height: int = c.HEIGHT
    rad: float = c.RADIUS
    size: tuple = (width, height)
    screen: any = pygame.display.set_mode(size)
    pygame.display.set_caption("Jeux de couleur")


    def start_game(self, bd: Board) -> None:
        """Mettre en place les conditions du jeu, comme choisir game_mode et dessiner l'écran pygame."""
        pygame.init()
        self.draw_options_board()
        game_mode = self.choose_option()
        bd.print_board()	
        self.draw_board()    
        pygame.display.update()
        self.play_game(bd, game_mode)


    def play_game(self, bd: Board, game_mode: int) -> None:
        """Lancer le jeu"""
        board = bd.get_board()	
        game_over = False
        myfont = pygame.font.SysFont("Monospace", 50, bold=True)
        turns = itertools.cycle([1, 2])  
        turn = next(turns)
        
        while not game_over:
             
            for event in pygame.event.get():
                if event.type == pygame.QUIT: quit()

                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(self.screen, c.BACKGROUND_COLOR, (0,0, self.width, self.pixels-14))
                    posx = event.pos[0]
                    pygame.draw.circle(self.screen, c.PIECES_COLORS[turn], (posx, int(self.pixels/2)-7), self.rad)
                pygame.display.update()

                
                if event.type == pygame.MOUSEBUTTONDOWN:	
                    if turn == 1 or (turn == 2 and game_mode == 1):  
                        if not game.human_move(bd, self, board, turn, event): continue 
                        if game.winning_move(board, turn): 
                            game_over = True
                            break
                        turn = next(turns)

                # jogada da IA:      
                if turn != 1 and game_mode != 1: 
                    pygame.time.wait(15)
                    game_over = game.ai_move(bd, self, game_mode, board, turn)  
                    if game_over: break                                        
                    turn = next(turns)

            if game.is_game_tied(board):
                self.show_draw(myfont)
                break

        if game.winning_move(board, turn):
            self.show_winner(myfont, turn)

       
            
        pygame.time.wait(5000)


    def draw_options_board(self):
        """Dessiner le tableau des options : joueur x joueur et joueur unique"""
        self.screen.fill(c.BACKGROUND_COLOR)
        font = pygame.font.Font("./fonts/04B_30__.TTF", 60)
        text_surface = font.render("Projet IA", True, c.BUTTON_TEXT_COLOR)
        text_rect = text_surface.get_rect()
        text_rect.center = (560, 230)
        self.screen.blit(text_surface, text_rect)
        self.draw_button(self.height/2, 350, 300, 50, "Joueur x Joueur")
        self.draw_button(self.height/2, 450, 300, 50, "Joueur x IA") # Player x IA


    def choose_option(self) -> int:
        while True:
            game_mode = 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT: quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if (self.width/2 - 150) <= mouse_x <= (self.width/2 + 150) and 350 <= mouse_y <= 400:
                        print("Joueur vs Joueur choisis")
                        game_mode = 1
                    elif (self.width/2 - 150) <= mouse_x <= (self.width/2 + 150) and 450 <= mouse_y <= 500:
                        print("Joueur vs IA choisi")
                        self.draw_algorithms()
                        game_mode = 2

            pygame.display.flip()

            if game_mode == 1:
                return game_mode
            
            if game_mode == 2:
                game_mode = self.choose_ai_option()
                return game_mode


    def draw_algorithms(self):
        self.screen.fill(c.BACKGROUND_COLOR)
        self.draw_button(self.height/2, 150, 300, 50, "Debutant") 
        self.draw_button(self.height/2, 250, 300, 50, "Facile") 
        self.draw_button(self.height/2, 350, 300, 50, "Moyen") 
        self.draw_button(self.height/2, 450, 300, 50, "Difficile") 
        self.draw_button(self.height/2, 550, 300, 50, "Tres difficle") 


    def choose_ai_option(self) -> int:
        """Dessinez le tableau d'options IA pour A*, MCTS, Alpha Beta ou MCTS."""
        while True:
            game_mode = 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT: quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if (self.width / 2 - 150) <= mouse_x <= (self.width / 2 + 150) and 250 <= mouse_y <= 300:
                        print("Debutan")
                        game_mode = 2
                    elif (self.width / 2 - 150) <= mouse_x <= (self.width / 2 + 150) and 350 <= mouse_y <= 400:
                        print("Facile")
                        game_mode = 3
                    elif (self.width / 2 - 150) <= mouse_x <= (self.width / 2 + 150) and 450 <= mouse_y <= 500:
                        print("Moyen")
                        game_mode = 4
                    elif (self.width / 2 - 150) <= mouse_x <= (self.width / 2 + 150) and 550 <= mouse_y <= 600:
                        print("Difficile")
                        game_mode = 5
                    elif (self.width / 2 - 150) <= mouse_x <= (self.width / 2 + 150) and 150 <= mouse_y <= 200:
                        print("Tres difficile")
                        game_mode = 6

                pygame.display.flip()
                if game_mode != 0:
                    return game_mode


    def draw_board(self) -> None:
        """Dessiner l'affichage du plateau de jeu"""
        self.screen.fill(c.BACKGROUND_COLOR)    

        
        shadow_coordinates = (2*self.pixels-10, self.pixels-10, self.columns*self.pixels+24, self.rows*self.pixels+24)
        board_coordinates = (2*self.pixels-10, self.pixels-10, self.columns*self.pixels+20, self.rows*self.pixels+20)
        pygame.draw.rect(self.screen, c.SHADOW_COLOR, shadow_coordinates, 0, 30) 
        pygame.draw.rect(self.screen, c.BOARD_COLOR, board_coordinates, 0, 30) 

        
        for col in range(self.columns):
            for row in range(self.rows):
                center_of_circle = (int((col+5/2)*self.pixels), int((row+3/2)*self.pixels))
                pygame.draw.circle(self.screen, c.BACKGROUND_COLOR, center_of_circle, self.rad)
        pygame.display.update()     

            
    def draw_new_piece(self, row: int, col: int, piece: int) -> None:
        center_of_circle = (int(col*self.pixels+self.pixels/2), self.height-int(row*self.pixels+self.pixels/2))
        pygame.draw.circle(self.screen, c.PIECES_COLORS[piece], center_of_circle, self.rad)


    def draw_button(self, x: int, y: int, width: int, height: int, text: str) -> None:
        """Dessiner les boutons d'option"""
        pygame.draw.rect(self.screen, c.SHADOW_COLOR, (x, y, width, height), 0, 30)
        font = pygame.font.Font("./fonts/Minecraft.ttf", 25)
        text_surface = font.render(text, True, c.BUTTON_TEXT_COLOR)
        text_rect = text_surface.get_rect()
        text_rect.center = (x + width / 2, y + height / 2)
        self.screen.blit(text_surface, text_rect)


    def show_winner(self, myfont: any, turn: int) -> None:
        """Print  gagnant"""
        label = myfont.render("Joueur " + str(turn) +" a gagne!", turn, c.PIECES_COLORS[turn])
        self.screen.blit(label, (350,15))
        pygame.display.update()


    def show_draw(self, myfont: any) -> None:
        """Print l'eglite du jeu"""
        label = myfont.render("Egalite!", True, c.BOARD_COLOR)
        self.screen.blit(label, (400,15))
        pygame.display.update()


    def quit() -> None:
        pygame.quit()
        sys.exit()

