import pygame, os, random

pygame.init()
pygame.mixer.init()

SIZESCREEN = WIDTH, HEIGHT = 1000, 560
screen = pygame.display.set_mode(SIZESCREEN)
clock = pygame.time.Clock()

path = os.path.join(os.getcwd(), 'images')
file_names = os.listdir(path)
BACKGROUND = pygame.image.load(os.path.join(path, 'background.png')).convert()
file_names.remove('background.png')
BACKGROUND2 = pygame.image.load(os.path.join(path, 'background2.png')).convert()
file_names.remove('background2.png')
IMAGES = {}
for file_name in file_names:
    try:
        image_name = file_name[:-4].upper()
        IMAGES[image_name] = pygame.image.load(os.path.join(path, file_name)).convert_alpha()
    except pygame.error as e:
        print(f"Error loading image {file_name}: {e}")

ICE_CREAM_IMAGES = {
    'LEMON': IMAGES['LEMON'],
    'VANILLA': IMAGES['VANILLA'],
    'CHOCO': IMAGES['CHOCO'],
    'STRAWBERRY': IMAGES['STRAWBERRY'],
    'VANILLA_SPRINKLES': IMAGES['VANILLA_SPRINKLES'],
    'VANILLA_ICING': IMAGES['VANILLA_ICING'],
    'VANILLA_ICING_SPRINKLES': IMAGES['VANILLA_ICING_SPRINKLES'],
    'CHOCO_SPRINKLES': IMAGES['CHOCO_SPRINKLES'],
    'CHOCO_ICING': IMAGES['CHOCO_ICING'],
    'CHOCO_ICING_SPRINKLES': IMAGES['CHOCO_ICING_SPRINKLES'],
    'LEMON_SPRINKLES': IMAGES['LEMON_SPRINKLES'],
    'LEMON_ICING': IMAGES['LEMON_ICING'],
    'LEMON_ICING_SPRINKLES': IMAGES['LEMON_ICING_SPRINKLES'],
    'STRAWBERRY_SPRINKLES': IMAGES['STRAWBERRY_SPRINKLES'],
    'STRAWBERRY_ICING': IMAGES['STRAWBERRY_ICING'],
    'STRAWBERRY_ICING_SPRINKLES': IMAGES['STRAWBERRY_ICING_SPRINKLES']
}

DARKPINK = pygame.Color(209, 146, 197, 255)
LIGHTPINK = pygame.Color(230, 193, 222, 255)
BLACK = pygame.color.THECOLORS['black']

path2 = os.path.join(os.getcwd(), 'music')
pygame.mixer.music.load(os.path.join(path2, 'bgmusic.ogg'))
correct = pygame.mixer.Sound(os.path.join(path2, 'correct.ogg'))
wrong = pygame.mixer.Sound(os.path.join(path2, 'wrong.ogg'))
correct.set_volume(0.2)
wrong.set_volume(0.2)

class Waiter(pygame.sprite.Sprite):
    def __init__(self, images, cx, cy):
        super().__init__()
        self.images = images
        self.image = images['WAITERR']
        self.rect = self.image.get_rect(center=(cx, cy))
        self.step_index = self.points = self._count = 0
        self.lives = 3
        self.steps_right = ['WAITERS1R', 'WAITERR', 'WAITERS2R', 'WAITERR']
        self.steps_left = ['WAITERS1L', 'WAITERL', 'WAITERS2L', 'WAITERL']
        self.horizontal_direction = 'RIGHT'
        self.holding_ice_cream = self.current_flavor = self.text = None
        self.toppings, self.text_time = [], None
        self.text_font = pygame.font.SysFont(None, 36)
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        if self.holding_ice_cream:
            if self.horizontal_direction == 'LEFT':
                ice_cream_pos = (self.rect.centerx + 20, self.rect.top)
            else:
                ice_cream_pos = (self.rect.centerx - 70, self.rect.top)
            surface.blit(self.holding_ice_cream, ice_cream_pos)
        if self.text:
            message_surf = self.text_font.render(self.text, True, (255, 0, 0))
            surface.blit(message_surf, (self.rect.centerx - 30, self.rect.top - 40))
        for i in range(self.lives):
            surface.blit(IMAGES['LIFE'], (400 + i * 65, 0))
        points_surf = self.text_font.render(f'Points: {self.points}', True, BLACK)
        surface.blit(points_surf, (620, 40))

    def update(self, key_pressed, obiekty):
        self.get_event(key_pressed)

        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.centerx < 0:
            self.rect.centerx = 0
        if self.rect.centerx > WIDTH:
            self.rect.centerx = WIDTH

        if any(key_pressed):
            self._count += 1
            if self._count % 10 == 0:
                self.step_index = (self.step_index + 1) % 4
                if self.horizontal_direction == 'RIGHT':
                    self.image = self.images[self.steps_left[self.step_index]]
                else:
                    self.image = self.images[self.steps_right[self.step_index]]
        else:
            if self.horizontal_direction == 'RIGHT':
                self.image = self.images['WAITERL']
            else:
                self.image = self.images['WAITERR']
            self.step_index = 0

        if self.text and pygame.time.get_ticks() - self.text_time > 2000:
            self.text = None

    def get_event(self, key_pressed):
        move_x, move_y = 0, 0
        if key_pressed[pygame.K_a]:
            move_x = -4
            self.horizontal_direction = "RIGHT"
        if key_pressed[pygame.K_d]:
            move_x = 4
            self.horizontal_direction = "LEFT"
        if key_pressed[pygame.K_w]:
            move_y = -4
        if key_pressed[pygame.K_s]:
            move_y = 4

        self.move_and_check_collision(move_x, move_y)

    def move_and_check_collision(self, move_x, move_y):
        self.rect.x += move_x
        self.rect.y += move_y

        collided = pygame.sprite.spritecollideany(self, tables_group) or pygame.sprite.spritecollideany(self, containers_group)
        if collided:
            self.rect.x -= move_x
            self.rect.y -= move_y

        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.centerx < 0:
            self.rect.centerx = 0
        if self.rect.centerx > WIDTH:
            self.rect.centerx = WIDTH

    def pick_ice_cream(self, ice_cream_image, flavor):
        if self.holding_ice_cream is None:
            if 'SPRINKLES' in flavor or 'ICING' in flavor:
                pass
            else:
                self.holding_ice_cream = ice_cream_image
                self.current_flavor = flavor
                self.toppings = []

        else:
            if 'SPRINKLES' in flavor or 'ICING' in flavor:
                if self.holding_ice_cream:
                    topping_type = flavor.split('_')[-1]
                    if topping_type not in self.toppings:
                        self.toppings.append(topping_type)
                        new_flavor = self.current_flavor
                        if 'SPRINKLES' in new_flavor or 'ICING' in new_flavor:
                            new_flavor = new_flavor.split('_')[0]
                        for topping in sorted(self.toppings):
                            new_flavor += f'_{topping}'
                        if new_flavor in ICE_CREAM_IMAGES:
                            self.holding_ice_cream = ICE_CREAM_IMAGES[new_flavor]
                            self.current_flavor = new_flavor

            else:
                if 'SPRINKLES' in self.current_flavor or 'ICING' in self.current_flavor:
                    self.current_flavor = flavor

                else:
                    self.holding_ice_cream = ice_cream_image
                    self.current_flavor = flavor
                    self.toppings = []




    def drop_ice_cream(self):
        self.holding_ice_cream = self.current_flavor = None
        self.toppings = []

    def deliver_order(self, tables):
        if self.holding_ice_cream:
            for table in tables:
                if self.rect.colliderect(table.get_expanded_rect()):
                    if table.bubble and self.current_flavor == table.correct_flavor:
                        self.points += 10
                        table.clear_order()
                        self.text = 'CORRECT'
                        correct.play()
                    else:
                        self.lives -= 1
                        self.text = 'WRONG'
                        wrong.play()
                        table.clear_order()
                    self.text_time = pygame.time.get_ticks()
                    self.drop_ice_cream()

                    break

    def is_in_selection_area(self, selection_area):
        return self.rect.colliderect(selection_area.rect)

class Item(pygame.sprite.Sprite):
    def __init__(self, image, cx, cy):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(cx, cy))
    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Table(Item):
    def __init__(self, image, cx, cy, initial_delay, waiter):
        super().__init__(image, cx, cy)
        self.bubble = self.exclamation = self.correct_flavor = None
        self.bubble_time = self.initial_time = pygame.time.get_ticks()
        self.initial_delay = initial_delay
        self.waiter = waiter
    def draw(self, surface):
        super().draw(surface)
        if self.bubble:
            surface.blit(IMAGES['BUBBLE'], (self.rect.centerx - 50, self.rect.top - 60))
            surface.blit(self.bubble, (self.rect.centerx - 30, self.rect.top - 60))
        if self.exclamation:
            surface.blit(self.exclamation, (self.rect.centerx + 10, self.rect.top - 50))

    def clear_order(self):
        self.bubble = self.exclamation = self.correct_flavor = None
        self.initial_time = pygame.time.get_ticks()

    def set_bubble(self, bubble):
        self.bubble, self.bubble_time = pygame.transform.scale(bubble, (
        int(bubble.get_width() * 0.8), int(bubble.get_height() * 0.8))), pygame.time.get_ticks()
        self.exclamation = None

    def update(self):
        current_time = pygame.time.get_ticks()
        elapsed_time_since_start = current_time - self.initial_time
        if elapsed_time_since_start >= self.initial_delay:
            if self.bubble is None and self.exclamation is None:
                new_flavor = random.choice(list(ICE_CREAM_IMAGES.keys()))
                self.set_bubble(ICE_CREAM_IMAGES[new_flavor])
                self.correct_flavor = new_flavor

            if self.bubble:
                elapsed_time = current_time - self.bubble_time
                if elapsed_time > 10000 and self.exclamation is None:
                    self.exclamation = IMAGES['EXCLAMATION']
                if elapsed_time > 17000:
                    self.clear_order()
                    self.waiter.lives -= 1
                    self.waiter.text = "TOO LATE"
                    self.waiter.text_time = pygame.time.get_ticks()

    def get_expanded_rect(self):
        return self.rect.inflate(40, 40)

class Container(Item):
    def __init__(self, image, cx, cy, flavor):
        super().__init__(image, cx, cy)
        self.original_image = image
        self.enlarged_image = pygame.transform.scale(image,(int(image.get_width() * 1.1), int(image.get_height() * 1.1)))
        self.flavor = flavor

    def draw(self, surface):
        super().draw(surface)

    def enlarge(self):
        self.image, self.rect = self.enlarged_image, self.enlarged_image.get_rect(center=self.rect.center)

    def shrink(self):
        self.image, self.rect = self.original_image, self.original_image.get_rect(center=self.rect.center)

class Button:
    def __init__(self, text, text_color, background_color, width, height, pc_x, pc_y, font_size=36, font_type="Consolas"):
        self.text = str(text)
        self.text_color = text_color
        self.background_color = background_color
        self.width = width
        self.height = height
        self.font_size = font_size
        self.font_type = font_type
        self.font = pygame.font.SysFont(self.font_type, self.font_size)
        self.pc_x = pc_x
        self.pc_y = pc_y
        self.update()

    def update(self):
        self.image = self.font.render(self.text, True, self.text_color)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.pc_x, self.pc_y
        self.text_rect = self.image.get_rect(center=self.rect.center)

    def draw(self, surface):
        surface.fill(self.background_color, self.rect)
        surface.blit(self.image, self.text_rect)



player = Waiter({'WAITERR': IMAGES['WAITERR'],
                 'WAITERS1R': IMAGES['WAITERS1R'],
                 'WAITERS2R': IMAGES['WAITERS2R'],
                 'WAITERL': IMAGES['WAITERL'],
                 'WAITERS1L': IMAGES['WAITERS1L'],
                 'WAITERS2L': IMAGES['WAITERS2L']}, 500, 500)
tables = [
    Table(IMAGES['TABLE'], 110, 120, 3000, player),
    Table(IMAGES['TABLE'], 500, 230, 5000, player),
    Table(IMAGES['TABLE'], 875, 150, 10000, player),
    Table(IMAGES['TABLE'], 870, 490, 15000, player)
]

containers = [
    Container(IMAGES['CONTAINER_LEMON'], 40, 510, "LEMON"),
    Container(IMAGES['CONTAINER_CHOCO'], 110, 510, "CHOCO"),
    Container(IMAGES['CONTAINER_STRAWBERRY'], 180, 510, "STRAWBERRY"),
    Container(IMAGES['CONTAINER_VANILLA'], 250, 510, "VANILLA"),
    Container(IMAGES['SPRINKLES'], 50, 250, "VANILLA_SPRINKLES"),
    Container(IMAGES['ICING'], 50, 385, "VANILLA_ICING"),
]

chairs = [
    Item(IMAGES['CHAIR_L'], 40, 110),
    Item(IMAGES['CHAIR_R'], 190, 110),
    Item(IMAGES['CHAIR_L'], 430, 220),
    Item(IMAGES['CHAIR_R'], 580, 220),
    Item(IMAGES['CHAIR_L'], 805, 140),
    Item(IMAGES['CHAIR_R'], 955, 140),
    Item(IMAGES['CHAIR_L'], 800, 480),
    Item(IMAGES['CHAIR_R'], 950, 480)
]

tables_group = pygame.sprite.Group(tables)
containers_group = pygame.sprite.Group(containers)


choice = Item(IMAGES['CHOICE'], 180, 370)
start_button = Button("START", BLACK, LIGHTPINK, 150, 50, WIDTH//3-40, 500, 32)
quit_button = Button("QUIT", BLACK, LIGHTPINK, 150, 50, (WIDTH//3)+160, 500, 32)
controls_button = Button("CONTROLS", BLACK, LIGHTPINK, 150, 50, (WIDTH//3)+360, 500, 32)
game_over = Button("GAME OVER", BLACK, LIGHTPINK, 300, 100, WIDTH//2, HEIGHT//2, 40)


game_state = 'menu'
window_open = True
active_game = False
try:
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)
except pygame.error as e:
    print(f"Error playing background music: {e}")
while window_open:

    screen.blit(BACKGROUND, (0, 0))
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            window_open = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                window_open = False
                active_game = False
            elif event.key == pygame.K_q:
                player.drop_ice_cream()
            elif event.key == pygame.K_SPACE:
                player.deliver_order(tables)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if game_state == 'menu':
                if start_button.rect.collidepoint(mouse_pos):
                    game_state = 'game'
                elif quit_button.rect.collidepoint(mouse_pos):
                    window_open = False
                elif controls_button.rect.collidepoint(mouse_pos):
                    game_state = 'controls'
                    controls_start_time = pygame.time.get_ticks()

    mouse_pos = pygame.mouse.get_pos()
    if game_state == 'menu':
        if start_button.rect.collidepoint(mouse_pos):
            start_button.background_color = LIGHTPINK
            start_button.text_color = BLACK
        else:
            start_button.background_color = DARKPINK
            start_button.text_color = BLACK
        if quit_button.rect.collidepoint(mouse_pos):
            quit_button.background_color = LIGHTPINK
            quit_button.text_color = BLACK
        else:
            quit_button.background_color = DARKPINK
            quit_button.text_color = BLACK
        if controls_button.rect.collidepoint(mouse_pos):
            controls_button.background_color = LIGHTPINK
            controls_button.text_color = BLACK
        else:
            controls_button.background_color = DARKPINK
            controls_button.text_color = BLACK
        screen.blit(BACKGROUND2, (0, 0))
        start_button.draw(screen)
        quit_button.draw(screen)
        controls_button.draw(screen)

    elif game_state == 'game':
        active_game = True
        for container in containers:
            if container.rect.collidepoint(mouse_pos):
                container.enlarge()
            else:
                container.shrink()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if player.is_in_selection_area(choice):
                for container in containers:
                    if container.rect.collidepoint(mouse_pos):
                        player.pick_ice_cream(ICE_CREAM_IMAGES[container.flavor], container.flavor)

        for table in tables:
            table.update()
            table.draw(screen)
        for chair in chairs:
            chair.draw(screen)
        for container in containers:
            container.draw(screen)
        choice.draw(screen)

        player.draw(screen)
        player.update(pygame.key.get_pressed(), tables)
        if not player.lives:
            game_state = 'game_over'
            game_over_start_time = pygame.time.get_ticks()

    elif game_state == 'game_over':
        if pygame.time.get_ticks() - game_over_start_time < 5000:
            game_over.draw(screen)
        else:
            game_state = 'menu'

    elif game_state == 'controls':
        if pygame.time.get_ticks() - controls_start_time < 5000:
            controls_text = Button("Controls: ", BLACK, LIGHTPINK, 750, 50, WIDTH//2, HEIGHT//2-150, 40)
            controls_text2 = Button("Drop ice cream -> Q", BLACK, LIGHTPINK, 750, 50, WIDTH // 2, HEIGHT // 2-100, 40)
            controls_text3 = Button("Deliver order -> Space", BLACK, LIGHTPINK, 750, 50, WIDTH // 2, HEIGHT // 2 - 50, 40)
            controls_text4 = Button("Choose ice cream -> Leftclick", BLACK, LIGHTPINK, 750, 50, WIDTH // 2, HEIGHT // 2 , 40)
            controls_text.draw(screen)
            controls_text2.draw(screen)
            controls_text3.draw(screen)
            controls_text4.draw(screen)
        else:
            game_state = 'menu'

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
