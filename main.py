import pygame
import sys


class FarmClicker:
    def __init__(self):
        # 1️ Инициализация Pygame
        pygame.init()
        self.width, self.height = 400, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("🌾 Pygame Farm Clicker")
        self.clock = pygame.time.Clock()  # Для контроля FPS

        #  Шрифты (SysFont использует системные шрифты)
        self.font_small = pygame.font.SysFont("Arial", 18)
        self.font_big = pygame.font.SysFont("Arial", 24, bold=True)

        #  Игровые переменные
        self.money = 0
        self.click_value = 1
        self.auto_income = 0
        self.click_cost = 10
        self.auto_cost = 50
        self.last_auto_tick = pygame.time.get_ticks()  # Время последнего начисления автодохода

        #  Прямоугольники (границы кликабельных зон)
        self.field_rect = pygame.Rect(100, 150, 200, 100)
        self.click_btn_rect = pygame.Rect(50, 320, 300, 50)
        self.auto_btn_rect = pygame.Rect(50, 420, 300, 50)

    def handle_events(self):
        """Обработка событий (закрытие окна, клики мыши)"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Левая кнопка мыши
                pos = pygame.mouse.get_pos()

                if self.field_rect.collidepoint(pos):
                    self.money += self.click_value
                elif self.click_btn_rect.collidepoint(pos):
                    self.buy_click_upgrade()
                elif self.auto_btn_rect.collidepoint(pos):
                    self.buy_auto_upgrade()

    def buy_click_upgrade(self):
        """Покупка улучшения клика"""
        if self.money >= self.click_cost:
            self.money -= self.click_cost
            self.click_value += 1
            self.click_cost = int(self.click_cost * 1.5)  # Цена растёт на 50%

    def buy_auto_upgrade(self):
        """Покупка автоматического дохода"""
        if self.money >= self.auto_cost:
            self.money -= self.auto_cost
            self.auto_income += 5
            self.auto_cost = int(self.auto_cost * 1.8)  # Цена растёт на 80%

    def update(self):
        """Логика, не зависящая от отрисовки"""
        now = pygame.time.get_ticks()
        if now - self.last_auto_tick >= 1000:  # Каждую секунду (1000 мс)
            self.money += self.auto_income
            self.last_auto_tick = now

    def draw_button(self, rect, label, cost, is_active):
        """Отрисовка кнопки с учётом наведения и доступности"""
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = rect.collidepoint(mouse_pos)

        # Цвета кнопок
        if not is_active:
            color = (169, 169, 169)  # Серый (недоступно)
        elif is_hovered:
            color = (255, 220, 100) if rect == self.click_btn_rect else (255, 160, 50)
        else:
            color = (255, 215, 0) if rect == self.click_btn_rect else (255, 140, 0)

        pygame.draw.rect(self.screen, color, rect)
        pygame.draw.rect(self.screen, (0, 0, 0), rect, 2)  # Чёрная обводка

        # Текст кнопки
        btn_text = self.font_small.render(f"{label} - {cost}💰", True, (0, 0, 0))
        text_rect = btn_text.get_rect(center=rect.center)
        self.screen.blit(btn_text, text_rect)

    def draw(self):
        """Отрисовка всех элементов на экране"""
        self.screen.fill((144, 238, 144))  # Светло-зелёный фон

        #  Поле для кликов
        mouse_pos = pygame.mouse.get_pos()
        field_hover = self.field_rect.collidepoint(mouse_pos)
        field_color = (124, 220, 124) if field_hover else (100, 200, 100)
        pygame.draw.rect(self.screen, field_color, self.field_rect)
        pygame.draw.rect(self.screen, (0, 0, 0), self.field_rect, 2)

        field_text = self.font_big.render("КЛИКНИ СЮДА", True, (255, 255, 255))
        field_text_rect = field_text.get_rect(center=self.field_rect.center)
        self.screen.blit(field_text, field_text_rect)

        #  Статистика
        money_text = self.font_big.render(f"Монеты: {self.money}", True, (0, 0, 0))
        self.screen.blit(money_text, (110, 20))

        stats_text = self.font_small.render(f"За клик: +{self.click_value} | Авто: +{self.auto_income}/сек", True,
                                            (0, 0, 0))
        self.screen.blit(stats_text, (50, 60))

        #  Кнопки улучшений
        can_buy_click = self.money >= self.click_cost
        can_buy_auto = self.money >= self.auto_cost

        self.draw_button(self.click_btn_rect, "Улучшить клик (+1)", self.click_cost, can_buy_click)
        self.draw_button(self.auto_btn_rect, "Нанять фермера (+5/с)", self.auto_cost, can_buy_auto)

        pygame.display.flip()  # Обновляем экран

    def run(self):
        """Главный игровой цикл"""
        while True:
            self.handle_events()  # 1. События
            self.update()  # 2. Обновление логики
            self.draw()  # 3. Отрисовка
            self.clock.tick(60)  # Ограничение до 60 кадров/сек


if __name__ == "__main__":
    game = FarmClicker()
    game.run()