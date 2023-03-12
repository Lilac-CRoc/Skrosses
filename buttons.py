"""" Tutorial from
www.youtube-nocookie.com/embed/hDu8mcAlY4E
"""
import pygame as pg
import sys, random, os

# Settings
screen_width = 800
screen_height = 600
background_dir = "favicon.png"
button_dir = "button.png"
button2_dir = "cross.png"
targets = int(20)

# Load assets without having to use CD
main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "assets")

# Classes
class mice(pg.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = pg.image.load(os.path.join(data_dir,image))
        self.rect = self.image.get_rect()
        self.clicksound = pg.mixer.Sound(os.path.join(data_dir,"click.ogg"))
        # self.image = pg.Surface([width, height])
        # self.rect.center = [pos_x, pos_y]
    def click(self, mouse_pos):
        self.clicksound.play()
        for target in target_group:
            dx = target.rect.centerx - mouse_pos[0]
            dy = target.rect.centery - mouse_pos[1]
            dist_sq = dx*dx + dy*dy
            radius = target.image.get_width() / 2
            if dist_sq < radius*radius:
                print("Collision was detected!")
                # pg.Surface.blit(self, os.path.join(data_dir,button2_dir), [dx,dy])
    def update(self):
        self.rect.center = pg.mouse.get_pos()


class Target(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y, image):
        super().__init__()
        self.image = pg.image.load(os.path.join(data_dir,image))
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]


# Setup
pg.init()
clock = pg.time.Clock()

# Screen
screen = pg.display.set_mode((screen_width,screen_height))
background = pg.image.load(os.path.join(data_dir,background_dir))
pg.mouse.set_visible(True)

# Init Groups
mice = mice("pixel.png")
mice_group = pg.sprite.Group()
mice_group.add(mice)

# Targets
target_group = pg.sprite.Group()
for target in range(targets):
    new_target = Target(random.randrange(0,screen_width), random.randrange(0,screen_height), button_dir)
    target_group.add(new_target)


# Main loop
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            pg.quit()
            sys.exit()
        if event.type == pg.MOUSEBUTTONDOWN:
            mice.click(event.pos)
    pg.display.flip()
    screen.blit(background,(0,0))
    target_group.draw(screen)
    mice_group.draw(screen)
    mice_group.update()
    clock.tick(60)
