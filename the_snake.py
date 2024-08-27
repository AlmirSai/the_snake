"""Snake game logic"""


from random import randint

import pygame


SCREEN_WIDTH: int = 640
SCREEN_HEIGHT: int = 480
GRID_SIZE: int = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE


UP: tuple[int, int] = (0, -1)
DOWN: tuple[int, int] = (0, 1)
LEFT: tuple[int, int] = (-1, 0)
RIGHT: tuple[int, int] = (1, 0)


BOARD_BACKGROUND_COLOR: tuple[int, int, int] = (0, 0, 0)


BORDER_COLOR: tuple[int, int, int] = (93, 216, 228)


APPLE_COLOR: tuple[int, int, int] = (255, 0, 0)


SNAKE_COLOR: tuple[int, int, int] = (0, 255, 0)


SPEED = 20


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)


pygame.display.set_caption('Змейка')


clock = pygame.time.Clock()


class GameObject:
    """Class for Game Objects"""

    def __init__(self) -> None:
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self) -> None:
        """Method for drawing objects"""
        pass


class Apple(GameObject):
    """Class for logic of Apple"""

    def __init__(self) -> None:
        super().__init__()
        self.body_color: tuple[int, int, int] = APPLE_COLOR
        self.position = None
        self.randomize_position()

    def draw(self) -> None:
        """Drawing object Apple"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self) -> None:
        """Method for randomizing position of Apple"""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )


class Snake(GameObject):
    """CLass for logic of Snake"""

    def __init__(self) -> None:
        super().__init__()
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color: tuple[int, int, int] = SNAKE_COLOR
        self.last = None

    def update_direction(self) -> None:
        """Method for parsing next coordinates"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self) -> None:
        """Method for moving Snake position"""
        current = self.get_head_position()
        x, y = self.direction
        new_position = (
            ((current[0] + (x * GRID_SIZE)) % SCREEN_WIDTH),
            (current[1] + (y * GRID_SIZE)) % SCREEN_HEIGHT
        )

        if new_position in self.positions[1:]:
            self.reset()
        else:
            self.positions.insert(0, new_position)

            if len(self.positions) > self.length:
                self.last = self.positions.pop()

    def draw(self) -> None:
        """Method for drawing Snake"""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self) -> tuple[int, int]:
        """Method for parsing head position of Snake"""
        return self.positions[0]

    def reset(self) -> None:
        """Method for reset Snake"""
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = RIGHT


def handle_keys(game_object) -> None:
    """Function for parsing keys"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main() -> None:
    """Function for starting game"""
    pygame.init()

    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
