import pygame
from random import randint
from pygame.math import Vector2

pygame.init()

pygame.mixer.pre_init(44100, -16, 2, 512)
green = (255, 242, 0)
g = (138, 177, 20)
lg = (166, 213, 23)
r = (157, 13, 20)
lr = (237, 28, 36)
b = (51, 181, 213)
lb = (86, 193, 220)
black = (0, 0, 0)
lback_color = (255, 242, 0)
back_color = (255, 201, 14)
snake_color = (255, 128, 0)
bg = (175, 215, 70)
cell_size = 40
cell_number = 15
img = pygame.image.load("cave1.jpg")
cave = pygame.Rect(0, 35, 50, 40)
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()
apple = pygame.image.load('apple.png').convert_alpha()
frog = pygame.image.load('frog.jpg').convert_alpha()
mouse = pygame.image.load('mouse.png').convert_alpha()
rules_img = pygame.image.load('RULES.png').convert_alpha()
pause_img = pygame.image.load('PAUSE.png').convert_alpha()
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)
font = pygame.font.SysFont(None, 45)
font1 = pygame.font.SysFont(None, 60)
font2 = pygame.font.SysFont(None, 25)


class SNAKE:
    def __init__(self):
        self.body = [Vector2(0, 2), Vector2(1, 2), Vector2(2, 2)]
        self.direction = Vector2(0, 0)
        self.new_block = False

        self.head_up = pygame.image.load('head_up.png').convert_alpha()
        self.head_down = pygame.image.load('head_down.png').convert_alpha()
        self.head_right = pygame.image.load('head_right.png').convert_alpha()
        self.head_left = pygame.image.load('head_left.png').convert_alpha()

        self.tail_up = pygame.image.load('tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('body_bl.png').convert_alpha()

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0):
            self.head = self.head_left
        elif head_relation == Vector2(-1, 0):
            self.head = self.head_right
        elif head_relation == Vector2(0, 1):
            self.head = self.head_up
        elif head_relation == Vector2(0, -1):
            self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1):
            self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1):
            self.tail = self.tail_down

    def move_snake(self):
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True


class FOOD:
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(apple, fruit_rect)

    def draw_frog(self):
        frog_rect = pygame.Rect(int(self.frx * cell_size), int(self.fry * cell_size), cell_size, cell_size)
        screen.blit(frog, frog_rect)

    def draw_mouse(self):
        mouse_rect = pygame.Rect(int(self.mx * cell_size), int(self.my * cell_size), cell_size, cell_size)
        screen.blit(mouse, mouse_rect)

    def randomize(self):
        self.x = randint(1, 12)
        self.y = randint(1, 12)
        self.mx = randint(1, 12)
        self.my = randint(1, 12)
        self.frx = randint(1, 12)
        self.fry = randint(1, 12)
        self.pos = Vector2(self.x, self.y)
        self.mpos = Vector2(self.mx, self.my)
        self.frpos = Vector2(self.frx, self.fry)


class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.food = FOOD()
        self.score = 0

    def update(self):
        self.snake.move_snake()
        self.check_collision()

    def draw_elements(self):
        if self.score % 50 == 0 and self.score >= 50:
            self.food.draw_fruit()
        if self.score % 100 == 0 and self.score >= 100:
            self.food.draw_frog()
        if self.score % 10 == 0 and self.score >= 0:
            self.food.draw_mouse()
        self.snake.draw_snake()
        if self.score == 0:
            screen.blit(img, cave)
        self.draw_score()

    def check_collision(self):
        if self.food.mpos == self.snake.body[0]:
            self.score += 10
            self.food.randomize()
            self.snake.add_block()
        if self.food.frpos == self.snake.body[0]:
            self.score += 50
            self.food.randomize()
            self.snake.add_block()
        if self.food.pos == self.snake.body[0]:
            self.score -= 10
            self.food.randomize()
            self.snake.add_block()

        for block in self.snake.body[1:]:
            if block == self.food.pos:
                self.food.randomize()

    def draw_score(self):
        score_text = str(self.score)
        score_x = 70
        score_y = 20
        score_surface = font2.render("SCORE : " + score_text, True, (56, 74, 12))
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        screen.blit(score_surface, score_rect)

def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    screen.blit(screen_text, [x, y])


def text_screen1(text, color, x, y):
    screen_text = font1.render(text, True, color)
    screen.blit(screen_text, [x, y])


def text_screen2(text, color, x, y):
    screen_text = font2.render(text, True, color)
    screen.blit(screen_text, [x, y])

def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        screen.blit(pause_img, (0, 0))
        m_movement = pygame.mouse.get_pos()
        m_click = pygame.mouse.get_pressed()
        if 200 < m_movement[0] < 400 and 147 < m_movement[1] < 207:
            pygame.draw.rect(screen, lg, (200, 147, 200, 50))
            if m_click == (True, False, False):
                paused = False
        else:
            pygame.draw.rect(screen, g, (200, 147, 200, 50))
        if 225 < m_movement[0] < 375 and 270 < m_movement[1] < 320:
            pygame.draw.rect(screen, lb, (225, 270, 150, 50))
            if m_click == (True, False, False):
                gameloop()
        else:
            pygame.draw.rect(screen, b, (225, 270, 150, 50))
        if 200 < m_movement[0] < 400 and 410 < m_movement[1] < 460:
            pygame.draw.rect(screen, lr, (200, 410, 200, 50))
            if m_click == (True, False, False):
                welcome()
        else:
            pygame.draw.rect(screen, r, (200, 410, 200, 50))
        text_screen("Continue", black, 230, 157)
        text_screen("Restart", black, 245, 280)
        text_screen("Main Menu", black, 215, 420)
        pygame.display.update()
        clock.tick(60)

def rules():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        screen.blit(rules_img, (0, 0))
        movement = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if 20 < movement[0] < 170 and 20 < movement[1] < 70:
            pygame.draw.rect(screen, lback_color, (20, 20, 150, 50))
            if click == (True, False, False):
                welcome()
        else:
            pygame.draw.rect(screen, back_color, (20, 17, 150, 50))
        text_screen("BACK", g, 53, 32)
        pygame.display.update()
        clock.tick(60)

def welcome():
    exit_game = False
    bgimg = pygame.image.load("snake.png")
    bgimg = pygame.transform.scale(bgimg, (600, 600)).convert_alpha()
    while True:
        screen.fill((255, 255, 255))
        screen.blit(bgimg, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        mouse_movement = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        if 20 < mouse_movement[0] < 170 and 450 < mouse_movement[1] < 500:
            pygame.draw.rect(screen, lg, (20, 450, 150, 50))
            if mouse_click == (True, False, False):
                gameloop()
        else:
            pygame.draw.rect(screen, g, (20, 450, 150, 50))
        if 220 < mouse_movement[0] < 370 and 450 < mouse_movement[1] < 500:
            pygame.draw.rect(screen, lb, (220, 450, 150, 50))
            if mouse_click == (True, False, False):
                rules()
        else:
            pygame.draw.rect(screen, b, (220, 450, 150, 50))
        if 420 < mouse_movement[0] < 570 and 450 < mouse_movement[1] < 500:
            pygame.draw.rect(screen, lr, (420, 450, 150, 50))
            if mouse_click == (True, False, False):
                pygame.quit()
        else:
            pygame.draw.rect(screen, r, (420, 450, 150, 50))
        text_screen("Play", black, 65, 460)
        text_screen("Rules", black, 255, 460)
        text_screen("Quit", black, 465, 460)
        pygame.display.update()
        clock.tick(60)


def gameloop():
    gameover = False
    main_game = MAIN()
    while True:
        if gameover:
            screen.fill(green)
            text_screen("Game Over! Press Enter To Continue", snake_color, 20, 220)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == SCREEN_UPDATE:
                    main_game.update()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if main_game.snake.direction.y != 1:
                            main_game.snake.direction = Vector2(0, -1)
                    if event.key == pygame.K_RIGHT:
                        if main_game.snake.direction.x != -1:
                            main_game.snake.direction = Vector2(1, 0)
                    if event.key == pygame.K_DOWN:
                        if main_game.snake.direction.y != -1:
                            main_game.snake.direction = Vector2(0, 1)
                    if event.key == pygame.K_LEFT:
                        if main_game.snake.direction.x != 1:
                            main_game.snake.direction = Vector2(-1, 0)
                    if event.key == pygame.K_SPACE:
                        pause()
            screen.fill(bg)
            main_game.draw_elements()
            if 0 > main_game.snake.body[0].x or 0 > main_game.snake.body[0].y:
                gameover = True
            if main_game.snake.body[0].x >= cell_number or main_game.snake.body[0].y >= cell_number:
                gameover = True
            if main_game.score > 0:
                for block in main_game.snake.body[1:]:
                    if block == main_game.snake.body[0]:
                        gameover = True
            pygame.display.update()
            clock.tick(60)


welcome()
