import pygame
import time
import random
import database
from pygame_menu import themes
import settings_snake
from time import sleep
import pygame_menu

pygame.init()

white = settings_snake.white
yellow = settings_snake.yellow
black = settings_snake.black
red = settings_snake.red
green = settings_snake.green
blue = settings_snake.blue

dis_width = settings_snake.dis_width
dis_height = settings_snake.dis_height


dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption(settings_snake.caption)

clock = pygame.time.Clock()

snake_block = 10
snake_speed = 10

font_style = pygame.font.SysFont("ubuntu", 15)
score_font = pygame.font.SysFont("ubuntu", 25)


def winners():
    return database.read_database()


def Your_score(score):
    value = score_font.render("Ваши очки: " + str(score), True, black)
    dis.blit(value, [0, 0])


def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])


def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])


def gameLoop():
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_lst = []
    length_of_snake = 1

    o = 'start'

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0



    while not game_over:

        while game_close == True:

            pygame.init()
            surface = pygame.display.set_mode((600, 400))

            mainmenu = pygame_menu.Menu('Список лидеров', 600, 400, theme=themes.THEME_SOLARIZED)
            mainmenu.add.label('Имя1')
            mainmenu.add.label('счёт1')
            mainmenu.add.label('Имя2')
            mainmenu.add.label('счёт2')
            mainmenu.add.label('Имя3')
            mainmenu.add.label('счёт3')
            mainmenu.add.button('Выйти', pygame_menu.events.EXIT)

            arrow = pygame_menu.widgets.LeftArrowSelection(arrow_size=(10, 15))

            update_loading = pygame.USEREVENT + 0

            while True:
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT:
                        exit()

                if mainmenu.is_enabled():
                    mainmenu.update(events)
                    mainmenu.draw(surface)
                    if (mainmenu.get_current().get_selected_widget()):
                        arrow.draw(surface, mainmenu.get_current().get_selected_widget())

                pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                game_over = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if o == 'up' or o == 'down':
                        x1_change = -snake_block
                        y1_change = 0
                        o = 'left'
                    else:
                        pass
                elif event.key == pygame.K_RIGHT:
                    if o == 'up' or o == 'down':
                        x1_change = snake_block
                        y1_change = 0
                        o = 'right'
                    else:
                        pass
                elif event.key == pygame.K_UP:
                    if o == 'left' or o == 'right' or o == 'start':
                        y1_change = -snake_block
                        x1_change = 0
                        o = 'up'
                    else:
                        pass
                elif event.key == pygame.K_DOWN:
                    if o == 'left' or o == 'right':
                        y1_change = snake_block
                        x1_change = 0
                        o = 'down'
                    else:
                        pass

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)

        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_lst.append(snake_head)
        if len(snake_lst) > length_of_snake:
            del snake_lst[0]

        for x in snake_lst[:-1]:
            if x == snake_head:
                game_close = True

        our_snake(snake_block, snake_lst)
        Your_score(length_of_snake - 1)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            length_of_snake += 1
        clock.tick(snake_speed)

    pygame.quit()
    quit()



pygame.init()
surface = pygame.display.set_mode((600, 400))


def set_difficulty(value, difficulty):
    print(value)
    print(difficulty)


def start_the_game():
    mainmenu._open(loading)
    pygame.time.set_timer(update_loading, 30)


def level_menu():
    mainmenu._open(level)


def select_language(value, lang):
    print(value)
    print(lang)


def lang_menu():
    mainmenu._open(language)


mainmenu = pygame_menu.Menu('Snake', 600, 400, theme=themes.THEME_SOLARIZED)
mainmenu.add.text_input('Имя: ', default='')
mainmenu.add.button('Играть', start_the_game)
mainmenu.add.button('Сложность', level_menu)
mainmenu.add.button('Язык', lang_menu)
mainmenu.add.button('Выйти', pygame_menu.events.EXIT)

level = pygame_menu.Menu('Выберите сложность', 600, 400, theme=themes.THEME_BLUE)
level.add.selector('Сложность :', [('Тяжёлая', 1), ('Лёгкая', 2)], onchange=set_difficulty)

language = pygame_menu.Menu('Выберите Язык', 600, 400, theme=themes.THEME_BLUE)
language.add.selector('Язык :', [('English', 1), ('Русский', 2)], onchange=select_language)

loading = pygame_menu.Menu('Loading the Game...', 600, 400, theme=themes.THEME_DARK)
loading.add.progress_bar("Progress", progressbar_id="1", default=0, width=200, )

arrow = pygame_menu.widgets.LeftArrowSelection(arrow_size=(10, 15))

update_loading = pygame.USEREVENT + 0

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == update_loading:
            progress = loading.get_widget("1")
            progress.set_value(progress.get_value() + 1)
            if progress.get_value() == 100:
                gameLoop()
        if event.type == pygame.QUIT:
            exit()

    if mainmenu.is_enabled():
        mainmenu.update(events)
        mainmenu.draw(surface)
        if (mainmenu.get_current().get_selected_widget()):
            arrow.draw(surface, mainmenu.get_current().get_selected_widget())

    pygame.display.update()

