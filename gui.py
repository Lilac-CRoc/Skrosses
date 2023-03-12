import os, time
import pygame as pg

# Settings for quick changes
frames = int(3)
button_image = "button1.png"
nought_image = "button2.png"
cross_image = "button3.png"
favicon_image = "favicon.png"
nwin_image = "nwin.png"
cwin_image = "cwin.png"
nturn_image = "nturn.png"
cturn_image = "cturn.png"
exit_image = "exit.png"
draw_image = "draw.png"
background_dir = "bg.png"


# functions to create our resources
main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "assets")

# Create variables
human1 = "Dummy Variable"
Blank = " "
Nought = "○"
Cross = "X"
Winner = "none"
Playing = True
NoughtTurn = False
Ask = True
DisableInput = False
b = {'a1': Blank, 'a2': Blank, 'a3': Blank, 'b1': Blank, 'b2': Blank,
     'b3': Blank, 'c1': Blank, 'c2': Blank, 'c3': Blank}
ValidMove = ['a1', 'a2', 'a3', 'b1', 'b2', 'b3', 'c1', 'c2', 'c3']
check = []

def load_image(name, colorkey=None, scale=1):
    fullname = os.path.join(data_dir, name)
    image = pg.image.load(fullname)
    image = image.convert()

    size = image.get_size()
    size = (size[0] * scale, size[1] * scale)
    image = pg.transform.scale(image, size)

    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pg.RLEACCEL)
    return image, image.get_rect()


class Button():
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.sprites = []
        self.is_animating = False
        for i in range(frames):
            self.sprites.append(pg.image.load(os.path.join(data_dir,"button"+str(i+1)+".png")))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
       
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x,pos_y]
        
    def n_update(self):
        self.current_sprite = 1 
        self.image = self.sprites[self.current_sprite]
        
    def c_update(self):
        self.current_sprite = 2
        self.image = self.sprites[self.current_sprite]
        
    def reset(self):
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        
    """
    def __init__(self, x, y, scale):
        self.image, self.rect = load_image("button.png", -1, 2)
        self.rect.topleft = (x, y)
        self.clicked = False
    
    def update(self):
        try:
            if b[human1.lower()] == Nought:
                self.image = load_image("nought.png")
            elif b[human1.lower()] == Cross:
                self.image = load_image("cross.png")
        except KeyError:
            pass
    """
            
    def draw(self, surface):
        action = False
        # get mouse position
        pos = pg.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True
        if pg.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))
        return action


class Status(pg.sprite.Sprite):
    global Winner
    global NoughtTurn
    
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.sprites = []
        self.sprites.append(pg.image.load(os.path.join(data_dir,exit_image)))
        self.sprites.append(pg.image.load(os.path.join(data_dir,nturn_image)))
        self.sprites.append(pg.image.load(os.path.join(data_dir,cturn_image)))
        self.sprites.append(pg.image.load(os.path.join(data_dir,nwin_image)))
        self.sprites.append(pg.image.load(os.path.join(data_dir,cwin_image)))
        self.sprites.append(pg.image.load(os.path.join(data_dir,draw_image)))
        self.status_sprite = 1
        self.image = self.sprites[self.status_sprite]
       
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x,pos_y]
        
    def update(self):
        if Winner == "none":
            if NoughtTurn:
                self.status_sprite = 1
            else:
                self.status_sprite = 2
        elif Winner == "○":
                self.status_sprite = 3
        elif Winner == "X":
            self.status_sprite = 4
        else:
            self.status_sprite = 5
        self.image = self.sprites[self.status_sprite]
                
"""
def Exit():
    global running
    global DisableInput
    if not DisableInput:
        DisableInput = True
        print("Some placeholder code for \"exiting\"")
    elif pg.key == pg.K_ESCAPE or event.type == pg.QUIT:
        running = False
"""    


# create display window
Icon = pg.image.load(os.path.join(os.path.dirname(__file__), "assets", favicon_image))
Favicon = pg.transform.scale(Icon, (256, 256))
pg.display.set_icon(Favicon)
SCREEN_HEIGHT = 700
SCREEN_WIDTH = 780
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
background = pg.image.load(os.path.join(data_dir,background_dir))
pg.display.set_caption("Skrosses")


# create button instances & groups
status_bar = pg.sprite.Group()
status = Status(250,0)
status_bar.add(status)

a1_place = Button(70, 110)
b1_place = Button(320, 110)
c1_place = Button(570, 110)
a2_place = Button(70, 320)
b2_place = Button(320, 320)
c2_place = Button(570, 320)
a3_place = Button(70, 530)
b3_place = Button(320, 530)
c3_place = Button(570, 530)

def place_tile():
    global human1
    global DisableInput
    global NoughtTurn
    if DisableInput:
        pass
        # print("Input is disabled,", human1)
    else:
        # print("Place", human1)
        if ValidMove.count(human1.lower()) == 0 or not b.get(human1.lower()) == " ":
            # print("Invalid move")
            return False
        elif NoughtTurn:
            b[human1.lower()] = Nought
            NoughtTurn = False
            check_match() 
            return True
        elif not NoughtTurn:
            b[human1.lower()] = Cross
            NoughtTurn = True
            check_match()
            return True


def check_match():
    global NoughtTurn
    global Winner
    global DisableInput
    checking_side = "X"
    increment = 1
    # First checks for a winning combination. If not, check for if the board
    # is fully filled and declares a draw
    while True:
        matches = 0
        row_counter = 0
        if increment > 2:
            break
        elif increment == 2:
            checking_side = "○"
        check_grid = ['a1', 'a2', 'a3', 'b1', 'b2', 'b3', 'c1', 'c2', 'c3', 'a1', 'b1', 'c1',
                      'a2', 'b2', 'c2', 'a3', 'b3', 'c3', 'a1', 'b2', 'c3', 'a3', 'b2', 'c1']
        for i in range(len(check_grid)):
            if checking_side == b[check_grid.pop()]:
                matches = matches + 1
            row_counter = row_counter + 1
            if matches == 3 and row_counter > 2:
                Winner = checking_side
                DisableInput = True
                # print("The Winner is", Winner)
                break
            if row_counter > 2:
                row_counter = 0
                matches = 0
        increment = increment + 1
    if " " not in [*b.values()] and Winner == "none":
        Winner = "Draw!"
        DisableInput = True
        # Passes turn to the next player if neither of the criteria matches


# game loop
running = True
while running:
    screen.fill((0, 15, 38))
    screen.blit(background,(0,0))   
    status_bar.update()  

    if a1_place.draw(screen):
        human1 = "a1"
        if place_tile():
            if not NoughtTurn:
                a1_place.n_update() 
            else:
                a1_place.c_update() 
    if b1_place.draw(screen):
        human1 = "b1"
        if place_tile():
            if not NoughtTurn:
                b1_place.n_update() 
            else:
                b1_place.c_update() 
    if c1_place.draw(screen):
        human1 = "c1"
        if place_tile():
            if not NoughtTurn:
                c1_place.n_update() 
            else:
                c1_place.c_update() 
    if a2_place.draw(screen):
        human1 = "a2"
        if place_tile():
            if not NoughtTurn:
                a2_place.n_update() 
            else:
                a2_place.c_update() 
    if b2_place.draw(screen):
        human1 = "b2"
        if place_tile():
            if not NoughtTurn:
                b2_place.n_update() 
            else:
                b2_place.c_update() 
    if c2_place.draw(screen):
        human1 = "c2"
        if place_tile():
            if not NoughtTurn:
                c2_place.n_update() 
            else:
                c2_place.c_update() 
    if a3_place.draw(screen):
        human1 = "a3"
        if place_tile():
            if not NoughtTurn:
                a3_place.n_update() 
            else:
                a3_place.c_update() 
    if b3_place.draw(screen):
        human1 = "b3"
        if place_tile():
            if not NoughtTurn:
                b3_place.n_update() 
            else:
                b3_place.c_update() 
    if c3_place.draw(screen):
        human1 = "c3"
        if place_tile():
            if not NoughtTurn:
                c3_place.n_update() 
            else:
                c3_place.c_update()   
    # event handler
    keys = pg.key.get_pressed()
    for event in pg.event.get():
    
        # Exits if "ESC" or QUIT event is called
        if event.type == pg.QUIT or keys[pg.K_ESCAPE]:
            exit("Quitting...")
        # Resets the board when "Q" is pressed
        elif keys[pg.K_r]:
            a1_place.reset()
            b1_place.reset()
            c1_place.reset()
            a2_place.reset()
            b2_place.reset()
            c2_place.reset()
            a3_place.reset()
            b3_place.reset()
            c3_place.reset()
            Winner = "none"
            NoughtTurn = False
            b.clear()
            b = {'a1': Blank, 'a2': Blank, 'a3': Blank, 'b1': Blank,
            'b2': Blank, 'b3': Blank, 'c1': Blank, 'c2': Blank, 'c3': Blank}
            # print("Resetting board")
            DisableInput = False

    status_bar.draw(screen)
    pg.display.update()

pg.quit()
