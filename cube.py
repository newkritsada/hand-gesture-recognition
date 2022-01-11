import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
import os

width = 1280
height = 720
windowX = 600
windowY = 300
vertices = ((-1, -1, -1), (-1, 1, -1), (-1, 1, 1), (-1, -1, 1),
            (1, -1, -1), (1, 1, -1), (1, 1, 1), (1, -1, 1))
edges = ((0, 1), (0, 3), (0, 4), (1, 2), (1, 5), (2, 3),
         (2, 6), (3, 7), (4, 5), (4, 7), (5, 6), (6, 7))
faces = ((0, 1, 2, 3), (4,  5, 6, 7), (0, 4, 7, 3),
         (1, 5, 6, 2), (2, 6, 7, 3), (1, 5, 4, 0))

# dbclock = pygame.time.Clock()
# DOUBLECLICKTIME = 500

STOP = False

scaleX = 1
scaleY = 1
scaleZ = 1
ZOOM = False

rotateX = 0
rotateY = 0
rotateZ = 0
ROTATE = False


def Cube():  # สร้างMODEL 3d ค่าเอาจากที่ประกาศข้างบน
    glBegin(GL_QUADS)
    for face in faces:
        for vertex in face:
            glColor3fv((0, 0, 1))
            glVertex3fv(vertices[vertex])
    glEnd()

    glBegin(GL_LINES)
    glColor3fv((1, 1, 1))
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()


def Zoom(x=0, y=0, z=0):
    global scaleX, scaleY, scaleZ
    global ZOOM
    ZOOM = True
    scaleX = x
    scaleY = y
    scaleZ = z


def Rotate(x=0, y=0, z=0):
    global rotateX, rotateY, rotateZ
    global ROTATE
    ROTATE = True
    rotateX = x
    rotateY = y
    rotateZ = z


def Stop():
    global STOP
    STOP = True


def Main():
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (windowX, windowY)
    pygame.init()
    screen = (width, height)
    glutInit()
    display = pygame.display.set_mode(screen, DOUBLEBUF | OPENGL)
    glutInitWindowSize(640, 480)
    glutInitWindowPosition(10, 10)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (screen[0] / screen[1]), 0.1, 500)

    glMatrixMode(GL_MODELVIEW)
    modelMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)

    while True:

        glPushMatrix()
        glLoadIdentity()
        if STOP:
            break

        if ZOOM:
            glScalef(scaleX, scaleY, scaleZ)

        if ROTATE:
            glRotatef(rotateY, 1, 0, 0)
            glRotatef(rotateX, 0, 1, 0)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMultMatrixf(modelMatrix)
        modelMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)

        glLoadIdentity()
        glTranslatef(0, 0, -5)
        glMultMatrixf(modelMatrix)

        Cube()

        glPopMatrix()
        pygame.display.flip()
        pygame.time.wait(10)


# Main()
