import keyboard as k
import time, os

FPS = 0.05
WD = 30
HG = 20
GR_N = '   '
GR_BALL = ' * '
GR_BAR = '[ ]'
GR_WALL = '███'
GR_BRICK_L = '[  '
GR_BRICK_R = '  ]'

# INIT
BAR_LN = 7
BALL_X = 3
BALL_Y = HG-4
BALL_SP_X = 1
BALL_SP_Y = -1
MAP = [[GR_N for i in range(WD+2)] for j in range(HG+2)]
# walls
MAP[0] = [GR_WALL for i in range(WD+2)]
for l in range(HG+2):
    MAP[l][0] = MAP[l][-1] = GR_WALL
MAP[-1] = MAP[0]
BAR_POS = int((WD/2) - (BAR_LN/2))
#bricks
for i in range(2,WD-2,2):
    MAP[3][i] = GR_BRICK_L
    MAP[3][i+1] = GR_BRICK_R
    MAP[5][i] = GR_BRICK_L
    MAP[5][i + 1] = GR_BRICK_R

def paint_bar():
    #cleaning bar track
    MAP[-3] = [GR_N for i in range(WD+2)]
    MAP[-3][0] = MAP[-3][-1] = GR_WALL

    for i in range(BAR_LN):
       MAP[-3][BAR_POS + i] = GR_BAR


def break_brick(y, x):
    if MAP[y][x]==GR_BRICK_L:
        MAP[y][x] = MAP[y][x+1] = GR_N
    else:
        MAP[y][x] = MAP[y][x-1] = GR_N


def print_map(old_ball):

    print('\n')
    #[print(GR_WALL, end='') for w in range(WD+2)]
    print()

   # ball
    MAP[old_ball[0]][old_ball[1]] = GR_N
    MAP[BALL_Y][BALL_X] = GR_BALL

    paint_bar()
    for line in MAP:
    #    print(GR_WALL, end='')
        for pixel in line:
            print(pixel, end='')
        print()

    #[print(GR_WALL, end='') for w in range(WD+2)]
    print('\n\n\n\n')

while True:
    # move bar
    try:
        if k.is_pressed('a'):
            if BAR_POS > 1:
                BAR_POS -= 1
        elif k.is_pressed('d'):
            if BAR_POS + BAR_LN < WD+1:
                BAR_POS += 1
    except:
        break

    # move ball
    old_ball = (BALL_Y, BALL_X)
    # new_ball
    corner = False
    if BALL_X in [0, WD-1]:
        BALL_SP_X = -BALL_SP_X
        corner = True
    if BALL_Y in [0, HG-1]:
        BALL_SP_Y = -1
        corner = True

    # if not corner:
    #     if MAP[BALL_Y][BALL_X+1] != GR_N:
    #         BALL_SP_X = -1
    #     elif MAP[BALL_Y][BALL_X-1] != GR_N:
    #         BALL_SP_X = 1
    #     if MAP[BALL_Y+1][BALL_X] != GR_N:
    #         BALL_SP_Y = -1
    #         if MAP[BALL_Y+1][BALL_X] == GR_BAR:
    #             # ball tilt - middle bounce does not change X speed
    #             if BALL_X < BAR_POS + int(BAR_LN/2):
    #                 BALL_SP_X = -1
    #             elif BALL_X >= BAR_POS + int(BAR_LN/2):
    #                 BALL_SP_X = 1
    #
    #    elif MAP[BALL_Y-1][BALL_X] != GR_N:
    #        BALL_SP_Y = 1

    # next calculated move
    #
    if MAP[BALL_Y+BALL_SP_Y][BALL_X] != GR_N:
        if BALL_SP_Y == 1 and MAP[BALL_Y + 1][BALL_X] == GR_BAR:
                 # ball tilt - middle bounce does not change X speed
                 if BALL_X < BAR_POS + int(BAR_LN/2):
                     BALL_SP_X = -1
                 elif BALL_X >= BAR_POS + int(BAR_LN/2):
                     BALL_SP_X = 1
        if MAP[BALL_Y + BALL_SP_Y][BALL_X] in [GR_BRICK_R, GR_BRICK_L]:
            break_brick(BALL_Y + BALL_SP_Y,BALL_X)

        BALL_SP_Y = -BALL_SP_Y
    if MAP[BALL_Y][BALL_X + BALL_SP_X] != GR_N:
        if MAP[BALL_Y][BALL_X + BALL_SP_X] in [GR_BRICK_R, GR_BRICK_L]:
            break_brick(BALL_Y,BALL_X + BALL_SP_X)
        BALL_SP_X = -BALL_SP_X

    if MAP[BALL_Y + BALL_SP_Y][BALL_X + BALL_SP_X] != GR_N and MAP[BALL_Y + BALL_SP_Y][BALL_X] == GR_N and MAP[BALL_Y][BALL_X + BALL_SP_X] == GR_N:
        print('if')
        if MAP[BALL_Y + BALL_SP_Y][BALL_X + BALL_SP_X] in [GR_BRICK_R, GR_BRICK_L]:
            print('IN')
            break_brick(BALL_Y + BALL_SP_Y,BALL_X + BALL_SP_X)
        BALL_SP_X = -BALL_SP_X
        BALL_SP_Y = -BALL_SP_Y

    BALL_Y, BALL_X = BALL_Y + BALL_SP_Y, BALL_X + BALL_SP_X

    if BALL_Y == HG-1:
        print('\no shit')
        break

    print_map(old_ball)
    time.sleep(FPS)
    os.system('cls' if os.name == 'nt' else 'clear')


