import os.path
from typing import Callable

import pygame

pygame.init()
_size = width, height = 300, 300
_main_screen = pygame.display.set_mode(_size)


def load_image(filename: str | os.PathLike, colorkey=None) -> pygame.Surface:
    fullname = os.path.join('data', filename)
    if not os.path.isfile(fullname):
        pass
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class MainHero(pygame.sprite.Sprite):
    main_hero_image = load_image('MainHero.png')

    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = MainHero.main_hero_image
        self.rect = self.image.get_rect()

    def move(self, way):
        function_dict: dict[int, Callable] = {pygame.K_DOWN: lambda: setattr(self.rect, 'y', self.rect.y + 10),
                                              pygame.K_UP: lambda: setattr(self.rect, 'y', self.rect.y - 10),
                                              pygame.K_RIGHT: lambda: setattr(self.rect, 'x', self.rect.x + 10),
                                              pygame.K_LEFT: lambda: setattr(self.rect, 'x', self.rect.x - 10)}
        function_dict[way]()


class MainWindow:
    def __init__(self):
        self.fps = 60
        self.size = _size
        self.screen = _main_screen
        self.main_sprite_group = pygame.sprite.Group()
        self.main_hero = MainHero(self.main_sprite_group)

    @property
    def width(self):
        return self.size[0]

    @property
    def height(self):
        return self.size[1]

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            self.screen.fill(pygame.Color('white'))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_DOWN, pygame.K_UP, pygame.K_RIGHT, pygame.K_LEFT):
                        self.main_hero.move(event.key)

            self.main_sprite_group.draw(self.screen)
            self.main_sprite_group.update()

            pygame.display.flip()
            clock.tick(self.fps)
        pygame.quit()


if __name__ == '__main__':
    window = MainWindow()
    window.run()
