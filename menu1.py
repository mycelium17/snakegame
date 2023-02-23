import os
import json
import pygame
import pygame_menu
import random
import settings_snake as ss

width = ss.width
height = ss.height


def game1():
    user_name = user_input.get_value()
    print(f'{user_name=}')


def game():
    score = 0
    user_name = user_input.get_value()
    
    while True:
        x = random.randint(0, 10)
        y = random.randint(0, 10)
        z = x + y
        print(str(x) + "+" + str(y))
        result = int(input())
        if result == z:
            print("Correct")
            score = score + 5
            
        else:
            if result != z:
                stop = input("Wrong! Wanna stop? ")
                if stop == ("yes"):
                    print("You have " + str(score) + " points")
                    break
                else:
                    continue

def select_language(value, lang):
    init_dct = load_json(ss.folder_name, ss.file_name)
    init_dct['language'] = lang
    save_json(ss.folder_name, ss.file_name, init_dct)


def load_json(folder_name, file_name):
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
    filename = os.path.join(folder_name, file_name)
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            json.dump(dict(), f, ensure_ascii=True)
    with open(filename, encoding="utf-8") as f:
        load_dct = json.load(f)
    return load_dct


def save_json(folder_name, file_name, save_dct):
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
    filename = os.path.join(folder_name, file_name)
    with open(filename, "w") as f:
        json.dump(save_dct, f)
        
                        
if __name__ == '__main__':
    init_dct = load_json(ss.folder_name, ss.file_name)
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
        
    
    pygame.init()
    surface = pygame.display.set_mode((width, height))
    pygame.display.set_caption(text_dct['caption'])
    menu = pygame_menu.Menu(
        text_dct['menu'], 
        width, height, 
        theme=pygame_menu.themes.THEME_ORANGE
        )
    
    user_input = menu.add.text_input(text_dct['user'])
    menu.add.selector(text_dct['language'], lang_menu, onchange=select_language)
    menu.add.button(text_dct['start'], game1)
    menu.add.button(text_dct['exit'], pygame_menu.events.EXIT)

    menu.mainloop(surface)