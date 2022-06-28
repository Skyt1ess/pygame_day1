import pygame
import random
import math
import time
pygame.init()

display_size = [800, 600]

surf = pygame.Surface((800,600))

display = pygame.display.set_mode(display_size)
pygame.display.set_caption('Game')

icon = pygame.image.load('src/ufo.png')
pygame.display.set_icon(icon)
background = pygame.image.load('src/background.png')

PlayerImg = pygame.image.load('src/player.png')
EnemyImg = pygame.image.load('src/enemy.png')
EnemyGoldImg = pygame.image.load('src/enemygold.png')

PlayerX = display_size[0] / 2 - PlayerImg.get_size()[0] / 2
PlayerY = display_size[1] - PlayerImg.get_size()[1] - 30

PlayerMoveX = 0
PlayerSpeed = 8

Score = 0
PersonalBest=0
Score_x = 5
Score_y = 30
HP = 100
HP_x = 5
HP_y = 5
PB_x = 5
PB_y = 55

Lose_x = display_size[0]/2
Lose_y = display_size[1]/2

run = True
Time1 = 0
Reload1 = 20


Time2 = 0
Reload2 = 100

Enemy = []
EnemyCount = 4

EnemyGold = []
EnemyGoldCount = 1

Bullet = []
BulletSpeed = 9
font = pygame.font.SysFont('Paprus', 32)
fontlose = pygame.font.Font('src/bit8.ttf',100)
fonttip = pygame.font.SysFont('None',20)

BulletImg = pygame.image.load('src/bullet.png')




pygame.mixer.music.load('src/background.wav')
pygame.mixer.music.set_volume(0.3)
soundfon=-1
pygame.mixer.music.play(-1)

bullet_sound = pygame.mixer.Sound('src/laser.wav')
bullet_sound.set_volume(0.2)
enemy_sound = pygame.mixer.Sound('src/explosion.wav')
enemy_sound.set_volume(0.2)

text_hp = font.render('HP: ' + str(HP), True, (255, 255, 255))
best_score = font.render('Личный рекорд: ' + str(PersonalBest), True, (255, 255, 255))
def show_text():
     global text_hp,best_score
     display.blit(text_hp, (HP_x, HP_y))

     text_score = font.render('SCORE: ' + str(Score), True, (255, 255, 255))
     display.blit(text_score, (Score_x, Score_y))

def lose_text():
     textL = fontlose.render('Game Over',True,(255,0,0))
     display.blit(textL, (Lose_x - textL.get_size()[0] / 2, Lose_y - textL.get_size()[1] / 2))

     best_score = font.render('Личный рекорд: ' + str(PersonalBest), True, (255, 255, 255))
     display.blit(best_score, (Lose_x - best_score.get_size()[0] / 2, Lose_y - best_score.get_size()[1] / 2 + 100))

     final_score = font.render('SCORE: ' + str(Score), True, (255, 255, 255))
     display.blit(final_score, (Lose_x - final_score.get_size()[0] / 2, Lose_y - final_score.get_size()[1] / 2 +80))

     tip = fonttip.render('Клик в любом месте, чтобы начать заново',True,(255,255,255))
     display.blit(tip,(Lose_x - tip.get_size()[0] / 2, Lose_y + display_size[1]/2 - tip.get_size()[1]))

def PlayerUpdate():
    global PlayerX, PlayerMoveX
    PlayerX += PlayerMoveX

    if PlayerX < 0:
        PlayerX = 0

    if PlayerX + PlayerImg.get_size()[0] > display_size[0]:
        PlayerX = display_size[0] - PlayerImg.get_size()[0]


def EnemyCreate():
    EnemyX = random.randrange(0, display_size[0] - EnemyImg.get_size()[0])
    EnemyY = 0

    EnemyMoveX = random.randrange(-2, 4)
    EnemyMoveY = random.randrange(3, 7) / 2

    return [EnemyX, EnemyY, EnemyMoveX, EnemyMoveY]

def EnemyGoldCreate():
    EnemyX = random.randrange(0, display_size[0] - EnemyImg.get_size()[0])
    EnemyY = -700

    EnemyMoveX = random.randrange(-2, 4)
    EnemyMoveY = random.randrange(3, 7) / 2

    return [EnemyX, EnemyY, EnemyMoveX, EnemyMoveY]

def EnemyUpdate(Enemy):
    global HP

    Enemy[1] += Enemy[3]
    Enemy[0] += Enemy[2]

    if Enemy[0] < 0:
        Enemy[0] = 0
        Enemy[2] = -Enemy[2]

    if Enemy[0] + EnemyImg.get_size()[0] > display_size[0]:
        Enemy[0] = display_size[0] - EnemyImg.get_size()[0]
        Enemy[2] = -Enemy[2]

    if Enemy[1] > display_size[1]:
        HP -= 5
        Enemy = EnemyCreate()

    return Enemy

def EnemyGoldUpdate(Enemy):
    global HP

    Enemy[1] += Enemy[3]
    Enemy[0] += Enemy[2]

    if Enemy[0] < 0:
        Enemy[0] = 0
        Enemy[2] = -Enemy[2]

    if Enemy[0] + EnemyImg.get_size()[0] > display_size[0]:
        Enemy[0] = display_size[0] - EnemyImg.get_size()[0]
        Enemy[2] = -Enemy[2]

    if Enemy[1] > display_size[1]:
        HP -= 5
        Enemy = EnemyGoldCreate()

    return Enemy

def isCollision(X1, Y1, Img1, X2, Y2, Img2):
    first = pygame.Rect(X1, Y1, Img1.get_width(), Img1.get_height())
    second = pygame.Rect(X2, Y2, Img2.get_width(), Img2.get_height())
    return first.colliderect(second)


def BulletCreate(shotgun):
    BulletX = PlayerX + PlayerImg.get_width() / 2 - BulletImg.get_width() / 2
    BulletY = PlayerY - BulletImg.get_height()
    BulletMoveX = random.randrange(-2, 3)

    if not shotgun:
        BulletMoveX = 0

    BulletMoveY = -1 * math.sqrt(BulletSpeed * BulletSpeed - BulletMoveX * BulletMoveX)
    Bullet.append([BulletX, BulletY, BulletMoveX, BulletMoveY])

def BulletUdpate(Bullet):
    Bullet[0] += Bullet[2]
    Bullet[1] += Bullet[3]
    return Bullet


for i in range(EnemyCount):
    Enemy.append(EnemyCreate())

for i in range(EnemyGoldCount):
    EnemyGold.append(EnemyGoldCreate())

while run:
    if Time1 != 0:
        Time1 += 1
    if Time1 > Reload1:
        Time1 = 0

    if Time2 != 0:
        Time2 += 1
    if Time2 > Reload2:
        Time2 = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()

        if event.type == pygame.KEYDOWN and HP>0:
            if event.key in (pygame.K_LEFT, pygame.K_a):
                PlayerMoveX = -PlayerSpeed
            if event.key in (pygame.K_RIGHT, pygame.K_d):
                PlayerMoveX = PlayerSpeed

        if event.type == pygame.MOUSEBUTTONDOWN and HP>0:
            key = pygame.mouse.get_pressed()
            if key[0] and Time1 == 0:
                Time1 = 1
                bullet_sound.play()
                BulletCreate(False)

            if key[2] and Time2 == 0 and HP>0:
                Time2 = 1
                bullet_sound.play()
                for i in range(7):
                    BulletCreate(True)

        if event.type == pygame.KEYUP and HP>0:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT,
                             pygame.K_a, pygame.K_d):
                PlayerMoveX = 0

    for i in range(EnemyCount):
        Enemy[i] = EnemyUpdate(Enemy[i])

    for i in range(EnemyGoldCount):
        EnemyGold[i] = EnemyGoldUpdate(EnemyGold[i])


    for bullet in Bullet:
        bullet = BulletUdpate(bullet)
        if bullet[1] < 0:
            Bullet.remove(bullet)

    PlayerUpdate()


    for enemy in Enemy:
        if isCollision(PlayerX, PlayerY, PlayerImg,
                       enemy[0], enemy[1], EnemyImg):
            enemy_sound.play()
            Enemy.remove(enemy)
            Enemy.append(EnemyCreate())
            HP -= 10
            continue

        for bullet in Bullet:
            if isCollision(bullet[0], bullet[1], BulletImg,
                           enemy[0], enemy[1], EnemyImg):
                enemy_sound.play()
                Bullet.remove(bullet)
                Enemy.remove(enemy)
                Enemy.append(EnemyCreate())
                Score += 5
                break

    for enemy in EnemyGold:
        if isCollision(PlayerX, PlayerY, PlayerImg,
                        enemy[0], enemy[1], EnemyGoldImg):
            enemy_sound.play()
            EnemyGold.remove(enemy)
            EnemyGold.append(EnemyGoldCreate())
            HP -= 15
            continue

        for bullet in Bullet:
            if isCollision(bullet[0], bullet[1], BulletImg,
                           enemy[0], enemy[1], EnemyImg):
                enemy_sound.play()
                Bullet.remove(bullet)
                EnemyGold.remove(enemy)
                EnemyGold.append(EnemyGoldCreate())
                Score += 25
                break


    display.blit(background, (0, 0))


    display.blit(PlayerImg, (PlayerX, PlayerY))

    for enemy in Enemy:
        display.blit(EnemyImg, (enemy[0], enemy[1]))

    for enemy in EnemyGold:
        display.blit(EnemyGoldImg, (enemy[0], enemy[1]))

    for bullet in Bullet:
        display.blit(BulletImg, (bullet[0], bullet[1]))
    text_hp = font.render('HP: ' + str(HP), True, (255, 255, 255))
    if HP <= 15:
        text_hp = font.render('Осторожно! Кол-во HP: ' + str(HP), True, (255,0,0))
    show_text()
    if HP <= 0:
        PersonalBest = max (PersonalBest,Score)

        display.blit(surf,(0,0))
        pygame.mixer.music.stop()
        pygame.mixer.pause()
        lose_text()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.mixer.music.play(-1)
            pygame.mixer.unpause()
            Score = 0
            HP = 100
    pygame.display.update()
