# fazer um sistema de carregar o tiro que aumenta o tamanho do tiro e a quantidade de vida que ele tem
#png andre guedes cartoon roubar imagens

import os, sys
import getopt

import pygame
from pygame.locals import *
import math
import random

images_dir = os.path.join( "..", "imagens" )

resolution_x = 1920
resolution_y = 1080

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

nave_img = pygame.image.load('asteroids_fake/imagens/nave.png')
bala_img = pygame.image.load('asteroids_fake/imagens/bala.png')
asteroid_img = pygame.image.load('asteroids_fake/imagens/asteroid.png')

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

    def draw( self, screen ):
        new_image = pygame.transform.rotate(self.image, self.direction)

        new_rect = new_image.get_rect(center = self.image.get_rect(topleft = (self.x,self.y)).center)
        
        screen.blit( new_image, new_rect )

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
    def __init__(self,direction,x,y):
        self.speed = 300
        self.direction = direction
        self.rotr = math.radians(self.direction)
        self.x = x
        self.y = y
        self.ysp = math.cos(self.rotr)
        self.xsp = math.sin(self.rotr)
        self.sizeX = 60
        self.sizeY = 60
        projectile = pygame.Surface( (self.sizeX,self.sizeY), pygame.SRCALPHA, 32 ).convert_alpha()
        #projectile.fill( ( 0, 0, 255 ) )
        #nave_img = pygame.transform.scale(nave_img, (20, 20))
        projectile.blit(pygame.transform.scale(bala_img, (self.sizeX,self.sizeY)),(0,0))
        self.image = projectile

    def move(self,delta):
        self.x -= float(self.xsp*delta*self.speed)
        self.y -= float(self.ysp*delta*self.speed)


    def draw( self, screen ):
        new_image = pygame.transform.rotate(self.image, self.direction)

        new_rect = new_image.get_rect(center = self.image.get_rect(topleft = (self.x,self.y)).center)
        
        screen.blit( new_image, new_rect )

class Asteroid:
    def __init__(self):
        self.speed = random.randint(80, 200)
        

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

    def move(self,delta):
        self.x -= float(self.xsp*delta*self.speed)
        self.y -= float(self.ysp*delta*self.speed)


    def draw( self, screen ):
        new_image = pygame.transform.rotate(self.image, self.direction)

        new_rect = new_image.get_rect(center = self.image.get_rect(topleft = (self.x,self.y)).center)
        
        screen.blit( new_image, new_rect )

class Text:
    def __init__(self,text,x,y,size):
        self.x = x
        self.y = y
        self.text = text
        self.my_font = pygame.font.SysFont('Comic Sans MS', size)

    def draw( self, screen ):
        text_surface = self.my_font.render(self.text, False, (255, 255, 255))
        
        screen.blit( text_surface, (self.x,self.y) )


class Game:
    screen      = None
    screen_size = None
    run         = True
    background  = None   
    ship = None 
    startLabel = None
    timeLabel = None
    scoreLabel = None
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
        self.startLabel = Text('Aperte Enter para iniciar',resolution_x/2,resolution_y/2,30)
        self.timeLabel = Text('teste1',200,100,30)
        self.scoreLabel = Text('teste2',1000,100,30)
        self.duration=0
        self.timer=0
        self.score=0
        self.running=True


    def handle_events( self ):
        """
        Trata o evento e toma a ação necessária.
        """
        for event in pygame.event.get():
            t = event.type
            if t in ( KEYDOWN, KEYUP ):
                k = event.key
        
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
                    if(not self.running):
                        self.running = True
                        self.game_start(self.size)
                elif k == K_SPACE:
                    self.shoot = True
                elif k == K_KP_ENTER:
                    if self.debug:
                        self.debug = False
                    else:
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
            self.ship.shoot()
            if(len(self.bullets)<5):
                bullet = Projectile(self.ship.direction,self.ship.x,self.ship.y)
                self.bullets.append(bullet)
                print('shoot')
        i=1
        for bullet in self.bullets[:]:
            #print('bullet',i)
            i+=1
            bullet.move(delta)
            if(bullet.x>resolution_x or bullet.x<0 or bullet.y>resolution_y or bullet.y<0):
                self.bullets.remove(bullet)  
        
        for asteroid in self.asteroids[:]:
            #print('asteroid',i)
            i+=1
            asteroid.move(delta)
            if(asteroid.x>resolution_x or asteroid.x<0 or asteroid.y>resolution_y or asteroid.y<0):
                self.asteroids.remove(asteroid)
        
        bulletsRemove = []
        asteroidsHit = []
        asteroidsRemove = []

        for bullet in self.bullets[:]:    
            for asteroid in self.asteroids[:]:
                    if(self.collide(bullet.x,bullet.y,bullet.sizeX,bullet.sizeY,asteroid.x,asteroid.y,asteroid.sizeX,asteroid.sizeY)):
                        bulletsRemove.append(bullet)
                        asteroidsHit.append(asteroid)
                        asteroidsRemove.append(asteroid)
        
        bulletsRemove = list(dict.fromkeys(bulletsRemove))
        asteroidsRemove = list(dict.fromkeys(asteroidsRemove))
        asteroidsHit = list(dict.fromkeys(asteroidsHit))

        for asteroid in asteroidsHit[:]:
            self.score+=100

        for bullet in bulletsRemove[:]: 
            self.bullets.remove(bullet)
        
        for asteroid in asteroidsRemove[:]: 
            self.asteroids.remove(asteroid)

        for asteroid in self.asteroids[:]:
            #print(self.ship.x,self.ship.y,self.ship.sizeX,self.ship.sizeY,asteroid.x,asteroid.y,asteroid.sizeX,asteroid.sizeY)
            if(self.collide(self.ship.x,self.ship.y,self.ship.sizeX,self.ship.sizeY,asteroid.x,asteroid.y,asteroid.sizeX,asteroid.sizeY)):
                self.asteroids.remove(asteroid)
                self.running = False
        
        if not self.running:
            for asteroid in self.asteroids[:]: 
                self.asteroids.remove(asteroid)

            for bullet in self.bullets[:]: 
                self.bullets.remove(bullet)




    def actors_draw( self ):
        self.background.draw( self.screen )
        for bullet in self.bullets:
            bullet.draw(self.screen)
        
        for asteroid in self.asteroids:
            asteroid.draw(self.screen)

        self.ship.draw(self.screen)

        self.timeLabel = Text('Tempo:'+str(self.duration),200,100,30)
        self.scoreLabel = Text('score:'+str(self.score),1000,100,30)
        self.startLabel = Text('Aperte P para reiniciar',resolution_x/2-100,resolution_y/2-100,30)

        self.scoreLabel.draw(self.screen)
        self.timeLabel.draw(self.screen)

        if not self.running:
            self.startLabel.draw(self.screen)
    # actors_draw()

    def spawn_asteroids( self,dt,delta ):
        if self.timer <=0:
            asteroid = Asteroid()
            self.asteroids.append(asteroid)
            print('asteroid')

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

    
    def collide(self,x1,y1,xsize1,ysize1,x2,y2,xsize2,ysize2):
        
        newX1=x1+xsize1/2
        newY1=y1+ysize1/2
        if(
            newX1  < x2 + xsize2 / 2 and x1> x2 - xsize2 / 2 and 
            newY1 < y2 + ysize2 / 2 and newY1 > y2 - xsize2 / 2
        ):
            return True
        
        newX1=x1
        newY1=y1+ysize1/2
        if(
            newX1  < x2 + xsize2 / 2 and x1> x2 - xsize2 / 2 and 
            newY1 < y2 + ysize2 / 2 and newY1 > y2 - xsize2 / 2
        ):
            return True
        
        newX1=x1-xsize1/2
        newY1=y1+ysize1/2
        if(
            newX1  < x2 + xsize2 / 2 and x1> x2 - xsize2 / 2 and 
            newY1 < y2 + ysize2 / 2 and newY1 > y2 - xsize2 / 2
        ):
            return True
        
        newX1=x1+xsize1/2
        newY1=y1
        if(
            newX1  < x2 + xsize2 / 2 and x1> x2 - xsize2 / 2 and 
            newY1 < y2 + ysize2 / 2 and newY1 > y2 - xsize2 / 2
        ):
            return True
        
        newX1=x1-xsize1/2
        newY1=y1
        if(
            newX1  < x2 + xsize2 / 2 and x1> x2 - xsize2 / 2 and 
            newY1 < y2 + ysize2 / 2 and newY1 > y2 - xsize2 / 2
        ):
            return True
        
        newX1=x1+xsize1/2
        newY1=y1-ysize1/2
        if(
            newX1  < x2 + xsize2 / 2 and x1> x2 - xsize2 / 2 and 
            newY1 < y2 + ysize2 / 2 and newY1 > y2 - xsize2 / 2
        ):
            return True
        
        newX1=x1
        newY1=y1-ysize1/2
        if(
            newX1  < x2 + xsize2 / 2 and x1> x2 - xsize2 / 2 and 
            newY1 < y2 + ysize2 / 2 and newY1 > y2 - xsize2 / 2
        ):
            return True
        
        newX1=x1-xsize1/2
        newY1=y1-ysize1/2
        if(
            newX1  < x2 + xsize2 / 2 and x1> x2 - xsize2 / 2 and 
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
                self.duration += delta * 1000

                self.timer -= delta * 1000

            # ao fim do desenho temos que trocar o front buffer e o back buffer
            pygame.display.flip()

            self.shoot = False

            print(self.timer)

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
