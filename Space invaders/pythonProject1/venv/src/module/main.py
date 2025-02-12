import pygame
from random import randrange

pygame.init()

display_width = 800
display_height = 600
display_size = (display_width, display_height)
display = pygame.display.set_mode(display_size)

running = True
kill_count = 0
display_mode = ['Start', 'Game', 'End']
background_sound = pygame.mixer.Sound('resources/audio/background.wav')
background_sound.set_volume(0.3)

player_img = pygame.image.load('resources/img/player.png')
player_width = player_img.get_width()
player_height = player_img.get_height()
player_gap = 5
player_x = display_width // 2 - player_width // 2
player_y = display_height - player_height - player_gap
player_speed = 1
player_dx = player_speed
sound_death = pygame.mixer.Sound('resources/audio/explosion.wav')
sound_death.set_volume(0.7)

enemy_img = pygame.image.load('resources/img/enemy.png')
enemy_width = enemy_img.get_width()
enemy_height = enemy_img.get_height()
enemy_x, enemy_y, enemy_dx, enemy_dy = 0, 0, 0, 0
enemy_alive = False

bullet_img = pygame.image.load('resources/img/bullet.png')
bullet_width = bullet_img.get_width()
bullet_height = bullet_img.get_height()
bullet_x, bullet_y, bullet_dy = 0, 0, 0
bullet_alive = False
bullet_speed = 3
sound_bullet = pygame.mixer.Sound('resources/audio/laser.wav')
sound_bullet.set_volume(0.5)


def player_update():
    global player_x
    player_x += player_dx
    if player_x < 0:
        player_x = 0
    elif player_x > display_width - player_width:
        player_x = display_width - player_width


def bullet_create():
    x = player_x + player_width / 2 - bullet_width / 2
    y = player_y - bullet_height
    dy = -bullet_speed
    sound_bullet.play()
    return x, y, dy


def bullet_update():
    global bullet_y, bullet_alive
    if bullet_alive:
        bullet_y += bullet_dy
    if bullet_y < 0:
        bullet_alive = False


def enemy_create():
    x = randrange(0, display_width - enemy_width)
    y = 0

    dx = randrange(-1, 2) / 2
    dy = randrange(1, 2) / 3

    return x, y, dx, dy


def enemy_update():
    global enemy_x, enemy_y, enemy_alive
    enemy_x += enemy_dx
    enemy_y += enemy_dy

    if enemy_x < 0 \
            or enemy_x + enemy_width > display_width \
            or enemy_y + enemy_height > display_height:
        enemy_alive = False


def enemy_init():
    global enemy_alive, enemy_x, enemy_y, enemy_dx, enemy_dy
    if not enemy_alive:
        enemy_x, enemy_y, enemy_dx, enemy_dy = enemy_create()
        enemy_alive = True


def event_check_collision():
    global bullet_alive, enemy_alive, kill_count
    bullet_rect = pygame.Rect(bullet_x, bullet_y, bullet_width, bullet_height)
    enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height)
    if bullet_rect.colliderect(enemy_rect):
        bullet_alive = False
        enemy_alive = False
        kill_count += 1


def event_check_game_over():
    global enemy_alive
    enemy_rect = pygame.rect.Rect(enemy_x, enemy_y, enemy_width, enemy_height)
    player_rect = pygame.rect.Rect(player_x, player_y, player_width, player_height)
    if enemy_rect.colliderect(player_rect):
        enemy_alive = False
        return True
    return False


def model_update():
    player_update()
    bullet_update()
    enemy_update()
    event_check_collision()
    if not enemy_alive:
        enemy_init()


def event_player(event):
    """Вправо-влево по нажатию стрелок и a, d;"""
    global player_dx
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
            player_dx = -player_speed
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            player_dx = player_speed
    elif event.type == pygame.KEYUP:
        player_dx = 0


def event_close_application(event):
    return event.type == pygame.QUIT


def event_start_application(event):
    return event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN


def event_restart_application(event):
    return event.type == pygame.KEYDOWN and event.key == pygame.K_r


def event_bullet(event):
    global bullet_alive, bullet_x, bullet_y, bullet_dy
    if event.type == pygame.MOUSEBUTTONDOWN:
        key = pygame.mouse.get_pressed()
        if key[0] and not bullet_alive:
            bullet_x, bullet_y, bullet_dy = bullet_create()
            bullet_alive = True


def event_process():
    for event in pygame.event.get():
        event_player(event)
        event_bullet(event)
        if event_close_application(event):
            return False
    return True


def display_redraw(d_mode):
    if d_mode == display_mode[1]:
        display.fill('black', (0, 0, display_width, display_height))
        display.blit(player_img, (player_x, player_y))
        kill_font = pygame.font.Font('resources/04B_19__.TTF', 24)
        kill_surface = kill_font.render(f'Score: {kill_count}', True, 'orange')
        display.blit(kill_surface, (0, 0))
        if enemy_alive:
            display.blit(enemy_img, (enemy_x, enemy_y))
        if bullet_alive:
            display.blit(bullet_img, (bullet_x, bullet_y))

        pygame.display.update()
    elif d_mode == display_mode[0]:
        font = pygame.font.Font('resources/04B_19__.TTF', 48)
        display.fill('black', (0, 0, display_width, display_height))
        start_surface = font.render('Press any button to start', True, 'white')
        display.blit(start_surface, (80, display_height // 2 - 40))

        pygame.display.update()
    elif d_mode == display_mode[2]:
        r_font = pygame.font.Font('resources/04B_19__.TTF', 64)
        display.fill('black', (0, 0, display_width, display_height))
        restart_surface = r_font.render('Press R to restart', True, 'red')
        display.blit(restart_surface, (80, display_height // 2 - 40))

        pygame.display.update()


start = False

while not start:
    display_redraw(display_mode[0])
    for event in pygame.event.get():
        if event_close_application(event):
            running = False
            start = True
        if event_start_application(event):
            start = True


background_sound.play(-1)

while running:
    background_sound.set_volume(0.3)
    model_update()
    display_redraw(display_mode[1])
    running = event_process()
    if event_check_game_over():
        background_sound.set_volume(0)
        sound_death.play()
        restart = False
        while not restart:
            display_redraw(display_mode[2])
            for event in pygame.event.get():
                if event_restart_application(event):
                    restart = True
                    kill_count = 0
                    model_update()
                    display_redraw(display_mode[1])
                    running = event_process()
                if event_close_application(event):
                    running = False
                    restart = True
