import os
import pygame as pg

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
    global human1
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


def Exit():
    global running
    global DisableInput
    print("Some placeholder code for \"exiting\"")
    if not DisableInput:
        DisableInput = True
    else:
        running = False


# create display window
Icon = pg.image.load(os.path.join(os.path.dirname(__file__), 'assets', 'favicon.png'))
Favicon = pg.transform.scale(Icon, (256, 256))
pg.display.set_icon(Favicon)
SCREEN_HEIGHT = 700
SCREEN_WIDTH = 780
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption('Skrosses')

# load button images
# start_img = load_image("thonkpad.png", -1)
# exit_img = load_image("thonkpad.png", -1)

# create button instances
a1_place = Button(50, 70, 0.1)
b1_place = Button(300, 70, 0.1)
c1_place = Button(550, 70, 0.1)
a2_place = Button(50, 280, 0.1)
b2_place = Button(300, 280, 0.1)
c2_place = Button(550, 280, 0.1)
a3_place = Button(50, 490, 0.1)
b3_place = Button(300, 490, 0.1)
c3_place = Button(550, 490, 0.1)

def place_tile():
    global human1
    global DisableInput
    global NoughtTurn
    if DisableInput:
        print("Input is disabled,", human1)
    else:
        print("Place", human1)
        if ValidMove.count(human1.lower()) == 0 or not b.get(human1.lower()) == " ":
            print("Invalid move")
        elif NoughtTurn:
            b[human1.lower()] = Nought
        elif not NoughtTurn:
            b[human1.lower()] = Cross
        if NoughtTurn:
            NoughtTurn = False
        else:
            NoughtTurn = True
    check_match()


def check_match():
    global NoughtTurn
    global Winner
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
                break
            if row_counter > 2:
                row_counter = 0
                matches = 0
        increment = increment + 1
    if " " not in [*b.values()] and Winner == "none":
        Winner = "Draw!"
        # Passes turn to the next player if neither of the criteria matches
    print("The Winner is", Winner, "Is it nought turn?",NoughtTurn)


# game loop
running = True
while running:
    screen.fill((0, 15, 38))

    if a1_place.draw(screen):
        human1 = "a1"
        place_tile()
    if b1_place.draw(screen):
        human1 = "b1"
        place_tile()
    if c1_place.draw(screen):
        human1 = "c1"
        place_tile()
    if a2_place.draw(screen):
        human1 = "a2"
        place_tile()
    if b2_place.draw(screen):
        human1 = "b2"
        place_tile()
    if c2_place.draw(screen):
        human1 = "c2"
        place_tile()
    if a3_place.draw(screen):
        human1 = "a3"
        place_tile()
    if b3_place.draw(screen):
        human1 = "b3"
        place_tile()
    if c3_place.draw(screen):
        human1 = "c3"
        place_tile()
    # Button.update()

    # event handler
    for event in pg.event.get():
        if event.type == pg.QUIT:
            Exit()
        elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            Exit()
    pg.display.update()

pg.quit()
