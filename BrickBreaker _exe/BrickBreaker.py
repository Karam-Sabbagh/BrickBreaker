#'''press left or right arrows to move the paddle'''
#edit able:
# game settings:
canvas_width = 450  # 500 max to be playable.
free_hight_space = 435 # the free space after the lines of bricks.(435 recomended,350 min)
big_space = 20 # the space befor the first brick at each line of bricks(it could be 200 as max if the width is between 500 and 700)
between_bricks_spaces = 5  # the spaces between each brick at the bricks line(10 recomended).
between_lines_spaces = 20  # (the free spaces between each line)10 as recomended
first_line_hight = 50  # 50 recomended (20 min and 100 max)
lines_of_bricks = 4  # how many lines of bricks should be.(19 max)
bricks_in_line = 6 # this is for how many bricks in each line of bricks.(6 recomended, 2 min ,30 max)
time_limet = 70 # this is the limeted time to finish the game.(150 max)
# hint: if the the value is higher than its maximum value it will automaticly be set to its max and the same for min
# settings done.

#DON'T EDIT ANYTHING HERE BECAUSE THAT MAY CAUSE SOME ERRORS!

# imports:
# for sounds:
try:
    import pygame
    from pygame.locals import *
    pygame.init()
    hit_sound = pygame.mixer.Sound('Hit.wav')
    brick_hit_sound = pygame.mixer.Sound('break.wav')
    paddle_hit_sound = pygame.mixer.Sound('Paddle_hit.wav')
    pressed_keys = pygame.key.get_pressed()
except:
    pass
# other imports:
from tkinter import *
import random
import time

#game engin:
class Ball:
    def __init__(self, canvas, hight_place, color):
        self.canvas = canvas
        self.canvas_width = self.canvas.winfo_width()
        self.canvas_height = self.canvas.winfo_height()
        self.color = color
        self.id = canvas.create_oval(10, 10, 25, 25, fill=self.color)
        self.canvas.move(self.id, (self.canvas_width / 2), (self.canvas_height / 2))
        self.starts = [-1,-1.5,-2,2,1.5, 1]
        random.shuffle(self.starts)
        self.x = self.starts[0]
        self.y = 2
        self.hit_bottom = False
        self.hit_wall = False

    def restart(self):
        canvas.delete(self.id)
        self.id = canvas.create_oval(10, 10, 25, 25, fill=self.color)
        self.canvas.move(self.id, (self.canvas_width / 2), (self.canvas_height / 2))
        random.shuffle(self.starts)
        self.x = self.starts[0]
        self.y = 2

    def check(self):
        # makes the ball bounce when it touch the walls:
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        if pos[3] >= self.canvas_height:
            self.hit_bottom = True
        # walls bounce:
        if pos[1] <= 0:
            self.y = 3
            self.hit_wall = True
        if pos[0] <= 0:
            self.x = 3
            self.hit_wall = True
        if pos[2] >= self.canvas_width:
            self.x = -3
            self.hit_wall = True

        shadow_pos = (pos[3]+5)
        for i in range(1, 1):
            self.ball_shadow = canvas.create_oval(10, 10, 25, 25, fill=self.color)
            self.canvas.move(self.ball_shadow, (pos[2]+5), (shadow_pos))

class Paddle:
    def __init__(self, canvas, ball,hight, color):
        self.canvas = canvas
        self.hight = hight
        self.color = color
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=self.color)
        self.canvas.move(self.id, 200, self.hight)
        self.x = 0
        self.canvas_width = self.canvas.winfo_width()
        self.ball = ball
        self.ball_hit = False
        # this makes the controls for the paddle
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)

    def restart(self):
        canvas.delete(self.id)
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=self.color)
        self.canvas.move(self.id, 200, self.hight)
        self.x = 0

    def hit_paddle(self):
        ball_pos = self.canvas.coords(ball.id)
        pos = self.canvas.coords(self.id)
        if ball_pos[3] >= pos[1] and ball_pos[3] <= pos[3]:
            if ball_pos[2] >= pos[0] and ball_pos[0] <= pos[2]:
                return True
            return False

    def check(self):
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)
        ball_pos = self.canvas.coords(ball.id)
        ball_w_mid = ((ball_pos[0] + ball_pos[2]) / 2) # this is the position of the middle of the ball
        # ball bounce:
        if self.hit_paddle() == True:
            self.ball_hit = True
            if ball_w_mid > (pos[0]+35) and ball_w_mid < (pos[2]-35):
                ball.y = -3
            else:
                ball.y = -2

        # paddle movement limets:
        if pos[0] <= 0:
            self.x = 0
        elif pos[2] >= self.canvas_width:
            self.x = 0

    # this change the direction of the paddle left and right:
    def turn_left(self, evt):
        pos = self.canvas.coords(self.id)
        if pos[0] > 0: #that means if the paddle is not at the left wall.
            self.x = -2.25

    def turn_right(self, evt):
        pos = self.canvas.coords(self.id)
        if pos[2] < self.canvas_width: #that means if the paddle is not at the right wall
            self.x = 2.25

class Bricks:
    def __init__(self, canvas, ball, size, color, x, y):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, size, 13, fill=color)
        self.canvas.move(self.id, x, y)
        self.pos = self.canvas.coords(self.id)
        self.ball = ball

    # this two functions makes the limets for the sides of the bricks and used to let the ball bounce by making them true and false:
    def hit_brick_UD(self, pos, ball_pos, ball_w_mid):      # up and down sides of the brick:
        if ball_w_mid  >= pos[0] and ball_w_mid <= pos[2]:
            #down:
            if ball_pos[1] <= pos[3] and ball_pos[1] >= pos[1]:
                return True
            #up:
            if ball_pos[3] <= pos[3] and ball_pos[3] >= pos[1]:
                return True
            return False

    def hit_brick_LR(self, pos, ball_pos, ball_h_mid):      #right and left sides limets of the brick
        if ball_h_mid >= pos[1] and ball_h_mid <= pos[3]:
            #right:
            if ball_pos[0] >= pos[0] and ball_pos[0] <= pos[2]:
                return True
            #left:
            if ball_pos[2] <= pos[2] and ball_pos[2] >= pos[0]:
                return True
            return False

    def hit_brick(self):
        ball_pos = self.canvas.coords(self.ball.id)
        ball_w_mid = ((ball_pos[0] + ball_pos[2]) / 2)
        ball_h_mid = ((ball_pos[1] + ball_pos[3]) / 2)
        if self.hit_brick_LR(self.pos, ball_pos, ball_h_mid) == True or self.hit_brick_UD(self.pos, ball_pos, ball_w_mid) == True:
            return True
        return False

    # hint here the pos is the brick pos
    def check(self):
        pos = self.canvas.coords(self.id)
        ball_pos = self.canvas.coords(self.ball.id)
        ball_w_mid = ((ball_pos[0]+ball_pos[2])/2)
        ball_h_mid = ((ball_pos[1]+ball_pos[3])/2)
            # this makes the ball bounce when it touch the sides of the brick:
        # up and down sides of the brick:
        if self.hit_brick_UD(pos, ball_pos, ball_w_mid) == True:
            #down side of the brick:
            if ball_pos[1] <= pos[3] and ball_pos[1] >= pos[1]:
                ball.y = 2
            #up side of the brick
            if ball_pos[3] <= pos[3] and ball_pos[3] >= pos[1]:
                ball.y = -2

        #left and right sides of the brick bounce
        if self.hit_brick_LR(pos, ball_pos, ball_h_mid) == True:
            # right side of the brick:
            if ball_pos[0] >= pos[0] and ball_pos[0] <= pos[2]:
                ball.x = 2
            # left side of the brick:
            if ball_pos[2] <= pos[2] and ball_pos[2] >= pos[0]:
                ball.x = -2

# game engin done.
# interface
canvas_height = (((lines_of_bricks * (13 + between_lines_spaces)) + 50) + free_hight_space)
tk = Tk()
tk.title("Brick Breaker")
tk.resizable(0, 0)
tk.wm_attributes('-topmost', 1)
try:
    tk.iconbitmap('BrickBreaker.ico')
except:
    pass
canvas = Canvas(tk, width=canvas_width, height=canvas_height, bd=0,highlightthickness=0)  # width and height are a the top.
canvas.pack()
tk.update()

# sizes limets:
# bricks_in_line limets:
if bricks_in_line > 30:
    bricks_in_line = 30
# lines_of_bricks limets:
if lines_of_bricks > 20:
    lines_of_bricks = 19
# canvas_width limets:
if canvas_width > 500:
    canvas_width = 500
# free_hight_space limet:
if free_hight_space < 350:
    free_hight_space = 350
# big_space limets:
if big_space > 100:
    if canvas_width > 499 and canvas_width < 700:
        big_space = 100
# first_line_hight limets:
if first_line_hight < 20:
    first_line_hight = 200
if first_line_hight > 100:
    first_line_hight = 100
# time_limet limets:
if time_limet > 150:
    time_limet = 150
# bricks_in_Line limets:
if bricks_in_line < 2:
    bricks_in_line = 2

ball = Ball(canvas, ((canvas_height / 2) - 50), 'red')
paddle = Paddle(canvas, ball,canvas_height - 125, 'blue')

screen_middle = (canvas_width / 2), (canvas_height / 2)
def print_for_second(num):  # prints something on the screen for 1 second (for the start timer)
    try:
        text_num = canvas.create_text(screen_middle, font=("Purisa", 50), text=num)
        tk.update_idletasks()
        tk.update()
        time.sleep(1)
        canvas.delete(text_num)
    except:
        pass

def colors_chooser(colors):
    random.shuffle(colors)
    real_end = len(colors)
    end = int(real_end) - 1
    colors_chooser.brick_color = colors[end]
    colors.pop()

def restart__print(sentence, text, ball, paddle, breaks):
    sen = canvas.create_text(screen_middle, font=("Purisa", 50), text=sentence)
    tk.update_idletasks()
    tk.update()
    time.sleep(2)
    canvas.delete(sen)
    canvas.delete(text)
    canvas.delete(breaks)
    ball.hit_bottom = False
    ball.restart()
    paddle.restart()

def remove_bricks(objDict):
    for brick in dict(objDict).keys():  # look for all the bricks(objects) in the dictionary I have made when I made the objects for the Brick class.
        canvas.delete(objDict[brick])

canvas.create_text((canvas_width-76), (canvas_height-15), text='Made by : Karam Sabbagh')
canvas.create_text(35, 10, text='Timer:')
canvas.create_text(390, 10, text= 'Bricks breaked:')

pause = False
def resmue():
    global pause
    pause = False
    pause_btn.place(x=8, y=(canvas_height-50))
    paddle.x = 0

resmue_btn = Button(tk, text='resmue', width=20, height=1, bd='10', command=resmue)

def do_pause():
    global pause
    pause = True
    pause_btn.place(x = 3000, y = -2000)
    resmue_btn.place(x=(canvas_height/4), y=(canvas_height/2))
    while True:
        time.sleep(0.05)
        try:
            tk.update()
        except:
            break
        if pause == False:
            resmue_btn.place(x=3000, y= -2000)
            break

pause_btn = Button(tk, text='Pause', width= 5, height= 1, bd='10', command = do_pause)

def start():
    # colors (for bricks)
    colors = ['orange', 'green', 'gray', 'cyan', 'gold', 'silver', 'purple', 'pink']
    t0 = canvas.create_text(30, 30, text=time_limet)
    bricks_breaked = 0
    breaks = canvas.create_text(390, 30, text= bricks_breaked)
    pause_btn.place(x = 3000, y = -2000)
    # making bricks as an objects.
    objDict = {}
    bigen = 1
    # hint: most of things about sizes and bricks are defined at the top of the program.
    y = first_line_hight
    size_without_spaces = ((canvas_width - (big_space * 2)) - (((bricks_in_line - 1) * between_bricks_spaces)))
    brick_size = (size_without_spaces / bricks_in_line)

    for i in range(1, ((lines_of_bricks * bricks_in_line) + 1)):
        objName = f"brick_{i}"
        objName_2 = f"brick_{(i - 1)}"  # for the last object's name that was made.
        # for x of the bricks:
        if i == 1:
            x = big_space
            colors_chooser(colors)
        else:
            last_x = objDict[objName_2].pos[2]  # this is for the position of the last brick that was made at the last time.
            x = last_x + between_bricks_spaces
        # this is for y and x of the first brick:
        if i == bigen + bricks_in_line:
            y = ((y + between_lines_spaces) + 13)
            bigen = bigen + bricks_in_line
            x = big_space
            # color chooser:
            try:
                colors_chooser(colors)
            except:
                colors = ['orange', 'green', 'gray', 'cyan', 'gold', 'silver', 'purple', 'pink']
                colors_chooser(colors)

        objDict[objName] = Bricks(canvas, ball, brick_size, colors_chooser.brick_color, x, y)

    # The game's starter
    run = False

    def start_run():
        nonlocal run
        run = True

    start_btn = Button(tk, text='Start', width=20, height=1, bd='10', command = start_run)
    start_btn.place(x=(canvas_height/4), y=(canvas_height/2))

    while True:
        try:
            tk.update()
        except:
            break
        if run == True:
            start_btn.place(x=-3000, y=-3000)
            break
        time.sleep(0.01)

    # game's start counter:
    if run == True:
        times = 4
        for i in range(1 ,4):
            print_for_second(times - i)
        print_for_second('GO')
    try:
        pause_btn.place(x=8, y=(canvas_height-50))
        t = (time_limet-1) # t is the seconds amount till the game finish and its = for the time limet thats at the settings of the game at the top of the program
        count = 0 # a counter variable
        second_to_count = 79 # this is for how many loops of the while needed to make a second.
        bricks = (lines_of_bricks * bricks_in_line) #this is for the number of bricks on the screen each second.
        #this set the paddle movment to 0 after restarting the game to not let the paddle move if the controls have been pressed before the game starts:
        paddle.x = 0
    except:
        run = False
    # this is the game loop.
    while run == True:
        try :
            if ball.hit_bottom == False:
                if ball.hit_wall == True:
                    try:
                        hit_sound.play()
                    except:
                        pass
                    ball.hit_wall = False
                # hint: check is a function in the both classes.
                ball.check() #in the ball it check if it toutched the walls or the paddle and if that it will bounce
                paddle.check() #and in the paddle it checks if left or right buttons and if left been pressed the paddle will go left and if right been pressed the paddle will move right.
                # plays a sound when it toutch something axcept the brick:
                if paddle.ball_hit == True:
                    try:
                        paddle_hit_sound.play()
                        paddle.ball_hit = False
                    except:
                        pass

                # timer for the game:
                # this calculates(there after a line) are about to make the value of the time left, and seconds to count is for how many while loops to get the time 1 second.
                if count == ((time_limet - t)*second_to_count) or count == 1:
                    if count == 1:
                        canvas.delete(t0)
                    if count >= second_to_count:
                        canvas.delete(text) # deletes the last number to not over write on the last one later
                    text = canvas.create_text(30, 30, text=t) # prints what time left till the game finish.
                    t = t-1 # make the seconds left lesser because 1 seconed passed.

                # brick checks:
                for brick in dict(objDict).keys(): #look for all the bricks(objects) in a dictionary I have made when I made the objects for the Brick class.
                    objDict[brick].check() #this function check if the ball toutched it and if that it will be breaked and the ball will bounce.
                    if objDict[brick].hit_brick() == True: # (hit_brick()) is a function in the Bricks class that change to True if the ball toutched the brick.
                        try:
                            brick_hit_sound.play() # plays the hit sound when the ball hit the brick
                        except:
                            pass
                        canvas.delete (objDict[brick].id) # this removes(delete) the paddle from the window.
                        objDict.pop(brick) # this removes the object from the dictionary to not let the ball bounce ever again if it toutched the place of the brick.
                        bricks = bricks-1 # increase the number of the bricks because this brick doesn't contain anymore
                        bricks_breaked = (bricks_breaked + 1)
                        canvas.delete(breaks)
                        breaks = canvas.create_text(390, 30, text=bricks_breaked)

                if bricks <= 0: # if all of the bricks are removed from the dictionary (all been hited).
                    # this two 'update' updates the screen after printing ('YOU WON') to let the player see it.
                    restart__print('YOU WON', text, ball, paddle, breaks)
                    if len(objDict) != 0:
                        for brick in dict(objDict).keys():
                            canvas.delete(objDict[brick].id)
                            objDict.pop(brick)
                    start()

                # the game's time is over end:
                if t <= -1:
                    restart__print('GAME OVER', text, ball, paddle, breaks)
                    for brick in dict(
                            objDict).keys():  # look for all the bricks(objects) in the dictionary I have made when I made the objects for the Brick class.
                        canvas.delete(objDict[brick].id)
                        objDict.pop(brick)
                    start()

                # canvas updeter:
                tk.update_idletasks()
                tk.update()
                time.sleep(0.01)
                # this adds 1 to the counter because 1 loop of the while loop finished:
                count = count+1

            # the game's hit bottom end:
            else:
                restart__print('YOU LOST', text, ball, paddle, breaks)
                for brick in dict(objDict).keys():  # look for all the bricks(objects) in the dictionary I have made when I made the objects for the Brick class.
                    canvas.delete(objDict[brick].id)
                    objDict.pop(brick)
                start()
        except:
            break
start()
