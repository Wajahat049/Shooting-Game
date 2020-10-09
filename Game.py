import pygame
import random
import math
from pygame import mixer

pygame.init()

# For window
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("JetShooting")

# For images
img2 = pygame.image.load("images/ufo.png")
img1 = pygame.image.load("images/spaceship.png")
play_img = pygame.transform.scale(img1, (60, 60))
img3 = pygame.image.load("images/main5.jpg")
bg_img = pygame.transform.scale(img3, (600, 600))
img4 = pygame.image.load("images/ammo.png")
bullet_img = pygame.transform.scale(img4, (30, 30))
main_bg_img = pygame.transform.scale(img3, (600, 600))
score = 0
game = "no"
bomb_scoring = 1

def collide(x1, x2, y1, y2):
    distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    if distance < 30:
        return True
    else:
        return False


def collide_over(x1, x2, y1, y2):
    distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    if distance < 30:
        return True
    else:
        return False


def bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 10, y))


def game_over():
    over = pygame.font.SysFont("comicsans", 50)
    overr = over.render("GAME OVER", True, (255, 255, 255))
    screen.blit(overr, (150, 250))


# For bullets
bullet_x = 0
bullet_y = 500
bullet_x_change = 0
bullet_y_change = 40
bullet_state = "rest"

# For player
play_x = 300
play_y = 500
play_x_change = 0
play_y_change = 0

# For multiple enemies
enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
enemies = 4

for i in range(enemies):
    enemy_x.append(random.randint(0, 550))
    enemy_y.append(random.randint(50, 100))
    enemy_x_change.append(5)
    enemy_y_change.append(30)

    enemy_img.append(pygame.transform.scale(img2, (50, 50)))

# For starting window
while True:
    screen.blit(main_bg_img, (0, 0))
    pygame.draw.rect(screen, (0, 255, 0), (90, 340, 90, 45))
    pygame.draw.rect(screen, (255, 0, 0), (390, 340, 90, 45))
    font = pygame.font.Font("freesansbold.ttf", 30)
    start_game = font.render("Start", True, (255, 255, 255))
    screen.blit(start_game, (100, 350))
    exit_game = font.render("Exit", True, (255, 255, 255))
    screen.blit(exit_game, (400, 350))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break

        if event.type == pygame.MOUSEBUTTONDOWN:
            # If start button pressed
            if 180 > pygame.mouse.get_pos()[0] > 90 and 395 > pygame.mouse.get_pos()[1] > 340:

                # Main game loop
                while 1:
                    screen.blit(bg_img, (0, 0))
                    screen.blit(play_img, (play_x, play_y))

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                        if event.type == pygame.KEYDOWN:
                            if (event.key == pygame.K_LEFT):
                                play_x_change -= 5
                            if (event.key == pygame.K_RIGHT):
                                play_x_change += 5
                            if (event.key == pygame.K_UP):
                                play_y_change -= 5
                            if (event.key == pygame.K_DOWN):
                                play_y_change += 5
                            if event.key == pygame.K_SPACE:
                                if bullet_state == "rest":
                                    bullet_fire = mixer.Sound("Sound/bulletfire2.wav")
                                    bullet_fire.play()
                                    bullet_x = play_x
                                    bullet(bullet_x, bullet_y)

                        if event.type == pygame.KEYUP:

                            if (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_DOWN or event.key == pygame.K_UP or event.key == pygame.K_SPACE):
                                play_x_change = 0
                                play_y_change = 0

                    # Movement of player
                    play_x += play_x_change
                    play_y += play_y_change

                    if play_x <= 0:
                        play_x = 0
                    elif play_x >= 550:
                        play_x = 550

                    if play_y <= 0:
                        play_y = 0
                    elif play_y >= 550:
                        play_y = 550

                    for i in range(enemies):

                        # For collision of player and enemies
                        collision_over = collide_over(enemy_x[i], play_x, enemy_y[i], play_y)
                        if collision_over:
                            for j in range(enemies):
                                enemy_x[j] = 2000
                            game = "yes"
                            break

                        if enemy_x[i] <= 0:
                            enemy_x_change[i] = 1
                            enemy_y[i] += enemy_y_change[i]
                        elif enemy_x[i] >= 550:
                            enemy_y[i] += enemy_y_change[i]
                            enemy_x_change[i] = -1
                        enemy_x[i] += enemy_x_change[i]

                        # For collision of bullets and enemies
                        collision = collide(enemy_x[i], bullet_x, enemy_y[i], bullet_y)
                        if collision:
                            explode = mixer.Sound("Sound/explosion.wav")
                            explode.play()

                            bullet_y = play_y
                            bullet_state = "rest"
                            score += 1

                            enemy_x[i] = random.randint(0, 550)
                            enemy_y[i] = random.randint(50, 100)

                        screen.blit(enemy_img[i], (enemy_x[i], enemy_y[i]))

                    # For bullets
                    if bullet_y <= 0:
                        bullet_state = "rest"
                        bullet_y = play_y

                    if bullet_state == "fire":
                        bullet(bullet_x, bullet_y)
                        bullet_y -= bullet_y_change

                    # To display game over
                    font = pygame.font.Font("freesansbold.ttf", 20)
                    scoring = font.render("SCORE:" + " " + str(score), True, (255, 255, 255))
                    screen.blit(scoring, (10, 10))

                    if game == "yes":
                        game_over()

                    pygame.display.update()

            # If exit button pressed
            elif 480 > pygame.mouse.get_pos()[0] > 400 and 395 > pygame.mouse.get_pos()[1] > 340:
                pygame.quit()

    pygame.display.update()
