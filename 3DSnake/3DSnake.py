import random
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

edges = (
    (0, 1),
    (2, 1),
    (2, 3),
    (2, 7),
    (6, 3),
    (6, 4),
    (6, 7),
    (5, 1),
    (5, 4),
    (5, 7),
    (0, 3),
    (0, 4)
)

surfaces = (
    (0, 1, 2, 3),
    (3, 2, 7, 6),
    (6, 7, 5, 4),
    (4, 5, 1, 0),
    (1, 5, 7, 2),
    (4, 0, 3, 6)
)

colors = (
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (0, 0, 0),
    (1, 1, 1),
    (0, 1, 1),
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (0, 0, 0),
    (1, 1, 1),
    (0, 1, 1)
)


def Cube(InputX, InputY, InputZ, Shade):
    verticies = (
        (InputX + 1, InputY + -1, InputZ + -1),
        (InputX + 1, InputY + 1, InputZ + -1),
        (InputX + -1, InputY + 1, InputZ + -1),
        (InputX + -1, InputY + -1, InputZ + -1),
        (InputX + 1, InputY + -1, InputZ + 1),
        (InputX + 1, InputY + 1, InputZ + 1),
        (InputX + -1, InputY + -1, InputZ + 1),
        (InputX + -1, InputY + 1, InputZ + 1)
    )
    glBegin(GL_QUADS)
    for surface in surfaces:
        x = 0
        for vortex in surface:
            x += 1
            glColor3fv(colors[Shade])
            glVertex3fv(verticies[vortex])
    glEnd()

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glColor3fv(colors[10])
            glVertex3fv(verticies[vertex])
    glEnd()


###   Declaring Global Variables   ###
GridSize = 5
RandX = random.randint(0, GridSize - 1) * 2
RandY = random.randint(0, GridSize - 1) * 2
RandZ = random.randint(0, GridSize - 1) * 2
dir = (1, 0, 0)
MOVEEVENT, t = pygame.USEREVENT + 1, 1
pygame.time.set_timer(MOVEEVENT, t)
Time = 1
TailPos = [[0, 0, 0]]
###   Declaring Global Variables   ###

###   PyGame Display Settings   ###
display = (800, 800)
screen = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
gluPerspective(120, (display[0] / display[1]), 0.1, 50.0)
###   PyGame Display Settings   ###


###   First image to be displayed   ###
glTranslatef(-5, -5, -19)
glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
[[Cube(2 * x, 2 * y, 2 * z, 9) for x in range(GridSize)] for y in range(GridSize) for z in
         range(GridSize)]  # Grid Creation
Cube(RandX, RandY, RandZ, 6)
pygame.display.flip()
###   First image to be displayed   ###


###   Remove The Tail-Create The Head Functions   ###
''' This Function Moves A Snake Segment Based On His Chosen Direction '''


def AddHead(direction):
    x = TailPos[-1][0]
    y = TailPos[-1][1]
    z = TailPos[-1][2]
    if direction == (0, -1, 0):
        TailPos.append([x, y + 2, z])
    elif direction == (-1, 0, 0):
        TailPos.append([x - 2, y, z])
    elif direction == (0, 1, 0):
        TailPos.append([x, y - 2, z])
    elif direction == (1, 0, 0):
        TailPos.append([x + 2, y, z])
    elif direction == (0, 0, 1):
        TailPos.append([x, y, z + 2])
    elif direction == (0, 0, -1):
        TailPos.append([x, y, z - 2])


''' This Function Removes The Previous Snake Segment So The Moving Illusion Can Be Created. '''


def RemoveTail():
    TailPos.pop(0)

###   Remove The Tail-Create The Head Functions   ###



while True:  # Main While Loop
    for event in pygame.event.get():  # Going Through All Of The Events In The Pygame "Event List"
        if event.type == pygame.QUIT:  # If I Click The X Button, System Exits
            pygame.quit()
            quit()

    keys = pygame.key.get_pressed()  # Shortcut For Writing The Whole Thing Over And Over Again
    ###   If I Press One Of The Button Below I Trigger The Direction System(More Later)   ###
    if keys[pygame.K_w]:
        dir = (0, -1, 0)
    elif keys[pygame.K_a]:
        dir = (-1, 0, 0)
    elif keys[pygame.K_s]:
        dir = (0, 1, 0)
    elif keys[pygame.K_d]:
        dir = (1, 0, 0)
    elif keys[pygame.K_e]:
        dir = (0, 0, -1)
    elif keys[pygame.K_q]:
        dir = (0, 0, 1)
        ###   If I Press One Of The Button Below I Trigger The Direction System(More Later)   ###

    for e in pygame.event.get():  # Again Going Through The "Event List"
        if e.type == MOVEEVENT:  # is called every 't' milliseconds
            # Happens Every Tick Basically So, If I Do Something Once It Will Keep Happening Until I Do Something Else
            AddHead(dir)
            RemoveTail()

        if TailPos[-1][0] >= GridSize * 2:  # Checking If The Snake Is Going Out Of Bounds
            TailPos[-1][0] = 0
        elif TailPos[-1][0] < 0:
            TailPos[-1][0] = (GridSize - 1) * 2
        elif TailPos[-1][1] >= GridSize * 2:
            TailPos[-1][1] = 0
        elif TailPos[-1][1] < 0:
            TailPos[-1][1] = (GridSize - 1) * 2
        elif TailPos[-1][2] >= GridSize * 2:
            TailPos[-1][2] = 0
        elif TailPos[-1][2] < 0:
            TailPos[-1][2] = (GridSize - 1) * 2

        if (TailPos[-1][0] == RandX) and (TailPos[-1][1] == RandY) and (TailPos[-1][2] == RandZ):  # Checking If The Head Intersected With The Fruit
            RandX, RandY, RandZ = random.randint(0, GridSize - 1) * 2, random.randint(0, GridSize - 1) * 2, random.randint(0, GridSize - 1) * 2
            AddHead(dir)

        ###    DEATH    ###
        for i in range(len(TailPos) - 1):
            if (TailPos[-1][0] == TailPos[i][0]) and (TailPos[-1][1] == TailPos[i][1]) and (TailPos[-1][2] == TailPos[i][2]):
                TailPos = [TailPos[-1]]
                break
        ###    DEATH    ###

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        [[Cube(2 * x, 2 * y, 2 * z, 9) for x in range(GridSize)] for y in range(GridSize) for z in
         range(GridSize)]  # Grid Creation
        glRotate(1, 1, 1, 1)
        Cube(RandX, RandY, RandZ, 6)  # Creating The Fruit
        for i in range(len(TailPos)):
            Cube(TailPos[i][0], TailPos[i][1], TailPos[i][2], 1)  # Creating The Snake

        pygame.display.flip()  # Screen Update
