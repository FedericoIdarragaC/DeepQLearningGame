from numpy import exp
import pygame
import random

AZUL = [59,124,255]
VERDE = [118,252,37]
ROJO = [214,6,6]
NEGRO = [0,0,0]
GRIS = [170,170,170]
BLANCO = [255,255,255]

ANCHO = 200
ALTO = 200

CENTRO = [ALTO/2,ANCHO/2]


class Jugador(pygame.sprite.Sprite):
    
    def __init__(self,color = AZUL):
        
        super().__init__()
        self.image = pygame.Surface([50,10])
        self.image.fill(color)
        
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 180
        self.velx = 15
        
        
    def move(self,action):
        if action == [1,0,0]:
            self.rect.x -= self.velx
        elif action == [0,0,1]:
            self.rect.x += self.velx
        elif action == [0,1,0]:
            self.rect.x += 0
            
        if self.rect.x < 0:
            self.rect.x = 0
            
        if self.rect.x > ANCHO-self.rect.width:
            self.rect.x = ANCHO-self.rect.width

        
class Goma(pygame.sprite.Sprite):           
    def __init__(self,pos_x,color = VERDE):
        super().__init__()
        self.image = pygame.Surface([15,15])
        self.image.fill(color)
        
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = 0
        self.vely = 6

        
    def update(self):
        self.rect.y += self.vely
        return self.rect.y

SPEED = 60

pygame.init()
class Juego:
    def __init__(self):
        self.pantalla = pygame.display.set_mode([ANCHO,ALTO])
        
        #Grupos
        self.jugadores = pygame.sprite.Group()
        self.gomas = pygame.sprite.Group()
        
        self.j1 = Jugador()
        self.jugadores.add(self.j1)
        
        px = random.randrange(15,ANCHO-15)
        self.g = Goma(px)
        self.gomas.add(self.g) 
        
        self.font = pygame.font.Font('font.ttf', 20)
        self.score = 0
        
        self.reloj = pygame.time.Clock()
        
        self._reiniciar()

    def _reiniciar(self):
        px = random.randrange(15,ANCHO-15)
        self.g.rect.y = 0
        self.g.rect.x = px
        
    def paso(self,mov):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        self.j1.move(mov)
        colision = pygame.sprite.spritecollide(self.j1,self.gomas,False)
        puntaje = 0
        end = False
        terminal = False
        if colision != []:
            terminal = True
            puntaje = 10
            self.score += 1
            self._reiniciar()
            
        if self.g.rect.y > 190:
            end = True
            terminal = True
            puntaje = -5
            self._reiniciar()
            
        self._dibujar()
        self.reloj.tick(SPEED)
        
        return puntaje,self.score,terminal,end


    def _dibujar(self):
        self.pantalla.fill(NEGRO)
        self.gomas.draw(self.pantalla)
        self.gomas.update()
        self.jugadores.draw(self.pantalla)
        self.jugadores.update()
        self.label = self.font.render("Puntaje: {0}".format(self.score), 1, (255,255,255))
        self.pantalla.blit(self.label, (10, 10))
        pygame.display.flip()
