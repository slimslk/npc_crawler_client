import pygame


class LoginScreen:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.active_field = "login"
        self.login_text = ""
        self.password_text = ""
        self.finished = False

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                self.active_field = "password" if self.active_field == "login" else "login"

            elif event.key == pygame.K_BACKSPACE:
                if self.active_field == "login":
                    self.login_text = self.login_text[:-1]
                else:
                    self.password_text = self.password_text[:-1]

            elif event.key == pygame.K_RETURN:
                if self.active_field == "login":
                    self.active_field = "password"
                if self.active_field == "password" and self.login_text and self.password_text:
                    self.finished = True
                    return {"user_id": self.login_text, "password": self.password_text}

            elif event.key == pygame.QUIT:
                self.finished = True
                return None

            else:
                char = event.unicode
                if self.active_field == "login":
                    self.login_text += char
                else:
                    self.password_text += char

    def draw(self):
        self.screen.fill((0, 0, 0))

        login_label = self.font.render("Login:", True, (200, 200, 200))
        password_label = self.font.render("Password:", True, (200, 200, 200))

        login_surface = self.font.render(self.login_text, True, (255, 255, 255))
        password_surface = self.font.render("*" * len(self.password_text), True, (255, 255, 255))

        screen_rect = self.screen.get_rect()
        login_pos = (screen_rect.centerx - 100, screen_rect.centery - 40)
        password_pos = (screen_rect.centerx - 100, screen_rect.centery)

        self.screen.blit(login_label, (login_pos[0] - 120, login_pos[1]))
        self.screen.blit(password_label, (password_pos[0] - 120, password_pos[1]))

        pygame.draw.rect(self.screen, (80, 80, 80), (*login_pos, 200, 30), 2)
        pygame.draw.rect(self.screen, (80, 80, 80), (*password_pos, 200, 30), 2)

        self.screen.blit(login_surface, (login_pos[0] + 5, login_pos[1] + 5))
        self.screen.blit(password_surface, (password_pos[0] + 5, password_pos[1] + 5))

        active_rect = pygame.Rect(login_pos if self.active_field == "login" else password_pos, (200, 30))
        pygame.draw.rect(self.screen, (0, 200, 0), active_rect, 2)

        pygame.display.flip()
