import sys, pygame
from random import randint
from player_ai import Agent
from game_config import *

class Birdy:
    def __init__(self, pos=None, size=None):

        if size is None:
            self.size = (BIRD_SIZE,BIRD_SIZE)
        else:
            self.size = size

        if pos is None:
            self.pos = [SCREEN_WIDTH // 2 - self.size[0] // 2, SCREEN_HEIGHT // 2 - self.size[1] // 2] #center of bird into center of screen
        else:
            self.pos = pos

        self.in_jump = False
        self.jump_counter = 0

    def update_pos(self, jump=False):
        if self.in_jump == False and jump == True:
            self.in_jump=True
            self.jump_counter=5

        if self.in_jump == False:
            self.pos[1]+=JUMP_SPEED #move bird down
        elif self.in_jump == True:
            self.pos[1]-=FALL_SPEED
            self.jump_counter-=1
            if self.jump_counter <= 0:
                self.in_jump = False

        if self.pos[1] <= 0:
            self.pos[1] = 0
        if self.pos[1] >= SCREEN_HEIGHT:
            self.pos[1] = SCREEN_HEIGHT-1

        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def get_rect(self):
        return self.rect

class Pipe:
    def __init__(self, pos_x=SCREEN_WIDTH-1, pos_y=0, width=PIPE_WIDTH, gap_y=SCREEN_HEIGHT//2):
        self.pos = [pos_x, pos_y] # top left corner of top pipe
        self.width = width
        self.gap_y = gap_y #center of gap in pipe


    def update_pos(self):
        self.pos[0]-=PIPE_SPEED
        self.rect_top = pygame.Rect(self.pos[0], self.pos[1], self.width, self.gap_y - PIPE_GAP_HEIGHT / 2)
        self.rect_bottom = pygame.Rect(self.pos[0], self.gap_y + PIPE_GAP_HEIGHT / 2, self.width,
                                  SCREEN_HEIGHT - (self.gap_y + PIPE_GAP_HEIGHT / 2))

    def get_rects(self):
        return self.rect_top, self.rect_bottom


def run_game(agent=None, framerate=30):
    score = 0
    pygame.init()
    size = width, height = 600, 600
    black = 0, 0, 0
    green = 0,0,255
    white = 255,255,255

    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    bird = Birdy()
    pipes = []
    pipes.append(Pipe(gap_y=randint(GAP_BOUNDARY, SCREEN_HEIGHT - GAP_BOUNDARY)))

    first_frame = True
    while 1:
        jump = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT: return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or pygame.K_w:
                    jump=True


        #Get closest gap location
        closest = pipes[0]
        for pipe in pipes:
            if pipe.pos[0]+PIPE_WIDTH/2 >= SCREEN_WIDTH/2 and pipe.pos[0]+PIPE_WIDTH/2< closest.pos[0]+PIPE_WIDTH/2:
                closest = pipe
        #call player ai
        if agent is not None:
            y_dif = bird.pos[1]-closest.gap_y
            x_dif = (closest.pos[0] + PIPE_WIDTH//2) - (bird.pos[0] + bird.size[0]//2)
            state = (x_dif, y_dif)
            jump = ACTION_DICT[agent.take_action(state)]
            print(f"State: {state} Action: {jump}")

            #update q table if not first frame
            #have to do it here to have the new game state
            if first_frame:
                first_frame = False

            else:
                # Update Q Table
                agent.update_q_table(state)


        #update pipes
        if pipes[0].pos[0] + PIPE_WIDTH < 0:
            del pipes[0]

        if pipes[-1].pos[0] + PIPE_WIDTH < SCREEN_WIDTH - (SCREEN_WIDTH / 4):
            pipes.append(Pipe(gap_y=randint(SCREEN_HEIGHT/3, SCREEN_HEIGHT - SCREEN_HEIGHT/3)))

        #clear screen
        screen.fill(black)

        #draw pipes
        for pipe in pipes:
            pipe.update_pos()
            rects = pipe.get_rects()
            pygame.draw.rect(screen, green, rects[0])
            pygame.draw.rect(screen, green, rects[1])

        bird.update_pos(jump=jump)


        #calculate reward
        if bird.pos[0] + bird.size[0]//2 >= closest.pos[0] + PIPE_WIDTH // 2: #passed pipe
            reward = 100
            score+=1
        else:
            reward = 0

        print(f"Reward:{reward}")
        print(f"Score: {score}")


        pygame.draw.rect(screen, white, bird.get_rect())
        pygame.display.flip()

        #screen_arr = pygame.surfarray.pixels2d(screen)


        #Check for collisions
        pipe_rects = []
        quit = False
        for pipe in pipes:
            pipe_rects = pipe_rects + list(pipe.get_rects())

        if bird.get_rect().collidelist(pipe_rects) != -1:
            print("Hit pipe you Lose")
            reward = -1000
            quit = True

        if bird.pos[1] + bird.size[1] >= SCREEN_HEIGHT-BIRD_SIZE:
            print("Hit bottom you lose")
            reward = -1000
            quit = True

        #Give reward
        if agent is not None:
            agent.set_reward(reward)

        if framerate != -1:
            clock.tick(framerate)

        if quit:
            pygame.display.quit()
            pygame.quit()
            return
