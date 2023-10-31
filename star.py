from time import sleep

from pygame import *
from random import randint


# нам потрібні такі картинки:
img_back = "back.jpg"  # фон гри
img_hero = "hero.png"  # герой
img_enemy1 = "enemy1.png"
img_bull = "bullet.png"
img_enemy2 = "enemy2.png"

score = 0  # збито ворогів
lost = 0  # пропущено ворогів
max_lost = 5
goal = 25

font.init()
font2 = font.Font(None, 36)
win = font2.render("YOU WIN!", True,0,(0, 255, 0))
lose = font2.render("YOU LOSE!", True,0, (255, 0, 0))

# клас-батько для інших спрайтів
class GameSprite(sprite.Sprite):
    # конструктор класу
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # викликаємо конструктор класу (Sprite):
        sprite.Sprite.__init__(self)
        # кожен спрайт повинен зберігати властивість image - зображення
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        # кожен спрайт повинен зберігати властивість rect - прямокутник, в який він вписаний
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    # метод, що малює героя на вікні
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


# клас головного гравця
class Player(GameSprite):

    # метод для керування спрайтом стрілками клавіатури
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    # метод "постріл" (використовуємо місце гравця, щоб створити там кулю)
    def fire(self):
        bullet = Bullet(img_bull, self.rect.centerx, self.rect.top, 25, 30, 15)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost

        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

# створюємо віконце
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

# створюємо спрайти
ship = Player(img_hero, 5, win_height - 100, 70, 90, 10)
monsters = sprite.Group()
for i in range(5):
    monster1 = Enemy(img_enemy1, randint(80, win_width - 80), -40, 80,  60, randint(1,5))
    monsters.add(monster1)
for i in range (2):
    monster2 = Enemy(img_enemy2, randint(40, win_width - 40), -40, 60, 40, randint(1, 4))
    monsters.add(monster2)



bullets = sprite.Group()
# змінна "гра закінчилася": як тільки вона стає True, в основному циклі перестають працювати спрайти
finish = False

# Основний цикл гри:
run = True  # прапорець скидається кнопкою закриття вікна

while run:
    # подія натискання на кнопку Закрити
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                ship.fire()

    if not finish:
        # оновлюємо фон
        window.blit(background, (0, 0))

        text = font2.render("Рахунок: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        # рухи спрайтів
        ship.update()
        monsters.update()
        bullets.update()
        # оновлюємо їх у новому місці при кожній ітерації циклу
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)

        #перевірка зіткнення кулі і монстрів
        colides = sprite.groupcollide(monsters, bullets, True, True)
        for c in colides:
            score += 1
            if score % 2 == 0:
                monster1 = Enemy(img_enemy1, randint(80, win_width - 80), -40, 80, 60, randint(1, 5))
                monsters.add(monster1)
            else:
                monster2 = Enemy(img_enemy2, randint(40, win_width - 40), -40, 60, 40, randint(1, 4))
                monsters.add(monster2)

        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))

        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        display.update()
    # цикл спрацьовує кожні 0.05 секунд
    time.delay(50)