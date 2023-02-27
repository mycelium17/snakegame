import pygame
import time
import random
import database
from pygame_menu import themes
from time import sleep
import pygame_menu

import settings_snake as ss


white = pygame.colordict.THECOLORS["whitesmoke"]
blue = pygame.colordict.THECOLORS["deepskyblue1"]
yellow = pygame.colordict.THECOLORS["lightyellow"]
black = pygame.colordict.THECOLORS["black"]
green = pygame.colordict.THECOLORS["forestgreen"]
red = pygame.colordict.THECOLORS["tomato3"]


event_dct = {
    pygame.K_LEFT: (-1, 0),
    pygame.K_RIGHT: (1, 0),
    pygame.K_UP: (0, -1),
    pygame.K_DOWN: (0, 1),
}


class Dot:
    color = (0, 0, 0, 255)

    def __init__(self, *args, **kwargs):
        self.color = kwargs.get("color", self.color)
        self.x = kwargs.get("x")
        self.y = kwargs.get("y")

    def __repr__(self):
        return f"({self.x}, {self.y})"


class Apple(Dot):
    color = pygame.colordict.THECOLORS["tomato3"]

    def __init__(self, *args, **kwargs):
        self.x = kwargs.get("x")
        self.y = kwargs.get("y")

    @staticmethod
    def create(snake_list=list()):
        while True:
            x = get_random(surface.get_width(), ss.seed)
            y = get_random(surface.get_height(), ss.seed)
            if (x, y) not in snake_list:
                apple = Apple(x=x, y=y)
                return apple


class Snake:
    color = pygame.colordict.THECOLORS["black"]

    def __init__(self, *args, **kwargs):
        self.color = kwargs.get("color", self.color)
        self.body = list()

    @staticmethod
    def create():
        snake = Snake()
        x = get_random(surface.get_width(), ss.seed)
        y = get_random(surface.get_height(), ss.seed)
        snake.add(x=x, y=y)
        return snake

    def add(self, x, y):
        bd = Dot(x=x, y=y, color=self.color)
        self.body.insert(0, bd)

    def is_collapse(self, dx, dy, dot):
        head = self.body[0]
        if head.x + dx == dot.x and head.y + dy == dot.y:
            return True
        return False

    def can_movie(self, dx, dy):
        if dx == 0 and dy == 0:
            return True
        if not self.body:
            return False
        head = self.body[0]
        # Достиг ли края экрана?
        if 0 > dx + head.x:
            return False
        if dx + head.x > surface.get_width() - 1:
            return False
        if 0 > dy + head.y:
            return False
        if dy + head.y > surface.get_height() - 1:
            return False
        # Съел сам себя?
        for body in self.body:
            if dx + head.x == body.x and dy + head.y == body.y:
                return False
        return True

    def move(self, dx, dy, clone):
        head = self.body[0]
        self.add(x=dx + head.x, y=dy + head.y)
        if not clone:
            self.body = self.body[:-1]

    def __repr__(self):
        body_lst = [f"({b.x}, {b.y})" for b in self.body]
        body = f"[{', '.join(body_lst)}]"
        return body


def get_random(max, size):
    ret = size * random.randrange(0, max // size)
    return ret


def food_coords(snake_list):
    """
    Подбор места для появления еды
    """
    while True:
        foodx = get_random(surface.get_width(), ss.seed)
        foody = get_random(surface.get_height(), ss.seed)
        if [foodx, foody] not in snake_list:
            return foodx, foody


def message(line, msg, color):
    """
    Вывод сообщения по центру экрана, в зависимости от размера надписи
    """
    font_path = os.path.join(ss.folder_name, ss.font_name)
    font_style = pygame.font.SysFont(font_path, 30)
    mesg = font_style.render(f"{line}. {msg}", True, color)
    surface.blit(
        mesg,
        [
            (130),
            (line * mesg.get_height() * 1.4 + 20),
        ],
    )



def winners():
    return read_database()

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

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_over = True
                if event.key == pygame.K_SPACE:
                    game_over = True
                if event.key == pygame.K_RETURN:
                    game_over = True
        surface.fill(green)

        for k, user_dct in winners_dct.items():
            msg = f'{text_dct["score"]} {user_dct["score"]} {text_dct["duration"]} {user_dct["duration"]} {text_dct["user"]} {user_dct["username"]}'
            message(int(k), msg, yellow)
        pygame.display.update()


def snake_games():
    clock = pygame.time.Clock()
    user_name = user_input.get_value()

    snake = Snake.create()
    apple = Apple.create(snake.body)
    caption_tmp = pygame.display.get_caption()
    tick_tmp = pygame.time.get_ticks()

    dx = 0
    dy = 0
    game_over = False

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

                if event.key == pygame.K_ESCAPE:
                    game_over = True
                if event.key == pygame.K_SPACE:
                    game_over = True
                if event.key == pygame.K_RETURN:
                    game_over = True

                x, y = event_dct.get(event.key, (0, 0))
                if x != 0 or y != 0:
                    dx = x * ss.seed
                    dy = y * ss.seed

        if not snake.can_movie(dx, dy):
            game_over = True
        is_collapse = snake.is_collapse(dx, dy, apple)
        snake.move(dx, dy, clone=is_collapse)
        if is_collapse:
            del apple
            apple = Apple.create(snake.body)

        surface.fill(blue)
        pygame.draw.rect(surface, red, [apple.x, apple.y, ss.seed, ss.seed])
        ticks60 = (pygame.time.get_ticks() - tick_tmp) // 60
        for dot in snake.body:
            pygame.draw.rect(surface, dot.color, [dot.x, dot.y, ss.seed, ss.seed])

        snake_length = len(snake.body) - 1
        caption = f'{text_dct["user"]} {user_name} | {text_dct["score"]} {snake_length} | {text_dct["duration"]} {ticks60}'
        pygame.display.set_caption(caption)
        pygame.display.update()
        clock.tick(ss.speed)

    database.update_database(username=user_name, score=snake_length, duration=ticks60)
    pygame.display.set_caption(caption_tmp[0])


def select_screen(value, screen):
    init_dct = database.load_json(ss.folder_name, ss.file_name)
    init_dct["screen"] = screen
    database.save_json(ss.folder_name, ss.file_name, init_dct)


def select_fullscreen(value, fullscreen):
    init_dct = database.load_json(ss.folder_name, ss.file_name)
    init_dct["fullscreen"] = fullscreen
    database.save_json(ss.folder_name, ss.file_name, init_dct)


def select_username(username):
    init_dct = database.load_json(ss.folder_name, ss.file_name)
    init_dct["username"] = username.strip()
    database.save_json(ss.folder_name, ss.file_name, init_dct)


def select_language(value, lang):
    init_dct = database.load_json(ss.folder_name, ss.file_name)
    init_dct["language"] = lang.strip()
    database.save_json(ss.folder_name, ss.file_name, init_dct)


if __name__ == "__main__":
    init_dct = database.load_json(ss.folder_name, ss.file_name)
    lang = init_dct.get("language", "en")
    username = init_dct.get("username", database.get_fake_name())
    fullscreen = init_dct.get("fullscreen", ss.fullscreen)
    screen = init_dct.get("screen", f"{ss.width},{ss.height}")

    text_dct = ss.language[lang]["text"]

    lang_menu = list()
    for k, v in ss.language.items():
        menu_tpl = (v["name"], k)
        if lang == k:
            lang_menu.insert(0, menu_tpl)
        else:
            lang_menu.append(menu_tpl)

    width, height = screen.split(",")
    width = int(width)
    height = int(height)

    screen_menu = list()
    for size in ss.screen_size:
        if (width, height) == size:
            screen_menu.insert(0, (f"({size[0]}, {size[1]})", f"{size[0]},{size[1]}"))
        else:
            screen_menu.append((f"({size[0]}, {size[1]})", f"{size[0]},{size[1]}"))

    if fullscreen:
        fullscreen_menu = [(text_dct["yes"], True), (text_dct["no"], False)]
    else:
        fullscreen_menu = [(text_dct["no"], False), (text_dct["yes"], True)]

    fs = pygame.FULLSCREEN if fullscreen else 0
    pygame.init()
    surface = pygame.display.set_mode((width, height), fs)
    pygame.display.set_caption(text_dct["caption"])
    menu = pygame_menu.Menu(
        text_dct["menu"], width, height, theme=pygame_menu.themes.THEME_ORANGE
    )

    user_input = menu.add.text_input(
        text_dct["user"],
        default=username,
        onchange=select_username,
        onreturn=select_username,
    )
    menu.add.selector(text_dct["language"], lang_menu, onchange=select_language)
    menu.add.selector(
        text_dct["fullscreen"], fullscreen_menu, onchange=select_fullscreen
    )
    menu.add.selector(text_dct["screen"], screen_menu, onchange=select_screen)
    menu.add.button(text_dct["start"], snake_games)
    menu.add.button(text_dct["winners"], winners)
    menu.add.button(text_dct["exit"], pygame_menu.events.EXIT)

    menu.mainloop(surface)

