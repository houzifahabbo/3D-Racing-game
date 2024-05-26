import pygame as pg
from OpenGL.GL import *
from OpenGL.GLUT import *
from objLoader import OBJ
from environment import Environment
from player import Player
from camera import Camera


def drawText(x, y, text):
    font = pg.font.Font(None, 25)
    textSurface = font.render(text, True, (0,0,0), (255,255,255))
    textData = pg.image.tostring(textSurface, "RGBA", True)
    glWindowPos2d(x, y)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)

def init():
    pg.init()
    display = (800, 600)
    pg.display.set_mode(display, pg.DOUBLEBUF | pg.OPENGL)
    pg.display.set_caption("Racing Game")

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


def render_scene(cameras, cars, trees,viewport,player_count):
    for i in range(player_count):
        glViewport(*viewport[i])
        cameras[i].apply()
        glColor3f(1, 1, 1)
        for car in cars:
            car.render()
        Environment().init_env(trees)


def main():
    init()
    clock = pg.time.Clock()
    player1_bindings = {
        'forward': pg.K_w,
        'backward': pg.K_s,
        'left': pg.K_a,
        'right': pg.K_d
    }
    player2_bindings = {
        'forward': pg.K_UP,
        'backward': pg.K_DOWN,
        'left': pg.K_LEFT,
        'right': pg.K_RIGHT
    }
    car = OBJ('car_object/Sedan.obj', swapyz=False)
    car.rotation = [0,180, 0]
    car.generate()

    car2 = OBJ('car_object/Sedan.obj', swapyz=False)
    car2.rotation = [0, 180, 0]
    car2.position = [5, 0, 0]
    car2.generate()
    player1 = Player(player1_bindings,car)
    player2 = Player(player2_bindings,car2)
    trees = Environment().draw_trees()
    timer = 0

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
        player2.movement(trees)
        render_scene([player1.camera,player2.camera], [car,car2], trees,([0, 0, 400, 600],[400, 0, 400, 600]),2)

        pg.display.flip()
        clock.tick(60)
        pg.time.wait(10)

if __name__ == "__main__":
    main()