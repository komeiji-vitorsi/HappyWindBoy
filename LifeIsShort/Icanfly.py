import pygame
from pygame.locals import *
from sys import exit
from random import randint


#ＱＱＱHasakil！吹风类
class Wind(pygame.sprite.Sprite):
    def __init__(self,wind_surface,wind_init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = wind_surface
        self.rect = self.image.get_rect()
        self.rect.topleft = wind_init_pos
        self.speed = 8
    #移动
    def update(self):
        self.rect.right += self.speed
        if self.rect.right < -self.rect.width:
            self.kill()

#小兵类
class Enemy(pygame.sprite.Sprite):
    def __init__(self,enemy_surface,enemy_init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_surface
        self.rect = self.image.get_rect()
        self.rect.topleft = enemy_init_pos
        self.speed = 4

    def update(self):
        self.rect.right -= self.speed
        if self.rect.right < 0:
            self.kill()
#小兵组
enemy1_group = pygame.sprite.Group()

#玩家类
class Yasoo(pygame.sprite.Sprite):

    def __init__(self,yasoo_surface,yasoo_init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = yasoo_surface
        self.rect = self.image.get_rect()
        self.rect.topleft = yasoo_init_pos
        self.speed = 6
        #风组
        self.winds1 = pygame.sprite.Group()

    def single_shoot(self,wind1_surface):
        wind1 = Wind(wind1_surface,self.rect.midtop)
        self.winds1.add(wind1)

    def move(self,offset):
        x = self.rect.left + offset[pygame.K_RIGHT] - offset[pygame.K_LEFT]
        y = self.rect.top + offset[pygame.K_DOWN] - offset[pygame.K_UP]
        if x < 0:
            self.rect.left = 0
        elif x > SCREEN_WIDTH - 100:
            self.rect.left = SCREEN_WIDTH - 100
        else:
            self.rect.left = x

        if y < 0:
            self.rect.top = 0
        elif y > SCREEN_HEIGHT - 90:
            self.rect.top = SCREEN_HEIGHT - 90
        else:
            self.rect.top = y

#面对疾风吧！
class WindWall(pygame.sprite.Sprite):

    def __init__(self,windwall_surface,windwall_init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = windwall_surface
        self.rect = self.image.get_rect()
        self.rect.topleft = windwall_init_pos
        self.speed = 1
        
    def update(self):
        self.rect.right += self.speed
        if ticks % (ANIMATE_CYCLE//4) == 0:
            self.kill()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 634

#计数
ticks = 0

#帧率和帧数
FRAME_RATE = 60
ANIMATE_CYCLE = 60

clock = pygame.time.Clock()
offset = {pygame.K_LEFT:0,pygame.K_RIGHT:0,pygame.K_UP:0,pygame.K_DOWN:0}

#wind1图片
wind1_surface = pygame.image.load('images/wind.png')

#enemy1图片
enemy1_surface = pygame.image.load('images/xiaobing.png')


#+14!图片
enemy1_down_surface = pygame.image.load('images/+14.png')

#初始化
pygame.init()
screen = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])
pygame.display.set_caption('I can fly!')    #窗口标题

#背景图
background = pygame.image.load('images/background.jpg')

#初始化亚索
yasoo_surface = pygame.image.load('images/Happy.png')
yasoo_pos = [400,400]

#创建玩家
yasoo = Yasoo(yasoo_surface,yasoo_pos)

#补刀（杀死小兵）
enemy1_down_group = pygame.sprite.Group()

#事件循环(main loop)
while True:

    #限制帧率
    clock.tick(FRAME_RATE)

    #背景图
    screen.blit(background,(0,0))
    #画亚索
    screen.blit(yasoo.image,yasoo.rect)
    
    #退出
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit

        #控制方向
        if event.type == pygame.KEYDOWN:
            if event.key in offset:
                offset[event.key] = yasoo.speed
            if event.key == pygame.K_q:
                yasoo.single_shoot(wind1_surface)
#没写完的风墙在这里-----------------显眼的注释-------------------
#            if event.key == pygame.K_w:
#                windwall.
        elif event.type == pygame.KEYUP:
            if event.key in offset:
                offset[event.key] = 0
    #疾风剑道
    yasoo.winds1.update()
    #画Hasakil
    yasoo.winds1.draw(screen)

    #计数
    ticks += 1

    #出兵
    if ticks %60 == 0:
        enemy = Enemy(enemy1_surface, [1200,randint(0,634)])
        enemy1_group.add(enemy)
    enemy1_group.update()
    # 画小兵
    enemy1_group.draw(screen)

    #碰撞检测
    enemy1_down_group.add(pygame.sprite.groupcollide(enemy1_group,yasoo.winds1,True,False))

    #+14!
    for enemy1_down in enemy1_down_group:
         screen.blit(enemy1_down_surface,enemy1_down.rect)
         if ticks % (ANIMATE_CYCLE//2) == 0:
             enemy1_down_group.remove(enemy1_down)
        
    #更新屏幕
    pygame.display.update()
 
    #玩家移动
    yasoo.move(offset)
