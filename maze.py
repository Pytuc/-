from pygame import *

class GameSprite(sprite.Sprite):
  def __init__(self, player_image, player_x, player_y, player_speed):
    super().__init__()
    self.image = transform.scale(image.load(player_image), (60, 60))
    self.speed = player_speed
    self.rect = self.image.get_rect()
    self.rect.x = player_x
    self.rect.y = player_y

  def reset(self):
    window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
  def update(self):
    keys = key.get_pressed()
    if keys[K_LEFT] and self.rect.x > 5:
      self.rect.x -= self.speed
    if keys[K_RIGHT] and self.rect.x < win_width - 80:
      self.rect.x += self.speed
    if keys[K_UP] and self.rect.y > 5:
      self.rect.y -= self.speed
    if keys[K_DOWN] and self.rect.y < win_width - 80:
      self.rect.y += self.speed

class Enemy(GameSprite):
  def __init__(self, player_image, player_x, player_y, player_speed):
    super().__init__(player_image, player_x, player_y, player_speed)
    self.direction = 'left'

  def update(self):
    if self.rect.x <= 470:
      self.direction = 'right'
    if self.rect.x > win_width - 85:
      self.direction = 'left'
    if self.direction == 'left':
      self.rect.x -= self.speed
    else:
      self.rect.x += self.speed

class Wall(sprite.Sprite):
  def __init__ (self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_height):
    super().__init__()
    self.color_1 = color_1
    self.color_2 = color_2
    self.color_2 = color_3
    self.width = wall_width
    self.height = wall_height
    self.rect_x = wall_x
    self.rect_y = wall_y
    self.image = Surface((self.width, self.height))
    self.image.fill((color_1, color_2, color_3))
    self.rect = self.image.get_rect()

  def draw_wall(self):
    window.blit(self.image, (self.rect.x, self.rect.y))
    
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Maze')
background = transform.scale(image.load('background.jpg'), (win_width, win_height))

player = Player('hero.png', 5, 420, 4)
monster = Enemy('cyborg.png', 620, 280, 2)
finish = GameSprite('treasure.png', 580, 420, 0)

w1 = Wall(154, 205, 50, 100, 20, 4500, 10)
w2 = Wall(154, 205, 50, 100, 480, 350, 10)
w3 = Wall(154, 205, 50, 100, 20, 10, 380)

game = True
final = False
clock = time.Clock()
FPS = 60

font.init()
font = font.Font(None, 70)
win = font.render('YOU WIN!', True, (255, 215, 0))
lose = font.render('YOU LOSE!', True, (180, 0, 0))

mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play()

money = mixer.Sound('money.ogg')
kick = mixer.Sound('kick.ogg')

while game:
  for e in event.get():
    if e.type == QUIT:
      game = False

  if final != True:
    window.blit(background, (0,0))
    player.update()
    monster.update()

    player.reset()
    monster.reset()
    finish.reset()

    w1.draw_wall()
    w2.draw_wall()
    w3.draw_wall()

    if sprite.collide_rect(player, monster) or sprite.collide_rect(player, w1) or sprite.collide_rect(player, w2) or sprite.collide_rect(player, w3):
      final = True
      window.blit(lose, (200, 200))
      kick.play()

    if sprite.collide_rect(player, finish):
      final = True
      window.blit(win, (200,200))
      money.play()

  display.update()
  clock.tick(FPS)
