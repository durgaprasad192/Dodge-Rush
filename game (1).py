import pygame
import sys
import glob

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Start background music (loops forever)
pygame.mixer.music.load("music1.mp3")
pygame.mixer.music.play(-1)

# Set up display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Battle")

# Load images
background = pygame.image.load("bg.png")
background = pygame.transform.scale(background, (800, 600))

gameover_img = pygame.image.load("gameover.png")
gameover_img = pygame.transform.scale(gameover_img, (800, 600))

# Load hero frame (just one image)
frame_img = pygame.image.load("hero.png").convert_alpha()
frame_img = pygame.transform.scale(frame_img, (80, 120))
frames = [frame_img]  # Single frame
frame_count = len(frames)
frame_index = 0

# Bullet
bullet_img = pygame.image.load("bullet.png")
bullet_img = pygame.transform.scale(bullet_img, (60, 20))

# Enemies
enemy1_img = pygame.image.load("enemy1.png")
enemy1_img = pygame.transform.scale(enemy1_img, (200, 140))

enemy2_img = pygame.image.load("enemy2.png")
enemy2_img = pygame.transform.scale(enemy2_img, (200, 140))

clock = pygame.time.Clock()

# Start screen
def show_start_screen():
    font = pygame.font.SysFont(None, 72)
    text = font.render("Press SPACE to Start", True, (255, 255, 255))
    text_rect = text.get_rect(center=(400, 300))
    while True:
        screen.fill((0, 0, 0))
        screen.blit(text, text_rect)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

show_start_screen()

# Hero setup
x = 100
base_y = 400 - 72
y = base_y
jumping = False
jump_velocity = 0
character_width = 50
character_height = 110
hero_health = 10
last_hit_time = 0
hit_cooldown = 1000  # ms

# Enemy setup
enemy_stage = 1
enemy_img = enemy1_img
enemy_x = 650
enemy_y = base_y
enemy_speed = 1.5
enemy_health = 2
enemy_visible = True
enemy_respawn_time = 0

# Bullets
bullets = []

# Game state
game_over = False
music2_played = False

# Main game loop
while True:
    if game_over:
        screen.blit(gameover_img, (0, 0))

        if not music2_played:
            pygame.mixer.music.stop()
            pygame.mixer.music.load("music2.mp3")
            pygame.mixer.music.play()
            music2_played = True

        pygame.display.flip()
        continue

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_SPACE) and not jumping:
                jumping = True
                jump_velocity = -18

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                bullet_x = x + character_width
                bullet_y = y + character_height // 2
                bullets.append([bullet_x, bullet_y])

    # Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x -= 5
    if keys[pygame.K_RIGHT]:
        x += 5

    x = max(0, min(x, 800 - character_width))
    y = max(0, min(y, base_y))

    if jumping:
        y += jump_velocity
        jump_velocity += 1
        if y >= base_y:
            y = base_y
            jumping = False

    screen.blit(background, (0, 0))

    # Enemy respawn logic
    if not enemy_visible and enemy_stage == 1 and enemy_respawn_time == 0:
        enemy_respawn_time = pygame.time.get_ticks()
    elif enemy_stage == 1 and enemy_respawn_time > 0:
        if pygame.time.get_ticks() - enemy_respawn_time > 1000:
            enemy_stage = 2
            enemy_img = enemy2_img
            enemy_health = 2
            enemy_x = 650
            enemy_y = base_y + 22
            enemy_visible = True
            enemy_respawn_time = 0

    # Enemy logic
    if enemy_visible:
        if enemy_x > x:
            enemy_x -= enemy_speed

        enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_img.get_width(), enemy_img.get_height())
        hero_rect = pygame.Rect(x, y, frames[0].get_width(), frames[0].get_height())

        current_time = pygame.time.get_ticks()
        if enemy_rect.colliderect(hero_rect):
            if current_time - last_hit_time > hit_cooldown:
                hero_health -= 1
                last_hit_time = current_time
                if hero_health <= 0:
                    game_over = True

        # Draw enemy
        screen.blit(enemy_img, (enemy_x, enemy_y))

        # Draw enemy health bar
        bar_width = 100
        bar_height = 10
        bar_x = enemy_x + (enemy_img.get_width() - bar_width) // 2
        bar_y = enemy_y - 20

        pygame.draw.rect(screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))
        health_ratio = enemy_health / 2
        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, int(bar_width * health_ratio), bar_height))

    # Draw hero
    frame = frames[frame_index]
    screen.blit(frame, (x, y))
    frame_index = (frame_index + 1) % frame_count

    # Hero health bar
    hero_bar_width = 100
    hero_bar_height = 10
    hero_bar_x = x + (character_width // 2) - (hero_bar_width // 2)
    hero_bar_y = y - 15

    pygame.draw.rect(screen, (100, 100, 100), (hero_bar_x, hero_bar_y, hero_bar_width, hero_bar_height))
    hero_health_ratio = hero_health / 10
    pygame.draw.rect(screen, (0, 255, 0), (hero_bar_x, hero_bar_y, int(hero_bar_width * hero_health_ratio), hero_bar_height))

    # Bullets
    for bullet in bullets[:]:
        bullet[0] += 15
        screen.blit(bullet_img, (bullet[0], bullet[1]))

        if enemy_visible:
            bullet_rect = pygame.Rect(bullet[0], bullet[1], bullet_img.get_width(), bullet_img.get_height())
            if bullet_rect.colliderect(enemy_rect):
                bullets.remove(bullet)
                enemy_health -= 1
                if enemy_health <= 0:
                    enemy_visible = False
                continue

        if bullet[0] > 800:
            bullets.remove(bullet)

    pygame.display.flip()
    clock.tick(30) 
