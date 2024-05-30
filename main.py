import pygame
import os
import random

pygame.init()

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

RUNNING = [pygame.image.load(os.path.join('Assets/Dino', 'DinoRun1.png')),
           pygame.image.load(os.path.join('Assets/Dino', 'DinoRun2.png'))
]
JUMPING = pygame.image.load(os.path.join('Assets/Dino', 'DinoJump.png'))
DUCKING = [pygame.image.load(os.path.join('Assets/Dino', 'DinoDuck1.png')),
           pygame.image.load(os.path.join('Assets/Dino', 'DinoDuck2.png'))]

SMALL_CACTUS = [
    pygame.image.load(os.path.join('Assets/Cactus', 'SmallCactus1.png')),
    pygame.image.load(os.path.join('Assets/Cactus', 'SmallCactus2.png')),
    pygame.image.load(os.path.join('Assets/Cactus', 'SmallCactus3.png'))
]

LARGE_CACTUS = [
    pygame.image.load(os.path.join('Assets/Cactus', 'LargeCactus1.png')),
    pygame.image.load(os.path.join('Assets/Cactus', 'LargeCactus2.png')),
    pygame.image.load(os.path.join('Assets/Cactus', 'LargeCactus3.png')),
]

BIRD = [
    pygame.image.load(os.path.join('Assets/Bird', 'Bird1.png')),
    pygame.image.load(os.path.join('Assets/Bird', 'Bird2.png')),
]

CLOUD = pygame.image.load(os.path.join('Assets/Other', 'Cloud.png'))

BG = pygame.image.load(os.path.join('Assets/Other', 'Track.png'))


class Dinosaur():
    x_pos = 80
    y_pos = 310
    y_pos_duck = 340
    jump_vel = 8.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_jump = False
        self.dino_run = True

        self.jumpvel = self.jump_vel
        self.step_index = 0
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.x_pos
        self.dino_rect.y = self.y_pos

    def update(self, user_input):

        if self.dino_duck:
            self.duck()
        if self.dino_jump:
            self.jump()
        if self.dino_run:
            self.run()
        if self.step_index >= 10:
            self.step_index = 0

        if user_input[pygame.K_UP] and not self.dino_jump:
            self.dino_jump = True
            self.dino_duck = False
            self.dino_run = False
        elif user_input[pygame.K_DOWN] and not self.dino_jump:
            self.dino_jump = False
            self.dino_duck = True
            self.dino_run = False
        elif not (self.dino_jump or user_input[pygame.K_DOWN]):
            self.dino_jump = False
            self.dino_duck = False
            self.dino_run = True


    
    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.x_pos
        self.dino_rect.y = self.y_pos
        self.step_index += 1
    
    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.x_pos
        self.dino_rect.y = self.y_pos_duck
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jumpvel * 4
            self.jumpvel -= 0.8
        if self.jumpvel < - self.jump_vel:
            self.dino_jump = False
            self.jumpvel = self.jump_vel

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(10, 100)
        self.image = CLOUD
        self.width = self.image.get_width()
    
    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(10, 100)
        
    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))


class Obstacles:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()
    
    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)

class SmallCactus(Obstacles):
    def __init__(self, image):
        super().__init__(image, random.randint(0, 2))
        self.rect.y = 325

class LargeCactus(Obstacles):
    def __init__(self, image):
        super().__init__(image, random.randint(0, 2))
        self.rect.y = 300

class Bird(Obstacles):
    def __init__(self, image):
        super().__init__(image, 0)
        self.rect.y = 250
        self.index = 0
    
    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        self.index += 1


def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    points = 0
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()
    font = pygame.font.Font('freesansbold.ttf', 20)
    death_count = 0


    game_speed = 14
    x_pos_bg, y_pos_bg = 0, 380
    obstacles = []


    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1
        text = font.render("Points: " + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        SCREEN.blit(text, textRect)

    def back_ground():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (x_pos_bg + image_width, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (x_pos_bg + image_width, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed


    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                continue


        SCREEN.fill((255, 255, 255))
        user_input = pygame.key.get_pressed()

        player.draw(SCREEN)
        player.update(user_input)
        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0, 2) == 2:
                obstacles.append(Bird(BIRD))
        
        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(2000)
                death_count += 1
                menu(death_count)
                return
        back_ground()
        cloud.draw(SCREEN)
        cloud.update()
        score()
        clock.tick(30)
        pygame.display.update()

def menu(death_count):
    global points
    run = True
    while run:
        SCREEN.fill((255, 255, 255))
        font = pygame.font.Font('freesansbold.ttf', 30)
        if death_count == 0:
            text = font.render('Press any key to start', True, (0, 0, 0))
        elif death_count > 0:
            text = font.render('Press any key to restart', True, (0, 0, 0))
            score = font.render('Your Score: ' + str(points), True, (0, 0, 0))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score, scoreRect)
        
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.KEYDOWN:
                main()
        



menu(death_count=0)