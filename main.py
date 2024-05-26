import pygame as pg
from OpenGL.GL import *
from OpenGL.GLUT import *

from environment import Environment
from objLoader import OBJ
from player import Player


def draw_text(x, y, text):
    font = pg.font.Font(None, 35)
    textSurface = font.render(text, True, (0, 0, 0), (255, 255, 255))
    textData = pg.image.tostring(textSurface, "RGBA", True)
    glWindowPos2d(x, y)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)


def init():
    pg.init()
    pg.mixer.init()
    display = (pg.display.Info().current_w, pg.display.Info().current_h)
    pg.display.set_mode(display, pg.DOUBLEBUF | pg.OPENGL | pg.FULLSCREEN)
    pg.display.set_caption("Racing Game")
    pg.mouse.set_visible(False)

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

    glShadeModel(GL_SMOOTH)


def render_scene(cameras, cars, trees, viewport, player_count):
    for i in range(player_count):
        glViewport(*viewport[i])
        cameras[i].apply()
        glColor3f(1, 1, 1)
        for car in cars:
            car.render()
        Environment().init_env(trees)


def menu():
    pg.init()
    display = (pg.display.Info().current_w, pg.display.Info().current_h)
    screen = pg.display.set_mode(display, pg.FULLSCREEN)  # Add the FULLSCREEN flag
    pg.display.set_caption("Racing Game Menu")
    font = pg.font.Font(None, 74)
    single_text = font.render('Single Player', True, (255, 255, 255))
    multi_text = font.render('Multiplayer', True, (255, 255, 255))

    single_rect = single_text.get_rect(
        center=(display[0] // 2, single_text.get_rect().height // 2 + display[1] // 2 - 50))
    multi_rect = multi_text.get_rect(
        center=(display[0] // 2, single_text.get_rect().height // 2 + display[1] // 2 + 50))

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
    mode = menu()
    init()
    width = int(pg.display.Info().current_w)
    height = int(pg.display.Info().current_h)
    viewports = {
        'single': [[0, 0, width, height]],
        'multi': [[0, 0, width // 2, height], [width // 2, 0, width // 2, height]]
    }
    clock = pg.time.Clock()
    player1_bindings = {
        'forward': pg.K_w,
        'backward': pg.K_s,
        'left': pg.K_a,
        'right': pg.K_d
    }
    car = OBJ('objects/Sedan.obj', swapyz=False)
    car.rotation = [0, 180, 0]
    car.generate()
    player1 = Player(player1_bindings, car, aspect_ratio=viewports[mode][0][2] / viewports[mode][0][3])
    player1.start_sound.play()
    trees = Environment().draw_trees()
    timer = 0
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
        car2.generate()
        player2 = Player(player2_bindings, car2, aspect_ratio=viewports[mode][1][2] / viewports[mode][1][3])
        player2.start_sound.play()
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
    main()
