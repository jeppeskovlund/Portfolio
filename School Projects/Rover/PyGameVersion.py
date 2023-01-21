from time import sleep

import pygame as pg

pg.init()
joy_controller = [pg.joystick.Joystick(x)
                  for x in range(pg.joystick.get_count())]
joy_controller[0].init()
pg.font.get_default_font()
screen_width = 1280
screen_height = 600
screen = pg.display.set_mode((screen_width, screen_height), pg.SCALED)
pg.display.set_caption("RACERBIL")
pg.mouse.set_visible(False)
clock = pg.time.Clock()

background = pg.Surface(screen.get_size())
background = background.convert()
background.fill((68, 101, 11))

font = pg.font.Font(pg.font.get_default_font(), 20)

x = 600
y = 300
# vel = 5

analog_keys = {0: 0, 1: 0}


def batteri_text():
    text = font.render(f"{round(x/screen_width*100)} %", True, "blue")
    text_rect = text.get_rect()
    text_rect.center = (60, 25)
    screen.blit(text, text_rect)


def batteri_life():
    batteri_width = round(x/screen_width*100)
    if batteri_width > 70:
        color = "green"
    elif batteri_width < 25:
        color = "red"
    else:
        color = "yellow"
    pg.draw.rect(screen, color, (10, 10, batteri_width, 30))


gameloop = True
while gameloop:
    clock.tick(60)
    for event in pg.event.get():
        if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            gameloop = False
        if event.type == pg.JOYAXISMOTION:
            print(x/screen_width*100)
            analog_keys[event.axis] = event.value
            x += analog_keys[0]
            y += analog_keys[1]

    screen.blit(background, (0, 0))
    pg.draw.rect(screen, "black", (8, 8, 104, 34))
    batteri_life()
    batteri_text()
    pg.draw.rect(screen, (0, 0, 0), (x, y, 30, 30))
    pg.display.flip()
pg.quit()
