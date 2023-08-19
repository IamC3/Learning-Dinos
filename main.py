import pygame as pg
import sys
from pygame.locals import QUIT

import Population as Pop
import projectVar as V

start = True
pause = True
temp = 0
speedMulti = 1

V.zoomText = V.FONT2.render('X' + str(speedMulti), True, 0, V.WHITE)
V.zoomTextRect = V.zoomText.get_rect()
V.zoomTextRect.center = (V.WIDTH - 15, V.HEIGHT - 15)

key1 = key2 = key3 = False


def reset(room):
    global test, pause
  
    V.DISPLAYSURF.fill(V.WHITE)
  
    loading()
    
    V.stage = room
    print("Set Room to Room " + str(room))

    test = Pop.population()

    frame()

    V.DISPLAYSURF.blit(V.STARTTEXT, V.STARTTEXTRECT)
    pg.display.update()

    pause = True

def loading():
    V.DISPLAYSURF.blit(V.LOADINGTEXT, V.LOADINGTEXTRECT)
    pg.display.update()

def frame():
    if not V.ITSPREADS:
        V.DISPLAYSURF.fill(V.WHITE)
    pg.draw.circle(V.DISPLAYSURF, (0, 0, 255), (V.GOAL), 7, 7)
    for box in V.OBSTACLES[V.stage]:
        pg.draw.rect(box[0], box[1], box[2], box[3])
    for edge in V.border:
        pg.draw.rect(edge[0], edge[1], edge[2], edge[3])
    V.DISPLAYSURF.blit(V.zoomText, V.zoomTextRect)
    image = V.HAM
    imgrect = image.get_rect(center=(V.WIDTH - 30, 30))
    V.DISPLAYSURF.blit(image, imgrect)
    cycle()
    stats()
    pg.display.update()
    V.FramePerSec.tick(speedMulti * V.FPS)


def cycle():
    if test.allDotsDead():
        test.show()
        V.statText1 = V.FONT2.render('GEN: ' + str(test.gen), True, 0, V.WHITE)
        V.statText2 = V.FONT2.render('POP SIZE: ' + str(V.POPSIZE), True, 0, V.WHITE)
        V.statText3 = V.FONT2.render('HIGH FIT: ' + '%.2f' % test.max,
                                     True, 0, V.WHITE)
        V.statText4 = V.FONT2.render('MIN STEPS: ' + str(test.minStep),
                                     True, 0, V.WHITE)
        V.statText5 = V.FONT2.render('MUTATION CHANCE: ' + str(V.URANIUM),
                                   True, 0, V.WHITE)


        V.statTexts = [V.statText1, V.statText2, V.statText3, V.statText4, V.statText5]
        stats()
        loading()
        test.calculateFitness()
        test.naturalSelection()
        test.mutation()
    else:
        test.update()
        test.show()

def stats():
    count = 0
    for text in V.statTexts:
        statTextRect = text.get_rect()
        statTextRect.topleft = (0, 0 + count)
        V.DISPLAYSURF.blit(text, statTextRect)
        count += 13


def events():
    global pause, temp, speedMulti, test, key1, key2, key3
    if key1 and key2 and key3:
        key1 = key2 = key3 = False
        reset(V.stage)
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit
        if event.type == pg.KEYDOWN:
            
            if event.key == pg.K_RETURN:
              if not pause:
                print("Paused") 
                V.DISPLAYSURF.blit(V.PAUSETEXT, V.PAUSETEXTRECT)
                pg.display.update()
              else:
                print("UnPaused")
              pause = not pause
                
            elif event.key == pg.K_SPACE:
                frame() if pause else None
                
            elif event.key == pg.K_f:
                if speedMulti == 1:
                    print("Zoom")
                    speedMulti = V.FFONE
                elif speedMulti == V.FFONE:
                    print("Zoomer")
                    speedMulti = V.FFTWO
                elif speedMulti == V.FFTWO:
                    print("UnZoom")
                    speedMulti = 1
                V.zoomText = V.FONT2.render('X' + str(speedMulti), True, 0,
                                            V.WHITE)
                V.zoomTextRect = V.zoomText.get_rect()
                V.zoomTextRect.midright = (V.WIDTH - 5, V.HEIGHT - 15)
                
            elif event.key == pg.K_m:
                print("expand")
                V.POPSIZE *= 2
                V.statText2 = V.FONT2.render('POP SIZE: ' + str(V.POPSIZE) + ' (Next Gen)', True, 0, V.WHITE)
                V.statTexts[1] = V.statText2
                
            elif event.key == pg.K_n:
                print("unexpand")
                if V.POPSIZE > 1:
                    V.POPSIZE = int(V.POPSIZE/2)
                    V.statText2 = V.FONT2.render('POP SIZE: ' + str(V.POPSIZE) + ' (Next Gen)', True, 0, V.WHITE)
                    V.statTexts[1] = V.statText2
                    
            elif event.key == pg.K_COMMA:
                print("DERAD")
                if V.URANIUM - 1 >= 0:
                    V.URANIUM -= 1
                    V.statText5 = V.FONT2.render('MUTATION CHANCE: ' + str(V.URANIUM) + ' (Next Gen)', True, 0, V.WHITE)
                    V.statTexts[4] = V.statText5
                    
            elif event.key == pg.K_k:
                print("DERAD+")
                if V.URANIUM - 5 >= 0:
                    V.URANIUM -= 5
                    V.statText5 = V.FONT2.render('MUTATION CHANCE: ' + str(V.URANIUM) + ' (Next Gen)', True, 0, V.WHITE)
                    V.statTexts[4] = V.statText5
                    
            elif event.key == pg.K_PERIOD:
                print("RAD")
                if V.URANIUM + 1 <= 100:
                    V.URANIUM += 1
                    V.statText5 = V.FONT2.render('MUTATION CHANCE: ' + str(V.URANIUM) + ' (Next Gen)', True, 0, V.WHITE)
                    V.statTexts[4] = V.statText5
                    
            elif event.key == pg.K_l:
                print("RAD+")
                if V.URANIUM + 5 <= 100:
                    V.URANIUM += 5
                    V.statText5 = V.FONT2.render('MUTATION CHANCE: ' + str(V.URANIUM) + ' (Next Gen)', True, 0, V.WHITE)
                    V.statTexts[4] = V.statText5
            elif event.key == pg.K_h:
                if not V.hdn:
                    print("Hidden")
                    temp = V.dotsize
                    V.dotsize = 0
                else:
                    print("UnHidden")
                    V.dotsize = temp
                V.hdn = not V.hdn

            # change room
            elif event.key == pg.K_0:
                reset(0)
            elif event.key == pg.K_1:
                reset(1)
            elif event.key == pg.K_2:
                reset(2)
            elif event.key == pg.K_3:
                reset(3)
            elif event.key == pg.K_4:
                reset(4)

            # reset simulation
            if event.key == pg.K_BACKSPACE:
                key1 = True
            elif event.key == pg.K_LCTRL:
                key2 = True
            elif event.key == pg.K_RCTRL:
                key3 = True
            else:
                key1 = key2 = key3 = False


pg.init()
pg.display.set_caption('THE SWARM!')
print("\n//////////GEN 1//////////")

reset(V.stage)

count = 0
for text in V.statTexts:
    statTextRect = text.get_rect()
    statTextRect.topleft = (0, 0 + count)
    V.DISPLAYSURF.blit(text, statTextRect)
    count += 13
# pg.display.update()


def screenCheck():
    if (V.w, V.h) != pg.display.get_surface().get_size():
        V.w, V.h = pg.display.get_surface().get_size()
        V.r = (V.w - 500)
        V.b = (V.h - 500)
        V.border = [(V.DISPLAYSURF, 0, (V.WIDTH, 0, V.r, V.h), 0),
                    (V.DISPLAYSURF, 0, (0, V.HEIGHT, V.w, V.b), 0)]


if V.ITSPREADS:
    pg.display.set_caption('IT SPREADS!')
while True:
    screenCheck()
    events()
    while pause:
        events()
    frame()
