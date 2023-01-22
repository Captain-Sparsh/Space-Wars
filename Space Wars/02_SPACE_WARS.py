import pygame
import os
import time
x = pygame.init()
pygame.mixer.init()
pygame.font.get_fonts()

#COLOURS
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
GREEN = (0,255,0)
CYAN = (0,255,255)

WIDTH,HEIGHT = 1520,800
FPS = 60
VELO = 4
BULLET_VEL = 8
MAX_BULL = 9
MAX_HEALTH = 1000
WRITING = pygame.font.SysFont('comicsansms',69)
WRITING_2 = pygame.font.SysFont('ariel',56)
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("SPACE WARS")
pygame.display.update()
clock = pygame.time.Clock()

#Spaceship IMAGES
SHIP_W = 50
SHIP_H = 50

P1_SP = pygame.image.load('Space Wars\Images\\02a_p1.jpg')
P1_SP = pygame.transform.rotate(pygame.transform.scale(P1_SP,(SHIP_W,SHIP_H)),270)
P2_SP = pygame.image.load('Space Wars\Images\\02a_p2.jpg')
P2_SP = pygame.transform.rotate(pygame.transform.scale(P2_SP,(SHIP_W,SHIP_H)),90)

BGIG = pygame.image.load('Space Wars\Images\\02a_backg.jpg')
BGIG = pygame.transform.scale(BGIG,((WIDTH/2)-5,HEIGHT))
WEL = pygame.image.load('Space Wars\Images\\02a_welcome.png')
WEL = pygame.transform.scale(WEL,(WIDTH,HEIGHT))
INS = pygame.image.load('Space Wars\Images\\02a_inst.jpg')
INS = pygame.transform.scale(INS,(WIDTH,HEIGHT))
P1WON = pygame.image.load('Space Wars\Images\\02a_p1won.png')
P1WON = pygame.transform.scale(P1WON,(WIDTH,HEIGHT))
P2WON = pygame.image.load('Space Wars\Images\\02a_p2won.png')
P2WON = pygame.transform.scale(P2WON,(WIDTH,HEIGHT))

P1_HIT = pygame.USEREVENT + 1
P2_HIT = pygame.USEREVENT + 3

def screen_text(text,color,x,y):
    on_screen = WRITING.render(text,True,color)
    SCREEN.blit(on_screen,[x,y])

def screen_text_2(text,color,x,y):
    on_screen = WRITING_2.render(text,True,color)
    SCREEN.blit(on_screen,[x,y])

def p1_movement(keys_pressed,p1_pos):
    if keys_pressed[pygame.K_w] and p1_pos.y>0:
        p1_pos.y -= VELO
    if keys_pressed[pygame.K_s] and p1_pos.y < HEIGHT-SHIP_H:
        p1_pos.y += VELO
    if keys_pressed[pygame.K_a] and p1_pos.x >0:
        p1_pos.x -= VELO
    if keys_pressed[pygame.K_d]and p1_pos.x < (WIDTH/2)-20-SHIP_W:
        p1_pos.x += VELO

def p2_movement(keys_pressed,p2_pos):
    if keys_pressed[pygame.K_UP] and p2_pos.y>0:
        p2_pos.y -= VELO
    if keys_pressed[pygame.K_DOWN] and p2_pos.y < HEIGHT-SHIP_H:
        p2_pos.y += VELO
    if keys_pressed[pygame.K_RIGHT] and p2_pos.x <WIDTH - SHIP_W:
        p2_pos.x += VELO
    if keys_pressed[pygame.K_LEFT] and p2_pos.x > (WIDTH/2)+10:
        p2_pos.x -= VELO

def draw_bullets(p1_nb,p2_nb):
    
    for bullets in p1_nb:
        pygame.draw.rect(SCREEN, RED,bullets)

    for bullets in p2_nb:
        pygame.draw.rect(SCREEN, YELLOW,bullets)

def track_bullets(p1_nb,p2_nb,p1_pos,p2_pos):
    for bullets in p1_nb:
        bullets.x += BULLET_VEL
        if p2_pos.colliderect(bullets):
            pygame.event.post(pygame.event.Event(P2_HIT))
            p1_nb.remove(bullets)
        elif bullets.x>WIDTH:
            p1_nb.remove(bullets)
        
    for bullets in p2_nb:
        bullets.x -= BULLET_VEL
        if p1_pos.colliderect(bullets):
            pygame.event.post(pygame.event.Event(P1_HIT))
            p2_nb.remove(bullets)
        elif bullets.x<0:
            p2_nb.remove(bullets)
        
def welcome():
    game_end = False
    while not game_end:
        SCREEN.blit(WEL,(0,0))
        screen_text('WELCOME TO SPACE WARS',GREEN,280,HEIGHT-200)
        screen_text('PRESS SPACEBAR TO START',GREEN,265,HEIGHT - 100)

        for steps in pygame.event.get():

            if steps.type == pygame.QUIT:
                game_end = True

            if steps.type == pygame.KEYDOWN:
                if steps.key == pygame.K_SPACE:
                    pygame.mixer.music.load('Space Wars\Music\\02a_entry.mp3')
                    pygame.mixer.music.play()
                    instructions()

        pygame.display.update()
        clock.tick(FPS+9)

def instructions():
    game_end = False
    while not game_end:
        SCREEN.blit(INS,(0,0))

        screen_text_2('PLAYER 1',GREEN,85,150)
        screen_text_2('A --->  MOVE LEFT',YELLOW,50,250)
        screen_text_2('D --->  MOVE RIGHT',YELLOW,50,300)
        screen_text_2('W --->  MOVE UP',YELLOW,50,350)
        screen_text_2('S --->  MOVE DOWN',YELLOW,50,400)
        screen_text_2('SPACEBAR --->  FIRE',YELLOW,50,450)

        screen_text_2('PLAYER 2',GREEN,945,150)
        screen_text_2('LEFT ARROW --->  MOVE LEFT',YELLOW,820,250)
        screen_text_2('RIGHTARROW --->  MOVE RIGHT',YELLOW,820,300)
        screen_text_2('UP ARROW --->  MOVE UP',YELLOW,820,350)
        screen_text_2('DOWN ARROW --->  MOVE DOWN',YELLOW,820,400)
        screen_text_2('LEFT CTRL --->  FIRE',YELLOW,820,450)
        
        screen_text_2("DESTROY YOUR OPPONENT BEFORE HE DESTROYS YOU.",WHITE,50,HEIGHT-150)
        screen_text_2(f"MAXIMUM {MAX_BULL} BULLETS AT ONCE CAN BE FIRED.",WHITE,50,HEIGHT-100)
        screen_text_2("PRESS ENTER",RED,1190,HEIGHT-69)
        screen_text("GYAN",CYAN,600,10)

        for steps in pygame.event.get():

            if steps.type == pygame.QUIT:
                game_end = True

            if steps.type == pygame.KEYDOWN:
                if steps.key == pygame.K_RETURN:
                    pygame.mixer.music.load('Space Wars\Music\\02a_music.mp3')
                    pygame.mixer.music.play()
                    ori()
        pygame.display.update()
        clock.tick(FPS+9)
    pygame.quit()

def ori():
    game_over = False
    end_game = False
    dedect = 0
    
    p1_pos = pygame.Rect(100,350,SHIP_W,SHIP_H)
    p2_pos = pygame.Rect(1100,350,SHIP_W,SHIP_H)

    p1_nb =[]
    p2_nb =[]
    p1_h = MAX_HEALTH
    p2_h = MAX_HEALTH
    
    while not game_over:

        clock.tick(FPS)
        SCREEN.fill(CYAN)
        SCREEN.blit(BGIG,(0,0))
        SCREEN.blit(BGIG,((WIDTH/2)+5,0))
        SCREEN.blit(P1_SP,(p1_pos.x,p1_pos.y))
        SCREEN.blit(P2_SP,(p2_pos.x,p2_pos.y))
        screen_text_2('HEALTH : '+ str(p1_h),RED,30,10)
        screen_text_2('HEALTH : '+ str(p2_h),RED,800,10)

        if end_game:
            SCREEN.fill(CYAN)
            
            if dedect == 0:
                SCREEN.blit(P1WON,(0,0))
                screen_text("WINNER", CYAN, 650,10)
                screen_text_2("PRESS ENTER TO PLAY AGAIN",RED,850,HEIGHT-50)

                for steps in pygame.event.get():

                    if steps.type == pygame.QUIT:
                        game_over = True

                    if steps.type == pygame.KEYDOWN:
                        if steps.key == pygame.K_RETURN:
                            pygame.mixer.music.load('Space Wars\Music\\02a_entry.mp3')
                            pygame.mixer.music.play()
                            instructions() 

            if dedect == 1:
                SCREEN.blit(P2WON,(0,0))
                screen_text("WINNER", CYAN, 650,10)
                screen_text_2("PRESS ENTER TO PLAY AGAIN",RED,850,HEIGHT-50)

                for steps in pygame.event.get():

                    if steps.type == pygame.QUIT:
                        game_over = True

                    if steps.type == pygame.KEYDOWN:
                        if steps.key == pygame.K_RETURN:
                            pygame.mixer.music.load('Space Wars\Music\\02a_entry.mp3')
                            pygame.mixer.music.play()
                            instructions() 
        else:

            for steps in pygame.event.get():

                if steps.type == pygame.QUIT:
                    game_over= True
                if steps.type == pygame.KEYDOWN:

                    if steps.key == pygame.K_SPACE and len(p1_nb) < MAX_BULL:
                        bullets = pygame.Rect(p1_pos.x + SHIP_W,p1_pos.y -2 + SHIP_H/2,10,6)
                        p1_nb.append(bullets)

                    if steps.key == pygame.K_RCTRL and len(p2_nb) < MAX_BULL:
                        bullets = pygame.Rect(p2_pos.x ,p2_pos.y -2 + SHIP_H/2,10,6)
                        p2_nb.append(bullets)

                if steps.type == P1_HIT:
                    p1_h-=100
                if steps.type == P2_HIT:
                    p2_h-=100

            if p1_h<=0:
                end_game = True  
                dedect = 1
            if p2_h<=0:
                end_game = True  
                
            keys_pressed = pygame.key.get_pressed()
            p1_movement(keys_pressed,p1_pos)
            p2_movement(keys_pressed,p2_pos)
            draw_bullets(p1_nb,p2_nb)
            track_bullets(p1_nb,p2_nb,p1_pos,p2_pos)

        pygame.display.update()
    pygame.quit()

welcome()
           