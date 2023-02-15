import pygame
import time
import random
from timer import timer

import settings

pygame.init()

white = settings.white
yellow = settings.yellow
black = settings.black
red = settings.red
green = settings.green
blue = settings.blue

dis_width = settings.dis_width
dis_height = settings.dis_height


dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption(settings.caption)

clock = pygame.time.Clock()

snake_block = 10
snake_speed = 10

font_style = pygame.font.SysFont("ubuntu", 15)
score_font = pygame.font.SysFont("ubuntu", 25)


def Timers():
    value = score_font.render("Время: " + str(1), True, black)
    dis.blit(value, [225, 0])


def winners():
    return {
        '1':'user1',
        '2':'user2',
        '3':'user3',
    }

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
            dis.fill(blue)
            message("Ты проиграл! Нажми C, чтобы играть или Q, чтобы выйти отсюда", black)
            Your_score(length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

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
        Timers()

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            length_of_snake += 1
        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()
