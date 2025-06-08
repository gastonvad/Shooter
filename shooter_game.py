#Создай собственный Шутер!

from pygame import *
from random import randint

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
win_width = 1500
win_height = 800
sccore = 0
window = display.set_mode(
    (win_width, win_height)
)
display.set_caption('Shooter Game')
background = transform.scale(
    image.load('galaxy.jpg'),
    (win_width, win_height)
)


FPS = 60
img_hero = 'rocket.png'
img_back = 'galaxy.jpg'
img_bullet = 'bullet.png'
img_enemy = 'ufo.png'
sccore = 0
max_lost = 3
lost = 0

goal = 20
font.init() 
font2 = font.SysFont(None, 36)
font3 = font.SysFont(None, 100)


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y,size_x, size_y ,player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 1430:
            self.rect.x += self.speed
        
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15,20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width-80)
            self.rect.y = 0
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


ship = Player('rocket.png',5,win_height - 100, 80, 100, 10)
monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

bullets = sprite.Group()

finish = False
run = True

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()
    if not finish:
        window.blit(background,(0,0))
        text = font2.render('Счёт:' + str(sccore), 1,(255,255,255))
        window.blit(text,(10, 20))

        text_lose = font2.render('Пропущено:'+str(lost),1,(255,255,255))
        window.blit(text_lose,(10, 50))

        text_lose2 = font3.render('Вы проиграли!',5, (255,0,0))
        win= font3.render('Вы выиграли!',5, (255,0,0))
        if lost > 3:
            window.blit(text_lose2, (750,400))
        
        monsters.update()
        bullets.update()
        ship.update()
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            sccore += 1
            monster = Enemy(img_enemy, randint(80, win_width-80), -40, 80,50,randint(1,5))
            monsters.add(monster)
        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(text_lose2, (200, 200))
        if sccore >= goal:
            finish = True
            window.blit(win, (200, 200)) 
        display.update()
        clock = time.Clock()
        clock.tick(FPS)
        
        
  