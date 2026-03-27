import pygame

class Button:
    HOLD_DELAY = 400
    HOLD_RATE  = 60
 
    def __init__(self, x, y, w, h, text, action,
                 color=(180, 180, 220), repeatable=False):
        self.rect         = pygame.Rect(x, y, w, h)
        self.text         = text
        self.action       = action
        self.color        = color
        self.hover_color  = tuple(min(255, c + 35) for c in color)
        self.is_hovered   = False
        self.repeatable   = repeatable
        self._held        = False
        self._hold_timer  = 0
        self._last_repeat = 0
 
    def draw(self, screen, font):
        col = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, col, self.rect, border_radius=5)
        pygame.draw.rect(screen, (80, 80, 80), self.rect, 1, border_radius=5)
        txt = font.render(self.text, True, (20, 20, 20))
        screen.blit(txt, (
            self.rect.x + (self.rect.w - txt.get_width())  // 2,
            self.rect.y + (self.rect.h - txt.get_height()) // 2,
        ))
 
    def update(self, mp):
        self.is_hovered = self.rect.collidepoint(mp)
 
    def on_mouse_down(self, pos):
        if self.rect.collidepoint(pos):
            self.action()
            if self.repeatable:
                self._held        = True
                self._hold_timer  = pygame.time.get_ticks()
                self._last_repeat = pygame.time.get_ticks()
 
    def on_mouse_up(self, _pos):
        self._held = False
 
    def tick(self):
        if self._held and self.repeatable:
            now = pygame.time.get_ticks()
            if now - self._hold_timer >= self.HOLD_DELAY:
                if now - self._last_repeat >= self.HOLD_RATE:
                    self.action()
                    self._last_repeat = now
 
    def click(self, pos):
        if self.rect.collidepoint(pos):
            self.action()