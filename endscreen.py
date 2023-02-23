from time import sleep
import pygame
import pygame_menu
from pygame_menu import themes

pygame.init()
surface = pygame.display.set_mode((600, 400))

mainmenu = pygame_menu.Menu("Список лидеров", 600, 400, theme=themes.THEME_SOLARIZED)
mainmenu.add.label("Имя1")
mainmenu.add.label("счёт1")
mainmenu.add.label("Имя2")
mainmenu.add.label("счёт2")
mainmenu.add.label("Имя3")
mainmenu.add.label("счёт3")
mainmenu.add.button("Выйти", pygame_menu.events.EXIT)

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
        if mainmenu.get_current().get_selected_widget():
            arrow.draw(surface, mainmenu.get_current().get_selected_widget())

    pygame.display.update()
