import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random

w, h = 800, 600
game_started = False
num_plat = 1000
offset = [0, 0]


def camera(pos):
    return [pos[0]-offset[0], pos[1]-offset[1]]


def height(y):

    global h
    return h-y


class doodle:
    rebound = 7

    def __init__(self, pos):
        self.pos = pos
        self.vel = [0, 0]

    def nudge(self, x):
        self.vel[0] += x

    def update(self):
        self.pos[0] = (self.pos[0] + self.vel[0]) % w
        oldy = int(min(height(self.pos[1])//100, num_plat - 1))
        newy = int(min(height(self.pos[1]+self.vel[1])//100, num_plat - 1))
        if oldy != newy and self.vel[1] > 0 and pl[oldy].exists and pl[oldy].left < self.pos[0] < pl[oldy].right:
            self.vel[1] = min(-self.vel[1], -doodle.rebound)
            if random.random() > .7:
                pl[oldy].exists = False
        else:
            self.pos[1] += self.vel[1]
        self.vel[1] += .1
        clearance = 300
        if self.pos[1]-offset[1] < clearance:
            offset[1] = self.pos[1] - clearance
        if self.pos[1]-offset[1] > h+50:
            offset[0], offset[1] = 0, 0
            dd.pos[0], dd.pos[1] = w//2, h-200
            dd.vel[1] = 0
            for i in range(0, num_plat):
                pl[i].exists = True


class platform:
    def __init__(self):
        global w
        width = random.randrange(100, 160)
        self.left = random.randrange(25, w-(25+width))
        self.right = self.left + width
        self.exists = True


def keydown(key):
    if key == simplegui.KEY_MAP["left"]:
        dd.nudge(-2.5)
    elif key == simplegui.KEY_MAP["right"]:
        dd.nudge(2.5)


def keyup(key):
    if key == simplegui.KEY_MAP["left"]:
        dd.nudge(2.5)
    elif key == simplegui.KEY_MAP["right"]:
        dd.nudge(-2.5)


def draw(canvas):
    dd.update()
    canvas.draw_circle(camera(dd.pos), 5, 2, "White")
    for steps in range(100*int(offset[1]//100), int(h+offset[1]), 100):
        ind = height(steps)//100
        if ind < num_plat and pl[ind].exists:
            canvas.draw_line(camera([pl[ind].left, steps]), camera(
                [pl[ind].right, steps]), 4, "Yellow")
        canvas.draw_text(str(height(steps)), camera(
            [w-50, steps]), 12, "White")


def start_or_reset_game():
    global game_started, offset
    if not game_started:
        game_started = True
        frame.set_draw_handler(draw)
        frame.set_keydown_handler(keydown)
        frame.set_keyup_handler(keyup)

        start_button.set_text("Reset Game")
    else:
        game_started = False
        offset = [0, 0]
        dd.pos[0], dd.pos[1] = w // 2, h - 200
        dd.vel[1] = 0
        for i in range(0, num_plat):
            pl[i].exists = True
        frame.set_draw_handler(draw)

        start_button.set_text("Start Game")


frame = simplegui.create_frame("Doodle Jump", w, h)
frame.add_label("Doodle Jumping Game")
start_button = frame.add_button("Start Game", start_or_reset_game)

pl = [platform() for i in range(0, num_plat)]
pl[0].left, pl[0].right = 0, w
dd = doodle(camera([w//2, h-200]))

frame.start()
