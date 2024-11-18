import pygame
import sys
from random import choice
from pygame.locals import *

WIDTH = 480 
HEIGHT = 600
FPS = 30

# variabel warna
#        RED  GREEN BLUE
WHITE = (255, 255, 255) 
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Flappy bird clone')
clock = pygame.time.Clock()

# Game variables
gravity = 0
score = 0
pos_list = [[-300, 350], [-400, 250], [-200, 450], [-450, 150], [-50, 550]]


def create_pipa():
    y_pos = choice(pos_list)
    p1 = Top(y_pos[0])
    p2 = Bottom(y_pos[1])
    detection = DetectionPoint(p2.rect.x, y_pos[1])
    pipas.add(p1)
    pipas.add(p2)
    all_sprites.add(p1)
    all_sprites.add(p2)
    detect_group.add(detection)
    all_sprites.add(detection)
    
def show_text(text, font_size, font_color, x,y):
    font = pygame.font.SysFont(None, font_size)
    font_surface = font.render(text, True, font_color)
    screen.blit(font_surface, (x,y))
    
def game_over_screen():
    screen.fill(BLACK)
    show_text("Game Over", 40, RED, WIDTH//2 - 65, HEIGHT//4)
    show_text("Score Kamu = {}".format(score), 25, WHITE, WIDTH//2 - 50, HEIGHT//3 + 100)
    show_text("Press any key to continue", 25, WHITE, WIDTH//2 - 95, HEIGHT//4 + 50 )
    
    pygame.display.flip()
    waiting_game_over = True
    while waiting_game_over:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == KEYUP:
                waiting_game_over = False
                

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = HEIGHT // 2
        
    def update(self):
        global game_over
        if self.rect.y > HEIGHT:
            game_over = True 
        if self.rect.y <= 0:
            self.rect.y = 0
        
        
class Pipa(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 500))
        self.image.fill(GREEN)        
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH + 10
        
    def update(self):
        self.rect.x -= 4
        if self.rect.x < -20:
            self.kill()
        
        
class Top(Pipa):
    def __init__(self, y):
         super().__init__()
         self.rect.y = y
         
         
class Bottom(Pipa):
    def __init__(self, y):
         super().__init__()
         self.rect.y = y
         
         
class DetectionPoint(pygame.sprite.Sprite):
    def __init__(self, x,y):
        super().__init__()
        self.image = pygame.Surface((20, 120))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = y
        self.hit = False
        
    def update(self):
        self.rect.x -= 4
        if self.rect.x < -20:
            self.kill()
             
        
all_sprites = pygame.sprite.Group()
pipas = pygame.sprite.Group()
detect_group = pygame.sprite.Group()
bird = Bird()
  
create_pipa()
    
all_sprites.add(bird)        

# Game loop
game_over = False 
run = True
while run:
    if game_over:
        game_over_screen()
        all_sprites = pygame.sprite.Group()
        pipas = pygame.sprite.Group()
        detect_group = pygame.sprite.Group()
        bird = Bird()
  
        create_pipa()
    
        all_sprites.add(bird)
        score = 0
        game_over = False
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                gravity = 0
                gravity -= 5
    
    gravity += 0.25
    bird.rect.y += gravity
    
    # check collision bird dengan detection point (score)
    bird_hit_point = pygame.sprite.spritecollide(bird, detect_group, False)
    if bird_hit_point and not bird_hit_point[0].hit:
        score += 1
        bird_hit_point[0].hit = True
      
        
    # check collision bird dengan pipa
    bird_hit_pipa = pygame.sprite.spritecollide(bird, pipas, False)
    if bird_hit_pipa:
        game_over = True 
        
    
    if len(pipas) <= 0:
        create_pipa()
    
    all_sprites.update()
    screen.fill(BLACK)        
    all_sprites.draw(screen)
    show_text(str(score), 32, WHITE, WIDTH//2, HEIGHT//4 - 100)
     
    pygame.display.flip()

pygame.quit()
