import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random
import math

WIDTH = 400
HEIGHT = 600
STAGE_WIDTH = 80
STAGE_HEIGHT = 10
JUMP_VELOCITY = -10
GRAVITY = 0.5

doodle_pos = [WIDTH / 2, HEIGHT - 50]
doodle_vel = [0, JUMP_VELOCITY]
platforms = [[100, 500]]
doodle_image = simplegui.load_image('doodle.png')
score = 0


def draw(canvas):
    global platforms, doodle_pos, doodle_vel, score

    Frame.set_canvas_background("white")

    canvas.draw_image(doodle_image, (20, 20), (40, 40), doodle_pos, (40, 40))
    canvas.draw_text("Score: " + str(score), (10, 20), 20, 'White')

    doodle_vel[1] += GRAVITY
    doodle_pos[0] += doodle_vel[0]
    doodle_pos[1] += doodle_vel[1]

    for platform in platforms:
        canvas.draw_polygon([(platform[0], platform[1]),
                             (platform[0] + STAGE_WIDTH, platform[1]),
                             (platform[0] + STAGE_WIDTH,
                              platform[1] + STAGE_HEIGHT),
                             (platform[0], platform[1] + STAGE_HEIGHT)], 1, 'black', 'black')

    for platform in platforms:
        if doodle_pos[1] + 20 > platform[1] and doodle_pos[1] + 20 < platform[1] + STAGE_HEIGHT:
            if doodle_pos[0] > platform[0] and doodle_pos[0] < platform[0] + STAGE_WIDTH:
                doodle_vel[1] = JUMP_VELOCITY
                score += 1

    platforms = [platform for platform in platforms if platform[1]
                 > -STAGE_HEIGHT]

    if random.random() < 0.02:
        x_pos = random.randint(0, WIDTH - STAGE_WIDTH)
        y_pos = platforms[-1][1] - random.randint(50, 200)
        platforms.append([x_pos, y_pos])


Frame = simplegui.create_frame("Doodle Jump", WIDTH, HEIGHT)
Frame.set_draw_handler(draw)

Frame.start()
