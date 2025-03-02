from random import choice, randint

import pygame  # Пустая строка добавлена для isort

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP, DOWN, LEFT, RIGHT = (0, -1), (0, 1), (-1, 0), (1, 0)

# Цвета:
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для объектов игры."""

    def __init__(self, x=0, y=0, color=(255, 255, 255)):
        """Инициализация объекта."""
        self.position = (x, y)
        self.body_color = color

    def draw(self, screen):
        """Отрисовывает объект на экране."""
        rect = pygame.Rect(
            self.position[0], self.position[1], GRID_SIZE, GRID_SIZE
        )
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)  # Рамка


class Apple(GameObject):
    """Класс яблока."""

    def __init__(self):
        """Создает яблоко в случайной позиции."""
        super().__init__(
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
            APPLE_COLOR,
        )

    def randomize_position(self):
        """Генерирует новую позицию яблока."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        )


class Snake(GameObject):
    """Класс змейки."""

    def __init__(self):
        """Создает змейку в центре экрана."""
        x, y = GRID_WIDTH // 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE
        super().__init__(x, y, SNAKE_COLOR)
        self.body = [self.position]
        self.positions = self.body  # Атрибут, ожидаемый тестами
        self.direction = choice((UP, DOWN, LEFT, RIGHT))
        self.next_direction = self.direction

    def get_head_position(self):
        """Возвращает текущую позицию головы змейки."""
        return self.body[0]

    def update_direction(self, new_direction):
        """Меняет направление движения змейки."""
        self.next_direction = new_direction

    def move(self):
        """Двигает змейку в текущем направлении."""
        self.direction = self.next_direction
        head_x, head_y = self.body[0]
        dir_x, dir_y = self.direction
        new_head = (
            (head_x + dir_x * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dir_y * GRID_SIZE) % SCREEN_HEIGHT,
        )

        if new_head in self.body:
            self.reset()

        self.body = [new_head] + self.body[:-1]
        self.positions = self.body  # Обновляем positions

    def grow(self):
        """Добавляет новый сегмент к змейке."""
        self.body.append(self.body[-1])
        self.positions = self.body

    def reset(self):
        """Сбрасывает змейку при столкновении с самой собой."""
        self.__init__()

    def draw(self, screen):
        """Отрисовывает змейку на экране."""
        for segment in self.body:
            self.position = segment
            super().draw(screen)


def handle_keys(snake):
    """Обрабатывает нажатие клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.update_direction(UP)
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.update_direction(DOWN)
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.update_direction(LEFT)
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.update_direction(RIGHT)


def main():
    """Запускает игру."""
    pygame.init()
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.grow()
            apple.randomize_position()

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()


if __name__ == '__main__':  # Исправлена кавычка (Q000)
    main()
