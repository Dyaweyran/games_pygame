import pygame as pg


def player_update():
    global player_x
    player_x += player_dx

    if player_x < 0:
        player_x = 0

    if player_x + player_width > display_width:
        player_x = display_width - player_width


def bullet_create():
    """Return coordinates for bullet"""
    x = player_x + player_width // 2 - bullet_width // 2
    y = player_y - bullet_height
    dy = -bullet_speed
    return x, y, dy


def bullet_update():
    global bullet_y, bullet_alive
    if bullet_alive:
        bullet_y += bullet_dy

    if bullet_y < -bullet_height:
        bullet_alive = False


def model_update():
    player_update()
    bullet_update()


def event_bullet(event):
    global bullet_alive, bullet_x, bullet_y, bullet_dy
    if event.type == pg.MOUSEBUTTONDOWN:
        key = pg.mouse.get_pressed()
        print(f'{key=} {bullet_alive=}')
        if key[0] and not bullet_alive:
            bullet_x, bullet_y, bullet_dy = bullet_create()
            bullet_alive = True


def display_redraw():
    display.fill('black', (0, 0, display_width, display_height))
    display.blit(player_img, (player_x, player_y))
    if bullet_alive:
        display.blit(bullet_img, (bullet_x, bullet_y))

    pg.display.update()


def event_player(event):
    """Player's movements from the keyboard"""
    global player_dx
    if event.type == pg.KEYDOWN:
        if event.key == pg.K_LEFT or event.key == pg.K_a:
            player_dx = -player_speed
        if event.key == pg.K_RIGHT or event.key == pg.K_d:
            player_dx = player_speed

    if event.type == pg.KEYUP:
        if event.key in (pg.K_LEFT, pg.K_RIGHT, pg.K_a, pg.K_d):
            player_dx = 0


def event_close_application(event):
    return event.type == pg.QUIT


def event_process():
    """Processing keyboard commands"""
    for event in pg.event.get():
        event_player(event)
        event_bullet(event)
        if event_close_application(event):
            return False
    return True


pg.init()

icon_img = pg.image.load('resources/img/ufo.png')


display_width = 800
display_height = 600
display_size = (display_width, display_height)


display = pg.display.set_mode(display_size)
pg.display.set_caption('Space Invaders')
pg.display.set_icon(icon_img)

player_img = pg.image.load('resources/img/player.png')
player_width = player_img.get_width()
player_height = player_img.get_height()

player_gap = 10
player_x = display_width // 2 - player_width // 2
player_y = display_height - player_height - player_gap

player_speed = 1
player_dx = 0


bullet_img = pg.image.load('resources/img/bullet.png')
bullet_alive = False
bullet_width = bullet_img.get_width()
bullet_height = bullet_img.get_height()
bullet_x, bullet_y, bullet_dy = 0, 0, 0
bullet_speed = 1


running = True
while running:
    model_update()
    display_redraw()
    running = event_process()
