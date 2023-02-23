import pygame 

width = 640
height = 480


if __name__ == '__main__':
    print('.' * 60)
    pygame.init()
    display = pygame.display.set_mode((width, height))
    background = pygame.Surface((width, height))
    text_color = (200, 200, 200, 255)
    font = pygame.font.SysFont("verdana", 30)
    text_value = "username"
    text = font.render(text_value, True, text_color)
    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    text_value = text_value[:-1]
                    text = font.render(text_value, True, text_color)
                if event.key == pygame.K_RETURN:
                    print(text_value)
            if event.type == pygame.TEXTINPUT:
                text_value += event.text
                text = font.render(text_value, True, text_color)

        display.blit(background, (100, 100))
        display.blit(text, (100, 100))
        pygame.display.update()
    
    print('1' * 60)
    