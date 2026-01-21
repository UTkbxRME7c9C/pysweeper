import ps
import os
import pygame
import sys

WHITE = (255,255,255)
BLACK = (0,0,0)
    
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
    
def import_images():
    image_names = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "boom", "flag", "unchecked"]
    image_paths = [f"img/{name}.png" for name in image_names]
    return [pygame.image.load(resource_path(path)) for path in image_paths]


def main_pygame():
    pygame.init()
    screen = pygame.display.set_mode((600,600))
    pygame.display.set_caption("PySweeper")
    clock = pygame.time.Clock()
    font = pygame.font.Font(resource_path("font.ttf"), 40)
    #0-8
    #9 = bomb
    #10 = flag
    #11 = unchecked
    images = import_images()
    #0 = main menu
    #1 = game start, waiting for first click
    #2 = game continue
    #3 = game over
    #4 = game win
    gamestate = 0
    game = None
    # board sizes
    lboardsize = 0 # length of actual board, 600 *squaresize 
    wboardsize = 0 # width of actual board, 600 *squaresize
    lboardstart = 0 # length where board starts, 600 - lboardsize / 2
    wboardstart = 0 # width where board starts, 600 - wboardsize / 2
    squaresize = 0 # size of each square, 600 / biggest side
    
    while True:
        clock.tick(60)
        screen.fill((90, 90, 90))
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # lmb
                    if (gamestate == 0):
                        if (event.pos[0] > 200 and event.pos[0] < 400 and event.pos[1] > 250 and event.pos[1] < 550):
                            gamestate = 1 
                            if (event.pos[1] > 250 and event.pos[1] < 350):
                                game = ps.sweeper(8,8,10)
                            elif (event.pos[1] > 350 and event.pos[1] < 450):
                                game = ps.sweeper(18,16,40)
                            elif (event.pos[1] > 450 and event.pos[1] < 550):
                                game = ps.sweeper(18,30,99)
                            squaresize = 600 / (game.length if game.length > game.width else game.width)
                            lboardsize = game.length * squaresize
                            wboardsize = game.width * squaresize
                            lboardstart = (600 - lboardsize) / 2
                            wboardstart = (600 - wboardsize) / 2
                            for i in range(12):
                                images[i] = pygame.transform.scale(images[i], (squaresize,squaresize))
                    elif (gamestate == 1):
                        if (event.pos[0] > wboardstart and event.pos[0] < wboardstart + wboardsize and event.pos[1] > lboardstart and event.pos[1] < lboardstart + lboardsize):
                            lboard = int((event.pos[1] - lboardstart)//(lboardsize/game.length))
                            wboard = int((event.pos[0] - wboardstart)//(wboardsize/game.width))
                            game.generate_mines(lboard,wboard)
                            gamestate = 2
                    elif (gamestate == 2):
                        if (event.pos[0] > wboardstart and event.pos[0] < wboardstart + wboardsize and event.pos[1] > lboardstart and event.pos[1] < lboardstart + lboardsize):
                            lboard = int((event.pos[1] - lboardstart)//(lboardsize/game.length))
                            wboard = int((event.pos[0] - wboardstart)//(wboardsize/game.width))
                            if (game.checked[lboard][wboard] == 0):
                                if (game.mines[lboard][wboard] == -1):
                                    gamestate = 3
                                else:
                                    game.set_checked(lboard,wboard)
                                    if (game.check_win()):
                                        gamestate = 4
                elif event.button == 3:  # rmb
                    if (gamestate == 2):
                        if (event.pos[0] > wboardstart and event.pos[0] < wboardstart + wboardsize
                            and event.pos[1] > lboardstart and event.pos[1] < lboardstart + lboardsize):
                            lboard = int((event.pos[1] - lboardstart)//(lboardsize/game.length))
                            wboard = int((event.pos[0] - wboardstart)//(wboardsize/game.width))
                            game.set_flag(lboard,wboard)
            elif event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_ESCAPE):
                    if (gamestate == 0):
                        pygame.quit()
                        sys.exit()
                    else:
                        gamestate = 0
                        images = import_images() #image quality dies without this
        if (gamestate == 0):
            tv = ["PySweeper", "Easy","Medium","Hard"]
            th = [100,300,400,500]
            for i in range(4):
                text = font.render(tv[i], True, WHITE)
                text_rect = text.get_rect(center=(300, th[i]))
                screen.blit(text, text_rect)
        elif (gamestate == 1 or gamestate == 2):        
            for i in range(game.length):
                for j in range(game.width):
                    rect = pygame.Rect(
                        wboardstart + (j * squaresize),
                        lboardstart + (i * squaresize),
                        squaresize,
                        squaresize,
                    )
                    if game.checked[i][j] == 0:
                        screen.blit(images[11], rect)
                    elif game.checked[i][j] == 1:
                        screen.blit(images[game.mines[i][j]], rect)
                    elif game.checked[i][j] == 2:
                        screen.blit(images[10], rect)
        else:
            for i in range(game.length):
                for j in range(game.width):
                    rect = pygame.Rect(
                        wboardstart + (j * squaresize),
                        lboardstart + (i * squaresize),
                        squaresize,
                        squaresize,
                    )
                    if game.mines[i][j] == -1:
                        if gamestate == 3:
                            screen.blit(images[9], rect)
                        elif gamestate == 4 and game.checked[i][j] == 2:
                            screen.blit(images[10], rect)
                        else:
                            screen.blit(images[11], rect)
                    else:
                        screen.blit(images[game.mines[i][j]], rect)
            if gamestate == 3:
                text = font.render("You lose!", True, (255,0,0))
            else:
                text = font.render("You win!", True, (0,255,0))
            text_rect = text.get_rect(center=(300, 300))
            screen.blit(text, text_rect)
                    
        pygame.display.update()
    
if __name__ == "__main__":
    main_pygame()


