import pygame

class ImageButton:
    def __init__ (self, name, x, y, width, height, text, image_path, hover_image_path=None, sound_path=None):
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text



        self.image = image_path
        self.image = pygame.transform.scale(self.image, (width, height))
        self.hover_image = self.image
        if hover_image_path:
            self.hover_image = pygame.image.load(hover_image_path)
            self.hover_image = pygame.transform.scale(self.hover_image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.sound = None
        if sound_path:
            self.sound = pygame.mixer.Sound(sound_path)
        self.is_hovered = False

    def draw(self, screen, areaHeight):
        current_image = self.hover_image if self.is_hovered else self.image
        screen.blit(current_image, self.rect.topleft)

        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, (255,255,255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
            #self.sound.play()
            pygame.event.post(pygame.event.Event(pygame.USEREVENT+1, button=self.name))


class BoxButton(ImageButton):
    def __init__(self,name, x, y, width, height, text, image_path, hover_image_path=None, sound_path=None):
        ImageButton.__init__(self, name, x, y, width, height, text, image_path, hover_image_path, sound_path)
        self.is_hovered = False
    def draw(self, screen, areaHeight):
        screenHeight = screen.get_rect().height
        rounding = screenHeight // 36
        border = screenHeight // (270)
        color = (120, 122, 130)
        blockHeight = int(screenHeight // areaHeight * 0.9)
        area = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        translucentArea = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        if self.is_hovered:
            translucentArea.set_alpha(256)
        else:
            translucentArea.set_alpha(200)
        pygame.draw.rect(translucentArea, (0, 0, 0), (0, 0, self.width, self.height), self.height, rounding)
        pygame.draw.rect(translucentArea, color, (0, 0, self.width, self.height), border, rounding)
        area.blit(translucentArea, (0, 0))
        # area.blit(scoreText, (0 + screenHeight / 100, 0 + screenHeight / 100))
        area.blit(self.image, (self.width // 2 - self.width // 2, self.height // 2 - self.height // 2))
        screen.blit(area, (self.x, self.y))