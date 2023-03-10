import os
import pygame
import random
import database
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
        # ???????????? ???? ???????? ?????????????
        if 0 > dx + head.x:
            return False
        if dx + head.x > surface.get_width() - 1:
            return False
        if 0 > dy + head.y:
            return False
        if dy + head.y > surface.get_height() - 1:
            return False
        # ???????? ?????? ?????????
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


def winners():
    winners_dct = database.read_database()
    user_dct = winners_dct[list(winners_dct.keys())[0]]
    score_max_num = len(str(user_dct["score"]))
    duration_max_num = len(str(user_dct["duration"]))
    for k, user_dct in winners_dct.items():
        score_max_num = score_max_num if score_max_num > len(str(user_dct["score"])) else len(str(user_dct["score"]))
        duration_max_num = duration_max_num if duration_max_num > len(str(user_dct["duration"])) else len(str(user_dct["duration"]))
    
    pygame.init()
    width = surface.get_width()
    height = surface.get_height()
    column = 1 if surface.get_width() < 1000 else 2
    font_size = 20 if height < 1000 else 30    
    font_style = pygame.font.SysFont('Courier New', font_size)
    mesg_lst = list()
    mesg_max_width = 0
    mesg_max_height = 0
    for k, user_dct in winners_dct.items():
        msg_lst = list()
        msg_lst.append(f'{k:0{2}}.')
        msg_lst.append(f'{text_dct["score"]}{user_dct["score"]:0{score_max_num}}')
        msg_lst.append(f'{text_dct["duration"]}{user_dct["duration"]:0{duration_max_num}}')
        msg_lst.append(f'{text_dct["user"]}{user_dct["username"]}')
        msg = ' '.join(msg_lst)
        mesg = font_style.render(msg, True, black)
        mesg_lst.append(mesg)
        mesg_max_height = mesg_max_height if mesg_max_height > mesg.get_height() else mesg.get_height()
        mesg_max_width = mesg_max_width if mesg_max_width > mesg.get_width() else mesg.get_width()

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
        
        surface.fill(red)
        start_y = (height - (len(mesg_lst) // column * 2 * mesg_max_height)) // 2
        for num, mesg in enumerate(mesg_lst):
            if column == 1:
                mx = (width - mesg_max_width) // 2
                my = start_y + (num * mesg_max_height * 2)
                surface.blit(mesg, [(mx), (my)])
            elif column == 2:
                cl = 1 if len(mesg_lst) // 2 <= num else 0
                mx = ((width // column) - mesg_max_width) // 2 + cl * (width // column)
                my = start_y + ((num - (len(mesg_lst) // 2 * cl)) * mesg_max_height * 2)
                surface.blit(mesg, [(mx), (my)])
        
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
