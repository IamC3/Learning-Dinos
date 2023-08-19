import pygame as pg

pg.init()

ITSPREADS = False
STREAMLINED = False
DINO = True

vec = pg.math.Vector2
HEIGHT = 500
WIDTH = 500

DISPLAYSURF = pg.display.set_mode((WIDTH, HEIGHT), pg.RESIZABLE)

w, h = pg.display.get_surface().get_size()
r = (w - 500)
b = (h - 500)

GOAL = vec(WIDTH / 2, HEIGHT / 25)

FPS = 30  # change to make dots faster. (30)
FFONE = 10  # change to increase fastforward speed change (10)
FFTWO = 25
hdn = False

dotsize = 4  # size of generic dots (4)
CORPSESIZE = 2  # size of dead dots (2)
GOALSIZE = 2  # size of successful dots (2)
CHAMPSIZE = 8  # size of the champion (8)

DINOSIZEMOD = 7

DINODOT = pg.image.load("DINO/Norm.png").convert_alpha()
DINODOT = pg.transform.smoothscale(
    DINODOT, (dotsize * DINOSIZEMOD, dotsize * DINOSIZEMOD))
DINOCORPSE = pg.image.load("DINO/Slump.png").convert_alpha()
DINOCORPSE = pg.transform.smoothscale(
    DINOCORPSE, (dotsize * DINOSIZEMOD, dotsize * DINOSIZEMOD))
DINOGOAL = pg.image.load("DINO/Scream.png").convert_alpha()
DINOGOAL = pg.transform.smoothscale(
    DINOGOAL, (dotsize * DINOSIZEMOD, dotsize * DINOSIZEMOD))
DINOCHAMP = pg.image.load("DINO/Champ.png").convert_alpha()
DINOCHAMP = pg.transform.smoothscale(
    DINOCHAMP, (dotsize * DINOSIZEMOD, dotsize * DINOSIZEMOD))
DINOCHAMPGOAL = pg.image.load("DINO/ChampScream.png").convert_alpha()
DINOCHAMPGOAL = pg.transform.smoothscale(
    DINOCHAMPGOAL, (dotsize * DINOSIZEMOD, dotsize * DINOSIZEMOD))

HAM = pg.image.load("Ham.png").convert_alpha()
HAM = pg.transform.smoothscale(HAM, (30, 30))

DOTSTART = (WIDTH / 2, HEIGHT - 30
            )  # starting dot position (WIDTH/2, HEIGHT-30)

POPSIZE = 512  # amount of dots per population. (512)
BRAINSIZE = 500  # amount of directions each dot has (500)
MAXVEL = 5  # fastest a dot can go (5)
URANIUM = 1  # mutation chance out of 1000 (1)

WHITE = (255, 255, 255)

WORD = 'freesansbold.ttf'
FONT = pg.font.Font(WORD, 25)
FONT2 = pg.font.Font(WORD, 15)

LOADINGTEXT = FONT.render('GENERATING GENERATION', True, 0, WHITE)
LOADINGTEXTRECT = LOADINGTEXT.get_rect()
LOADINGTEXTRECT.center = (WIDTH / 2, HEIGHT / 2)

STARTTEXT = FONT.render('Press "ENTER" to Start Simulation', True, 0, WHITE)
STARTTEXTRECT = STARTTEXT.get_rect()
STARTTEXTRECT.center = (WIDTH / 2, HEIGHT / 2)

PAUSETEXT = FONT.render('Paused: Press "ENTER" to Unpause', True, 0, WHITE)
PAUSETEXTRECT = PAUSETEXT.get_rect()
PAUSETEXTRECT.center = (WIDTH / 2, HEIGHT / 2)

zoomText = FONT2.render('X' + str(1), True, 0, WHITE)
zoomTextRect = zoomText.get_rect()
zoomTextRect.midright = (WIDTH - 5, HEIGHT - 15)

statText1 = FONT2.render('GEN: ' + str(1), True, 0, WHITE)
statText2 = FONT2.render('POP SIZE: ' + str(POPSIZE), True, 0, WHITE)
statText3 = FONT2.render('HIGHEST FITNESS: ' + str(0), True, 0, WHITE)
statText4 = FONT2.render('MINIMUM STEPS: ' + str(BRAINSIZE), True, 0, WHITE)
statText5 = FONT2.render('MUTATION CHANCE: ' + str(URANIUM), True, 0, WHITE)

statTexts = [statText1, statText2, statText3, statText4, statText5]

FramePerSec = pg.time.Clock()

stage = 0

border = [(DISPLAYSURF, 0, (WIDTH, 0, r, HEIGHT), 0),
          (DISPLAYSURF, 0, (0, HEIGHT, WIDTH, b), 0)]

OBSTACLE0 = [(DISPLAYSURF, 0, (0, 0, 0, 0), 0)]
OBSTACLE1 = [(DISPLAYSURF, 0, (0, 0, WIDTH / 2.5, HEIGHT), 0),
             (DISPLAYSURF, 0, (WIDTH - WIDTH / 2.5, 0, WIDTH / 2.5, HEIGHT), 0)
             ]
OBSTACLE2 = [(DISPLAYSURF, 0, (WIDTH / 4, HEIGHT / 4, WIDTH / 2, HEIGHT / 2),
              0)]
OBSTACLE3 = [
    (DISPLAYSURF, 0, (WIDTH / 6, HEIGHT / 2, WIDTH / 1.5, HEIGHT / 3), 0),
    (DISPLAYSURF, 0, (0, 0, WIDTH / 2.5, HEIGHT / 3), 0),
    (DISPLAYSURF, 0, (WIDTH - WIDTH / 2.5, 0, WIDTH / 2.5, HEIGHT / 3), 0)
]
OBSTACLE4 = [(DISPLAYSURF, 0, (0, HEIGHT / 4, WIDTH / 3, HEIGHT / 8), 0),
             (DISPLAYSURF, 0, (WIDTH - WIDTH / 3, HEIGHT / 4, WIDTH / 3,
                               HEIGHT / 8), 0),
             (DISPLAYSURF, 0, (WIDTH / 6, HEIGHT / 2, 2 * WIDTH / 3,
                               HEIGHT / 8), 0),
             (DISPLAYSURF, 0, (0, 3 * HEIGHT / 4, WIDTH / 3, HEIGHT / 8), 0),
             (DISPLAYSURF, 0, (WIDTH - WIDTH / 3, 3 * HEIGHT / 4, WIDTH / 3,
                               HEIGHT / 8), 0)]

OBSTACLES = [OBSTACLE0, OBSTACLE1, OBSTACLE2, OBSTACLE3, OBSTACLE4]
