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
    font_style = pygame.font.SysFont("ubuntu", 20)
    mesg = font_style.render(f'{line} {msg}', True, color)
    surface.blit(
        mesg,
        [
            (130),
            (line * mesg.get_height() * 1.4),
        ],
    )


def winners():
    winners_dct = database.read_database()
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
            msg = f'{user_dct["score"]} {user_dct["duration"]} {user_dct["username"]}'
            message(int(k), msg, yellow)
        pygame.display.update()
        

def snake():
    clock = pygame.time.Clock()
    user_name = user_input.get_value()
    
    x1 = surface.get_width() / 2
    y1 = surface.get_height() / 2

    x1_change = 0
    y1_change = 0

    snake_lst = []
    snake_length = 1

    foodx, foody = food_coords(snake_lst)
    
    tick_tmp = pygame.time.get_ticks()
    caption_tmp = pygame.display.get_caption()
    game_over = False
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            if event.type == pygame.KEYDOWN:
                x, y = event_dct.get(event.key, (0, 0))
                if x != 0 or y != 0:
                    x1_change = x * ss.seed
                    y1_change = y * ss.seed

        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_over = True

        x1 += x1_change
        y1 += y1_change

        surface.fill(blue)
        pygame.draw.rect(surface, red, [foodx, foody, ss.seed, ss.seed])
        
        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_lst.append(snake_head)
        if len(snake_lst) > snake_length:
            del snake_lst[0]

        for x in snake_lst[:-1]:
            if x == snake_head:
                game_over = True

        for x in snake_lst:
            pygame.draw.rect(surface, black, [x[0], x[1], ss.seed, ss.seed])
            
        if x1 == foodx and y1 == foody:
            foodx, foody = food_coords(snake_lst)
            snake_length += 1
        
        ticks60 = (pygame.time.get_ticks() - tick_tmp) // 60
        caption = f'{text_dct["user"]} {user_name} | {text_dct["score"]} {snake_length} | {text_dct["duration"]} {ticks60}'
        pygame.display.set_caption(caption)
        pygame.display.update()
        clock.tick(ss.seed)
    
    database.update_database(username=user_name, score=snake_length, duration=ticks60)
    pygame.display.set_caption(caption_tmp[0])
    

def select_language(value, lang):
    init_dct = database.load_json(ss.folder_name, ss.file_name)
    init_dct['language'] = lang
    database.save_json(ss.folder_name, ss.file_name, init_dct)

                        
if __name__ == '__main__':
    init_dct = database.load_json(ss.folder_name, ss.file_name)
    lang = init_dct.get('language', 'en')
    text_dct = ss.language[lang]['text']
    name_cur = ss.language[lang]['name']
    # lang_menu = [("English", 'en'), ("Русский", 'ru')]
    lang_menu = list()
    for k, v in ss.language.items():
        menu_tpl = (v['name'], k)
        if lang == k:
            lang_menu.insert(0, menu_tpl)
        else:
            lang_menu.append(menu_tpl)
        
    width = ss.width
    height = ss.height
    
    pygame.init()
    surface = pygame.display.set_mode((width, height))
    pygame.display.set_caption(text_dct['caption'])
    menu = pygame_menu.Menu(
        text_dct['menu'], 
        width, height, 
        theme=pygame_menu.themes.THEME_ORANGE
        )
    
    user_input = menu.add.text_input(text_dct['user'], default=database.get_fake_name())
    menu.add.selector(text_dct['language'], lang_menu, onchange=select_language)
    menu.add.button(text_dct['start'], snake)
    menu.add.button(text_dct['winners'], winners)
    menu.add.button(text_dct['exit'], pygame_menu.events.EXIT)

    menu.mainloop(surface)