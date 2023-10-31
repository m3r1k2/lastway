import pygame
from random import randint
pygame.init()

width = 650
height = 650

font.init()
font2 = font.Font(None, 36)

move_right = False
move_left = False

window = pygame.display.set_mode((width, height))
back = pygame.transform.scale(pygame.image.load('BACK sp10.jpg'),(width, height))

clock = pygame.time.Clock()

score = 0 #набрано балів
goal = 50 # потрібно для перемоги
lost = 0 #пропущено ворогів




#AREA
class Area():
    def __init__(self, x=0, y=0, width =10, height =10, color=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.fill_color = back
        if color:
            self.fill_color = color

    def color(self, new_color):
        self.fill_color = new_color

    def fill(self):
        pygame.draw.rect(window,self.fill_color,self.rect)

    def collidepoint(self, x, y):
        return self.rect.collidepoint(x, y)

    def colliderect(self, rect):
        return self.rect.colliderect(rect)

#label
class Label(Area):
    def set_text(self, text, fsize=12, text_color=(0, 0, 0)):
        self.image = pygame.font.SysFont('verdana', fsize).render(text, True, text_color)
    def draw(self, shift_x=0, shift_y=0):
        self.fill()
        window.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))


#Picture
class Picture(Area):
    def __init__(self, filename, x=0, y=0, width=10, height=10):
        Area.__init__(self, x=x, y=y, width=width, height=height, color=None)
        self.image = pygame.transform.scale(pygame.image.load(filename), (width, height))

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))



hero = Picture('SPACESHIP1.png', 275, 550, 75,75)
enemy = Picture('TARGET.png', -25,0, 150,100)



game = True
while game:
    window.blit(back,(0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                move_right = True
            if event.key == pygame.K_LEFT:
                move_left = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                move_right = False
            if event.key == pygame.K_LEFT:
                move_left = False
    if move_right:
        hero.rect.x += 4
    if move_left:
        hero.rect.x -= 4

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
    hero.draw()
    enemy.draw()
    pygame.display.update()
    clock.tick(40)

    text = Label("Рахунок: " + str(score), 1, (255, 255, 255))
    window.blit(text, (10, 20))