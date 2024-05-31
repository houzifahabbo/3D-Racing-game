import pygame as pg
from OpenGL.GL import *
from OpenGL.GLUT import *

from environment import Environment
from objLoader import OBJ
from player import Player


def draw_text(x, y, text):
    """
    Function to draw text on an OpenGL display using Pygame and PyOpenGL.

    Parameters:
    x (int): The x-coordinate on the screen where the text will be drawn.
    y (int): The y-coordinate on the screen where the text will be drawn.
    text (str): The text to be rendered.

    Returns:
    None
    """

    # Create a Pygame font object with the default font and a size of 35
    font = pg.font.Font(None, 35)

    # Render the text onto a Pygame surface with anti-aliasing enabled
    # The text color is black (0, 0, 0) and the background color is white (255, 255, 255)
    textSurface = font.render(text, True, (0, 0, 0), (255, 255, 255))

    # Convert the Pygame surface to pixel data for OpenGL
    textData = pg.image.tostring(textSurface, "RGBA", True)

    # Set the position for rasterizing 2D shapes in OpenGL
    glWindowPos2d(x, y)

    # Draw the pixel data onto the screen
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)


def init():
    """
    Initializes the Pygame and PyOpenGL environments for the game.

    This function initializes Pygame and its mixer module, sets up the display with the current screen resolution and
    necessary flags, sets the window title, hides the mouse cursor, sets up the OpenGL environment with necessary settings
    and two light sources, and sets the shading model to smooth.

    Parameters:
    None

    Returns:
    None
    """

    # Initialize Pygame and its mixer module
    pg.init()
    pg.mixer.init()

    # Get the current screen resolution and set up the display
    display = (pg.display.Info().current_w, pg.display.Info().current_h)
    pg.display.set_mode(display, pg.DOUBLEBUF | pg.OPENGL | pg.FULLSCREEN)

    # Set the window title and hide the mouse cursor
    pg.display.set_caption("Racing Game")
    pg.mouse.set_visible(False)

    # Set the clear color and enable necessary OpenGL settings
    glClearColor(0.53, 0.81, 0.98, 1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)

    # Setup light 0
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, (10, 10, 10, 1.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.8, 0.8, 0.8, 1.0))
    glLightfv(GL_LIGHT0, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))

    # Setup light 1 for additional lighting
    glEnable(GL_LIGHT1)
    glLightfv(GL_LIGHT1, GL_POSITION, (-10, 10, -10, 1.0))
    glLightfv(GL_LIGHT1, GL_AMBIENT, (0.1, 0.1, 0.1, 1.0))
    glLightfv(GL_LIGHT1, GL_DIFFUSE, (0.6, 0.6, 0.6, 1.0))
    glLightfv(GL_LIGHT1, GL_SPECULAR, (0.8, 0.8, 0.8, 1.0))

    # Set the shading model to smooth
    glShadeModel(GL_SMOOTH)


def render_scene(cameras, cars, trees, viewport, player_count):
    """
    Renders the game scene for each player.

    This function sets up the view for each player's screen, and renders the cars and the environment onto the screen.

    Parameters:
    cameras (list): A list of camera objects for each player.
    cars (list): A list of car objects to be rendered.
    trees (list): A list of tree objects to be rendered.
    viewport (list): A list of viewport dimensions for each player's screen.
    player_count (int): The number of players in the game.

    Returns:
    None
    """
    # Set up the view for each player's screen
    for i in range(player_count):
        glViewport(*viewport[i])
        cameras[i].apply()

        # Set the color for subsequent drawing operations
        glColor3f(1, 1, 1)

        # Render each car
        for car in cars:
            car.render()

        # Render the environment
        Environment().init_env(trees)


def menu():
    """
    Initializes the Pygame environment and displays the game menu.

    This function initializes Pygame, sets up the display with the current screen resolution and necessary flags,
    sets the window title, and renders the 'Single Player' and 'Multiplayer' options on the screen.
    It then enters a loop where it waits for the user to click on one of these options, and returns the selected option.

    Parameters:
    None

    Returns:
    str: The selected game mode ('single' or 'multi').
    """

    # Initialize Pygame
    pg.init()

    # Get the current screen resolution and set up the display
    display = (pg.display.Info().current_w, pg.display.Info().current_h)
    screen = pg.display.set_mode(display, pg.FULLSCREEN)  # Add the FULLSCREEN flag

    # Set the window title
    pg.display.set_caption("Racing Game Menu")

    # Create a Pygame font object and render the 'Single Player' and 'Multiplayer' options
    font = pg.font.Font(None, 74)
    single_text = font.render('Single Player', True, (255, 255, 255))
    multi_text = font.render('Multiplayer', True, (255, 255, 255))

    # Get the rectangles for positioning the options on the screen
    single_rect = single_text.get_rect(
        center=(display[0] // 2, single_text.get_rect().height // 2 + display[1] // 2 - 50))
    multi_rect = multi_text.get_rect(
        center=(display[0] // 2, single_text.get_rect().height // 2 + display[1] // 2 + 50))

    # Enter a loop where it waits for the user to click on one of the options
    while True:
        screen.fill((0, 0, 0))
        screen.blit(single_text, single_rect)
        screen.blit(multi_text, multi_rect)

        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if single_rect.collidepoint(event.pos):
                    return 'single'
                elif multi_rect.collidepoint(event.pos):
                    return 'multi'
        pg.display.flip()


def main():
    """
    The main function of the game.

    This function calls the menu function to get the game mode, initializes the Pygame and PyOpenGL environments,
    sets up the viewport based on the game mode, creates the player(s) and the car(s), and enters a game loop where it
    updates the game state and renders the game scene.

    Parameters:
    None

    Returns:
    None
    """

    # Call the menu function to get the game mode
    mode = menu()

    # Initialize the Pygame and PyOpenGL environments
    init()

    # Get the current screen resolution
    width = int(pg.display.Info().current_w)
    height = int(pg.display.Info().current_h)

    # Set up the viewport based on the game mode
    viewports = {
        'single': [[0, 0, width, height]],
        'multi': [[0, 0, width // 2, height], [width // 2, 0, width // 2, height]]
    }

    # Create a Pygame clock object
    clock = pg.time.Clock()

    # Define the key bindings for player 1
    player1_bindings = {
        'forward': pg.K_w,
        'backward': pg.K_s,
        'left': pg.K_a,
        'right': pg.K_d
    }

    # Load the car model and create player 1
    car = OBJ('objects/Sedan.obj', swapyz=False)
    car.rotation = [0, 180, 0]
    player1 = Player(player1_bindings, car, aspect_ratio=viewports[mode][0][2] / viewports[mode][0][3])
    player1.start_sound.play()

    # Draw the trees
    trees = Environment().draw_trees()

    # Initialize the timer
    timer = 0

    # Enter the game loop
    if mode == 'single':
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    car.free()
                    for tree in trees:
                        tree.free()
                    pg.quit()
                    sys.exit()
            timer += clock.get_time()

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            player1.movement(trees)
            player1.update_lap_count(timer)

            render_scene([player1.camera], [car], trees, viewports[mode], 1)
            draw_text(10, 10, f"Player 1 Lap: {player1.lap_count}")
            draw_text(width // 2 - 70, height - 50, f"Timer: {timer // 60000}:{timer // 1000 % 60}:{timer % 1000}")

            pg.display.flip()
            clock.tick(60)
            pg.time.wait(10)
    else:
        # Define the key bindings for player 2 and create player 2
        player2_bindings = {
            'forward': pg.K_UP,
            'backward': pg.K_DOWN,
            'left': pg.K_LEFT,
            'right': pg.K_RIGHT
        }
        car.position = [-2, 0, 0]
        car2 = OBJ('objects/Sedan.obj', swapyz=False)
        car2.rotation = [0, 180, 0]
        car2.position = [2, 0, 0]
        player2 = Player(player2_bindings, car2, aspect_ratio=viewports[mode][1][2] / viewports[mode][1][3])
        player2.start_sound.play()

        # Enter the game loop for multiplayer mode
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    car.free()
                    car2.free()
                    for tree in trees:
                        tree.free()
                    pg.quit()
                    sys.exit()
            timer += clock.get_time()

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            player1.movement(trees)
            player1.update_lap_count(timer)
            player2.movement(trees)
            player2.update_lap_count(timer)
            player2.check_rank(player1)

            render_scene([player1.camera, player2.camera], [car, car2], trees, viewports[mode], 2)
            draw_text(10, 10, f"Player 1 Lap: {player1.lap_count} {player1.rank}")
            draw_text(width // 2 + 10, 10, f"Player 2 Lap: {player2.lap_count} {player2.rank}")
            draw_text(width // 2 - 70, height - 50, f"Timer: {timer // 60000}:{timer // 1000 % 60}:{timer % 1000}")

            pg.display.flip()
            clock.tick(60)
            pg.time.wait(10)


if __name__ == "__main__":
    """
    The entry point of the script.

    This line checks if this script is being run directly or being imported by another script. 
    If it is being run directly, it calls the main function to start the game.

    Parameters:
    None

    Returns:
    None
    """

    main()
