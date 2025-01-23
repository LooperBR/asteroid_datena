import os, sys
import getopt

import pygame
from pygame.locals import *
import math
import random

pygame.mixer.init()


images_dir = os.path.join( "..", "imagens" )

resolution_x = 1600
resolution_y = 900

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

nave_img = pygame.image.load('imagens/nave.png')
super_nave_img = pygame.image.load('imagens/superNave.png')
bala_img = pygame.image.load('imagens/bala.png')
super_bala_img = pygame.image.load('imagens/superBala.png')
asteroid_img = pygame.image.load('imagens/asteroid.png')
tutorial_img = pygame.image.load('imagens/tutorial.png')

nao_datena_audio = pygame.mixer.Sound("audio/nao_datena.mp3")
nao_eh_homem = pygame.mixer.Sound("audio/nao_eh_homem.mp3")

class Ship:
    
    def __init__(self,x,y):
        self.x = float(x/2)
        self.y = float(y/2)
        self.direction = float(0)
        self.rotr = math.radians(self.direction)
        self.ysp = math.cos(self.rotr)
        self.xsp = math.sin(self.rotr)
        self.turnSpeed = float(180)
        self.moveSpeed = float(150)
        self.sizeX = 60
        self.sizeY = 60
        ship = pygame.Surface( (self.sizeX,self.sizeY), pygame.SRCALPHA, 32 ).convert_alpha()
        #ship.fill( ( 0, 0, 255 ) )
        #nave_img = pygame.transform.scale(nave_img, (20, 20))
        ship.blit(pygame.transform.scale(nave_img, (self.sizeX, self.sizeY)),(0,0))
        self.image = ship

        ship2 = pygame.Surface( (self.sizeX,self.sizeY), pygame.SRCALPHA, 32 ).convert_alpha()
        ship2.blit(pygame.transform.scale(super_nave_img, (self.sizeX, self.sizeY)),(0,0))
        self.image2 = ship2

    def shoot(self):
        pass

    def die(self):
        pass

    def rotate(self,dir,delta):
        self.direction += dir*self.turnSpeed*delta

        if self.direction>360:
            self.direction = 0
        if self.direction<0:
            self.direction = 360

        self.rotr = math.radians(self.direction)
        pass

    def move(self,direction2,delta):
        self.ysp = math.cos(self.rotr)
        self.xsp = math.sin(self.rotr)
        self.x += float(self.xsp*direction2*delta*self.moveSpeed)
        self.y += float(self.ysp*direction2*delta*self.moveSpeed)

        if(self.x<0):
            self.x=0
        if(self.x>resolution_x):
            self.x=resolution_x
        if(self.y<0):
            self.y=0
        if(self.y>resolution_y):
            self.y=resolution_y
        pass

    def draw( self, screen, charge):
        if charge>0.8 and charge<1.2:
            new_image = pygame.transform.rotate(self.image2, self.direction)
        else:
            new_image = pygame.transform.rotate(self.image, self.direction)

        new_rect = new_image.get_rect(center = self.image.get_rect(topleft = (self.x,self.y)).center)

        #pygame.draw.rect(new_image, "black", ((new_image.get_width()-self.sizeX)/2, (new_image.get_height()-self.sizeY)/2, self.sizeX, self.sizeY), 1)
        #print('new_rect ',new_rect)
        screen.blit( new_image, (new_rect[0]-(self.sizeX/2),new_rect[1]-(self.sizeY/2)) )

    def printAll(self):
        print("x: ",self.x)
        print("y: ",self.y)
        print("direction: ",self.direction)
        print("rotr: ",self.rotr)
        print("ysp: ",self.ysp)
        print("xsp: ",self.xsp)


class Background:
    """
    Esta classe representa o ator "Fundo" do jogo.
    """
    image = None
    
    def __init__( self ):
        screen = pygame.display.get_surface()
        back   = pygame.Surface( screen.get_size() ).convert()
        back.fill( ( 30, 30, 30 ) )
        self.image = back
    # __init__()



    def update( self, dt ):
        pass # Ainda não faz nada
    # update()



    def draw( self, screen ):
        screen.blit( self.image, ( 0, 0 ) )
    # draw()
# Background

class Projectile:
    def __init__(self,direction,x,y,charge,superNova=False):
        self.perfect = False
        if charge>0.8 and charge < 1.2:
            charge = 1
            self.perfect = True
        charge +=1
        if charge<1:
            charge = 1
        if charge>2:
            charge = 2
        self.speed = 300 * charge
        self.direction = direction
        self.rotr = math.radians(self.direction)
        self.x = x
        self.y = y
        self.ysp = math.cos(self.rotr)
        self.xsp = math.sin(self.rotr)
        self.sizeX = 60 * charge
        self.sizeY = 60 * charge

        self.superNova = superNova

        self.health = int(1*charge)
        projectile = pygame.Surface( (self.sizeX,self.sizeY), pygame.SRCALPHA, 32 ).convert_alpha()
        #projectile.fill( ( 0, 0, 255 ) )
        #nave_img = pygame.transform.scale(nave_img, (20, 20))
        if self.perfect:
            self.health = 10
            projectile.blit(pygame.transform.scale(super_bala_img, (self.sizeX,self.sizeY)),(0,0))
        else:
            projectile.blit(pygame.transform.scale(bala_img, (self.sizeX,self.sizeY)),(0,0))
        self.image = projectile

    def move(self,delta):
        self.x -= float(self.xsp*delta*self.speed)
        self.y -= float(self.ysp*delta*self.speed)


    def draw( self, screen ):
        new_image = pygame.transform.rotate(self.image, self.direction)

        new_rect = new_image.get_rect(center = self.image.get_rect(topleft = (self.x,self.y)).center)
        
        #pygame.draw.rect(new_image, "black", ((new_image.get_width()-self.sizeX)/2, (new_image.get_height()-self.sizeY)/2, self.sizeX, self.sizeY), 1)

        screen.blit( new_image, (new_rect[0]-(self.sizeX/2),new_rect[1]-(self.sizeY/2)) )

class TutorialImage:
    def __init__(self):
        asteroid = pygame.Surface( (1200,700), pygame.SRCALPHA, 32 ).convert_alpha()

        asteroid.blit(pygame.transform.scale(tutorial_img, (1200,700)),(0,0))
        self.image = asteroid
    
    def draw( self, screen ):
        screen.blit( self.image, (0,0) )
        

class Asteroid:
    def __init__(self,x=-1,y=-1,direction=0,boss=False):
        self.boss=boss
        
        if not boss:
            self.health = 1
            self.speed = random.randint(80, 200)
            if(x==-1 and y==-1):
                if(random.randint(0,1)==0):
                    if(random.randint(0,1)==0):
                        self.x = 0
                        self.direction = random.randint(210, 330)
                        self.rotr = math.radians(self.direction)
                    else:
                        self.x = resolution_x
                        self.direction = random.randint(30, 150)
                        self.rotr = math.radians(self.direction)
                    
                    self.y = random.randint(0, resolution_y)

                else:
                    if(random.randint(0,1)==0):
                        self.y = 0
                        self.direction = random.randint(120, 240)
                        self.rotr = math.radians(self.direction)
                    else:
                        self.y = resolution_y
                        self.direction = random.randint(310, 420)
                        self.rotr = math.radians(self.direction)

                    self.x = random.randint(0, resolution_x)
            else:
                self.x = x
                self.y = y
                self.direction = direction
                self.rotr = math.radians(self.direction)
                
            if self.direction>360:
                self.direction-=360
                self.rotr = math.radians(self.direction)

            if self.direction<0:
                self.direction+=360
                self.rotr = math.radians(self.direction)

            self.ysp = math.cos(self.rotr)
            self.xsp = math.sin(self.rotr)
            self.sizeX = 60
            self.sizeY = 60
            asteroid = pygame.Surface( (self.sizeX,self.sizeY), pygame.SRCALPHA, 32 ).convert_alpha()
            #asteroid.fill( ( 0, 0, 255 ) )
            asteroid.blit(pygame.transform.scale(asteroid_img, (self.sizeX,self.sizeY)),(0,0))
            self.image = asteroid
        else:
            self.health = 100
            self.speed = 200
            self.x = resolution_x
            self.y = resolution_y/2
            self.direction = 0
            self.rotr = math.radians(self.direction)
            self.ysp = math.cos(self.rotr)
            self.xsp = math.sin(self.rotr)
            self.sizeX = 400
            self.sizeY = 400
            asteroid = pygame.Surface( (self.sizeX,self.sizeY), pygame.SRCALPHA, 32 ).convert_alpha()
            #asteroid.fill( ( 0, 0, 255 ) )
            asteroid.blit(pygame.transform.scale(asteroid_img, (self.sizeX,self.sizeY)),(0,0))
            self.image = asteroid

    def move(self,delta):
        self.x -= float(self.xsp*delta*self.speed)
        self.y -= float(self.ysp*delta*self.speed)


    def draw( self, screen ):
        new_image = pygame.transform.rotate(self.image, self.direction)

        new_rect = new_image.get_rect(center = self.image.get_rect(topleft = (self.x,self.y)).center)
        
        #pygame.draw.rect(new_image, "black", ((new_image.get_width()-self.sizeX)/2, (new_image.get_height()-self.sizeY)/2, self.sizeX, self.sizeY), 1)

        screen.blit( new_image, (new_rect[0]-(self.sizeX/2),new_rect[1]-(self.sizeY/2)) )

class Text:
    def __init__(self,text,x,y,size,color = (255,255,255)):
        self.x = x
        self.y = y
        self.text = text
        self.my_font = pygame.font.SysFont('Comic Sans MS', size)
        self.color=color

    def draw( self, screen ):
        text_surface = self.my_font.render(self.text, False, (self.color))
        
        screen.blit( text_surface, (self.x,self.y) )


class Game:
    screen      = None
    screen_size = None
    run         = True
    background  = None   
    ship = None 
    boss = None
    startLabel = None
    timeLabel = None
    scoreLabel = None
    endingLabel = None
    bossLabel = None
    tutorialImg = None
    w = False
    s = False
    a = False
    d = False
    shoot = False
    debug = False
    bullets = []
    asteroids = []
    duration = 0
    timer = 0
    score = 0
    running = False
    size = None
    charge = 0
    launchShot = False
    superMaxCharge = 20
    superCharge = 0
    launchSuper = False
    lives = 3
    currentLevel = 1
    scoreToLevel = 30000

    def __init__( self, size, fullscreen ):
        """
        Esta é a função que inicializa o pygame, define a resolução da tela,
        caption, e disabilitamos o mouse dentro desta.
        """
        actors = {}
        pygame.init()

        flags = DOUBLEBUF
        if fullscreen:
            flags |= FULLSCREEN
        self.screen       = pygame.display.set_mode( size, flags )
        self.screen_size = self.screen.get_size()

        self.size = size

        self.game_start(size)

        pygame.mouse.set_visible( 0 )
        pygame.display.set_caption( 'Asteroid' )
    # init()

    def game_start(self,size):
        self.ship = Ship(size[0],size[1])
        self.startLabel  = Text('Aperte P para iniciar',resolution_x/2-100,resolution_y/2-100,30)
        self.endingLabel = Text('Parabens voce ganhou',resolution_x/2-100,resolution_y/2-100,30)
        self.tutorialImg = TutorialImage()
        self.timeLabel = Text('teste1',0,0,30)
        self.scoreLabel = Text('teste2',800,0,30)
        self.livesLabel = Text('3 vidas',1300,0,30)
        self.superLabel = Text('0/20',800,800,30)
        self.duration=0
        self.timer=0
        self.score=0
        self.charge=0
        self.superCharge=0
        self.currentLevel = 1
        self.lives = 3

        for asteroid in self.asteroids[:]: 
            self.asteroids.remove(asteroid)

        for bullet in self.bullets[:]: 
            self.bullets.remove(bullet)

        #self.running=True


    def handle_events( self ):
        """
        Trata o evento e toma a ação necessária.
        """
        for event in pygame.event.get():
            t = event.type
            if t in ( KEYDOWN, KEYUP ):
                k = event.key

            if t in ( MOUSEBUTTONDOWN, MOUSEBUTTONUP ):
                k = event.button

            if t == QUIT:
                self.run = False

            elif t == KEYDOWN:
                if   k == K_ESCAPE:
                    self.run = False
                elif k == K_w:
                    self.w = True
                elif k == K_s:
                    self.s = True
                elif k == K_a:
                    self.a = True
                elif k == K_d:
                    self.d = True
                elif k == K_p:
                        self.running = True
                        self.game_start(self.size)
                elif k == K_SPACE:
                    self.shoot = True
                elif k == K_KP_ENTER:
                    if self.debug:
                        print("no Debug")
                        self.debug = False
                    else:
                        print("Debug")
                        self.debug = True
            elif t == KEYUP:
                if k == K_w:
                    self.w = False
                elif k == K_s:
                    self.s = False
                elif k == K_a:
                    self.a = False
                elif k == K_d:
                    self.d = False
                elif k == K_SPACE:
                    self.shoot = False
                    self.launchShot = True
                elif k == K_LSHIFT:
                    self.launchSuper = True

                
            elif t == MOUSEBUTTONDOWN:
                if k == 1:
                    self.shoot = True
                elif k == 3:
                    self.launchSuper = True
            elif t == MOUSEBUTTONUP:
                if k == 1:
                    self.shoot = False
                    self.launchShot = True



    # handle_events()




    def actors_update( self, dt,delta ):        
        self.background.update( dt )
        if self.w and not self.s:
            self.ship.move(-1,delta)
        if self.s and not self.w:
            self.ship.move(1,delta)
        if self.d and not self.a:
            self.ship.rotate(-1,delta)
        if self.a and not self.d:
            self.ship.rotate(1,delta)

        if self.shoot:
            self.charge +=delta

        if self.launchShot:
            self.launchShot = False
            self.ship.shoot()

            bulletAmount = 0
            for bullet in self.bullets[:]:
                if not bullet.superNova:
                    bulletAmount+=1

            if(bulletAmount<5):
                if(self.currentLevel==1):
                    bullet = Projectile(self.ship.direction,self.ship.x,self.ship.y,self.charge)
                    self.bullets.append(bullet)
                elif(self.currentLevel==2):
                    bullet = Projectile(self.ship.direction,self.ship.x,self.ship.y,self.charge)
                    self.bullets.append(bullet)
                    bullet = Projectile(self.ship.direction+25,self.ship.x,self.ship.y,self.charge,superNova=True)
                    self.bullets.append(bullet)
                    bullet = Projectile(self.ship.direction-25,self.ship.x,self.ship.y,self.charge,superNova=True)
                    self.bullets.append(bullet)
                #print('shoot',self.charge)
                self.charge = 0
        
        if self.launchSuper:
            #print('super tentativa')
            pass
            

        if self.launchSuper and self.superCharge>=self.superMaxCharge:
            self.ship.shoot()

            degrees = [0,45,90,135,180,225,270,315]

            for degree in degrees:
                bullet = Projectile(degree,self.ship.x,self.ship.y,1,True)
                self.bullets.append(bullet)

            nao_datena_audio.play()
            nao_datena_audio.set_volume(1)

            self.launchSuper = False
            self.superCharge = 0
            #print('super')
    
        i=1
        for bullet in self.bullets[:]:
            #print('bullet',i)
            i+=1
            bullet.move(delta)
            if(bullet.x>resolution_x or bullet.x<0 or bullet.y>resolution_y or bullet.y<0):
                self.bullets.remove(bullet)  
        
        bulletsRemove = []
        asteroidsHit = []
        asteroidsHitNormal = []
        asteroidsRemove = []

        for asteroid in self.asteroids[:]:
            #print('asteroid',i)
            i+=1
            asteroid.move(delta)
            if(asteroid.x>resolution_x or asteroid.x<0 or asteroid.y>resolution_y or asteroid.y<0):
                if(asteroid.boss):
                    asteroid.speed *=-1
                else:
                    self.asteroids.remove(asteroid)
        
        

        for bullet in self.bullets[:]:    
            for asteroid in self.asteroids[:]:
                    if(self.collide(bullet.x,bullet.y,bullet.sizeX,bullet.sizeY,asteroid.x,asteroid.y,asteroid.sizeX,asteroid.sizeY)):
                        bullet.health-=1
                        if(bullet.health<=0):
                            bulletsRemove.append(bullet)
                        if(not bullet.superNova):
                            asteroidsHitNormal.append(asteroid)
                        asteroidsHit.append(asteroid)
                        asteroid.health-=1
                        if asteroid.health<=0:
                            asteroidsRemove.append(asteroid)
        
        bulletsRemove = list(dict.fromkeys(bulletsRemove))
        asteroidsRemove = list(dict.fromkeys(asteroidsRemove))
        asteroidsHit = list(dict.fromkeys(asteroidsHit))
        asteroidsHitNormal = list(dict.fromkeys(asteroidsHitNormal))

        #print(asteroidsRemove)

        for asteroid in asteroidsHitNormal[:]:
            if(self.superCharge<self.superMaxCharge):
                self.superCharge+=1
            self.score+=50

        for asteroid in asteroidsHit[:]:
            self.score+=50

        for bullet in bulletsRemove[:]: 
            self.bullets.remove(bullet)
        
        for asteroid in asteroidsRemove[:]: 
            self.asteroids.remove(asteroid)
            if asteroid == self.boss:
                self.currentLevel=3
                for asteroid in self.asteroids[:]: 
                    self.asteroids.remove(asteroid)

                for bullet in self.bullets[:]: 
                    self.bullets.remove(bullet)
                break
            
            

        for asteroid in self.asteroids[:]:
            #print(self.ship.x,self.ship.y,self.ship.sizeX,self.ship.sizeY,asteroid.x,asteroid.y,asteroid.sizeX,asteroid.sizeY)
            if(self.collide(self.ship.x,self.ship.y,self.ship.sizeX,self.ship.sizeY,asteroid.x,asteroid.y,asteroid.sizeX,asteroid.sizeY)):
                asteroid.health-=1
                if asteroid.health<=0:
                    self.asteroids.remove(asteroid)
                self.lives -= 1
                if(self.lives<=0):
                    self.running = False
        
        if self.scoreToLevel <= self.score and self.currentLevel == 1:
            self.currentLevel = 2
            self.lives +=3
            self.ship.x = 0
            self.ship.y = resolution_y/2

            for asteroid in self.asteroids[:]: 
                self.asteroids.remove(asteroid)

            for bullet in self.bullets[:]: 
                self.bullets.remove(bullet)

            nao_eh_homem.play()
            
            asteroid = Asteroid(boss=True)
            self.boss = asteroid
            self.asteroids.append(asteroid)
        
        if not self.running:
            self.asteroids=[] 

            #self.bullets=[] 

        self.launchSuper = False


    def actors_draw( self ):
        self.background.draw( self.screen )

        if not self.running:
            self.tutorialImg.draw(self.screen)
            self.startLabel.draw(self.screen)

        for bullet in self.bullets:
            bullet.draw(self.screen)
        
        for asteroid in self.asteroids:
            asteroid.draw(self.screen)

        self.ship.draw(self.screen,self.charge)

        self.timeLabel = Text('Tempo:'+str(self.duration),0,0,30)
        self.scoreLabel = Text('score:'+str(self.score),800,0,30)
        self.livesLabel = Text(str(self.lives)+' vidas',1300,0,30)

        if(self.superCharge>=self.superMaxCharge):
            color = (255,255,0)
        else:
            color = (255,255,255)
        self.superLabel = Text(str(self.superCharge)+'/'+str(self.superMaxCharge),800,800,30,color = color)
        

        self.scoreLabel.draw(self.screen)
        self.timeLabel.draw(self.screen)
        self.livesLabel.draw(self.screen)
        self.superLabel.draw(self.screen)

        if self.currentLevel == 2:
            self.bossLabel = Text(str(self.boss.health)+'/100',1300,800,30)
            self.bossLabel.draw(self.screen)

        if self.currentLevel == 3:
            self.endingLabel.draw(self.screen)
    # actors_draw()

    def spawn_asteroids( self,dt,delta ):
        if self.timer <=0 and self.currentLevel==1:
            asteroid = Asteroid()
            self.asteroids.append(asteroid)
            #print('asteroid')

            if self.duration <= 2000:
                self.timer =500
            elif self.duration <= 5000:
                self.timer =300
            elif self.duration <= 8000:
                self.timer =200
            elif self.duration <= 10000:
                self.timer =100
            elif self.duration <= 15000:
                self.timer =50
            else:
                self.timer =20
        elif self.timer <=0 and self.currentLevel==2:

            degrees =[90,45,135]

            for degree in degrees:
                asteroid = Asteroid(x=self.boss.x-150,y=self.boss.y+100,direction=degree)
                self.asteroids.append(asteroid)

            #print('asteroid')

            self.timer =100

    
    def collide(self,x1,y1,xsize1,ysize1,x2,y2,xsize2,ysize2):
        
        newX1=x1+xsize1/2
        newY1=y1+ysize1/2
        if(
            newX1  < x2 + xsize2 / 2 and newX1> x2 - xsize2 / 2 and 
            newY1 < y2 + ysize2 / 2 and newY1 > y2 - xsize2 / 2
        ):
            return True
        
        newX1=x1
        newY1=y1+ysize1/2
        if(
            newX1  < x2 + xsize2 / 2 and newX1> x2 - xsize2 / 2 and 
            newY1 < y2 + ysize2 / 2 and newY1 > y2 - xsize2 / 2
        ):
            return True
        
        newX1=x1-xsize1/2
        newY1=y1+ysize1/2
        if(
            newX1  < x2 + xsize2 / 2 and newX1> x2 - xsize2 / 2 and 
            newY1 < y2 + ysize2 / 2 and newY1 > y2 - xsize2 / 2
        ):
            return True
        
        newX1=x1+xsize1/2
        newY1=y1
        if(
            newX1  < x2 + xsize2 / 2 and newX1> x2 - xsize2 / 2 and 
            newY1 < y2 + ysize2 / 2 and newY1 > y2 - xsize2 / 2
        ):
            return True
        
        newX1=x1-xsize1/2
        newY1=y1
        if(
            newX1  < x2 + xsize2 / 2 and newX1> x2 - xsize2 / 2 and 
            newY1 < y2 + ysize2 / 2 and newY1 > y2 - xsize2 / 2
        ):
            return True
        
        newX1=x1+xsize1/2
        newY1=y1-ysize1/2
        if(
            newX1  < x2 + xsize2 / 2 and newX1> x2 - xsize2 / 2 and 
            newY1 < y2 + ysize2 / 2 and newY1 > y2 - xsize2 / 2
        ):
            return True
        
        newX1=x1
        newY1=y1-ysize1/2
        if(
            newX1  < x2 + xsize2 / 2 and newX1> x2 - xsize2 / 2 and 
            newY1 < y2 + ysize2 / 2 and newY1 > y2 - xsize2 / 2
        ):
            return True
        
        newX1=x1-xsize1/2
        newY1=y1-ysize1/2
        if(
            newX1  < x2 + xsize2 / 2 and newX1> x2 - xsize2 / 2 and 
            newY1 < y2 + ysize2 / 2 and newY1 > y2 - xsize2 / 2
        ):
            return True
        
        return False

    def loop( self ):
        """
        Laço principal
        """
        # Criamos o fundo
        self.background = Background()

        # Inicializamos o relogio e o dt que vai limitar o valor de
        # frames por segundo do jogo
        clock         = pygame.time.Clock()
        dt            = 16

        pygame.mixer.music.load("../audio/chiptune.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.2)
        # assim iniciamos o loop principal do programa
        while self.run:
            delta = clock.tick( 1000 / dt ) / 1000
            #print(delta)
            # Handle Input Events
            self.handle_events()

            # Cria asteroides
            self.spawn_asteroids( dt,delta )

            # Atualiza Elementos
            self.actors_update( dt,delta )

            # Desenhe para o back buffer
            self.actors_draw()
            
            
            if self.running:
                if self.currentLevel != 3:
                    self.duration += delta * 1000

                self.timer -= delta * 1000

            # ao fim do desenho temos que trocar o front buffer e o back buffer
            pygame.display.flip()

            

            #print(self.timer)

            #print(self.ship.x,self.ship.y,self.ship.sizeX,self.ship.sizeY)
                  
            if self.debug:
                self.ship.printAll()

            #print ("FPS: %0.2f" % clock.get_fps())
        # while self.run
    # loop()
# Game


def usage():
    """
    Imprime informações de uso deste programa.
    """
    prog = sys.argv[ 0 ]
    print("Usage:")
    print("\t%s [-f|--fullscreen] [-r <XxY>|--resolution=<XxY>]" % prog)
    print()
# usage()



def parse_opts( argv ):
    """
    Pega as informações da linha de comando e retorna 
    """
    # Analise a linha de commando usando 'getopt'
    try:
        opts, args = getopt.gnu_getopt( argv[ 1 : ],
                                        "hfr:",
                                        [ "help",
                                          "fullscreen",
                                          "resolution=" ] )
    except getopt.GetoptError:
        # imprime informacao e sai
        usage()
        sys.exit( 2 )

    options = {
        "fullscreen":  False,
        "resolution": ( resolution_x, resolution_y ),
        }

    for o, a in opts:
        if o in ( "-f", "--fullscreen" ):
            options[ "fullscreen" ] = True
        elif o in ( "-h", "--help" ):
            usage()
            sys.exit( 0 )
        elif o in ( "-r", "--resolution" ):
            a = a.lower()
            r = a.split( "x" )
            if len( r ) == 2:
                options[ "resolution" ] = r
                continue

            r = a.split( "," )
            if len( r ) == 2:
                options[ "resolution" ] = r
                continue

            r = a.split( ":" )
            if len( r ) == 2:
                options[ "resolution" ] = r
                continue
    # for o, a in opts
    r = options[ "resolution" ]
    options[ "resolution" ] = [ int( r[ 0 ] ), int( r[ 1 ] ) ]
    return options
# parse_opts()



def main( argv ):
    #primeiro vamos verificar que estamos no diretorio certo para conseguir
    #encontrar as imagens e outros recursos, e inicializar o pygame com as
    #opcoes passadas pela linha de comando
    fullpath = os.path.abspath( argv[ 0 ] )
    dir = os.path.dirname( fullpath )
    os.chdir( dir )

    options = parse_opts( argv )
    game = Game( options[ "resolution" ], options[ "fullscreen" ] )
    game.loop()
# main()
        
# este comando fala para o python chamar o main se estao executando o script
if __name__ == '__main__':
    main( sys.argv )
