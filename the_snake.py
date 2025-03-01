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


DEFAULT_POSITION = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)


pygame.display.set_caption('Змейка')


clock = pygame.time.Clock()


class GameObject:
    """Class for Game Objects"""

    def __init__(self, position=DEFAULT_POSITION, color=None) -> None:
        self.position = position
        self.body_color = color

    def draw(self) -> None:
        """Method for drawing objects"""
        pass

    def draw_cell(self, position, color) -> None:
        """Method for drawing single cell"""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Class for logic of Apple"""

    def __init__(self) -> None:
        super().__init__(color=APPLE_COLOR)
        self.randomize_position()

    def draw(self) -> None:
        """Drawing object Apple"""
        self.draw_cell(self.position, self.body_color)

    def randomize_position(self, snake_positions=None) -> None:
        """Method for randomizing position of Apple"""
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if snake_positions and self.position in snake_positions:
                continue
            break


class Snake(GameObject):
    """Class for the logic of Snake"""

    def __init__(self) -> None:
        super().__init__(color=SNAKE_COLOR)
        self.reset()

    def reset(self) -> None:
        """Method for resetting Snake"""
        self.length = 1
        self.positions = [DEFAULT_POSITION]
        self.direction = RIGHT
        self.next_direction = None

    def update_direction(self) -> None:
        """Method for updating the direction of the Snake"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self) -> tuple[int, int]:
        """Method for getting the head position of Snake"""
        return self.positions[0]

    def get_head_new_position(self) -> tuple[int, int]:
        """Method for calculating the new position of the snake's head"""
        current_x = self.get_head_position()
        current_y = self.get_head_position()
        direction_x, direction_y = self.direction
        return (
            (current_x[0] + (direction_x * GRID_SIZE)) % SCREEN_WIDTH,
            (current_y[1] + (direction_y * GRID_SIZE)) % SCREEN_HEIGHT
        )

    def move(self) -> None:
        """Method for moving the Snake"""
        new_position = self.get_head_new_position()
        self.positions.insert(0, new_position)

        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self) -> None:
        """Method for drawing the Snake"""
        for position in self.positions:
            self.draw_cell(position, self.body_color)


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
        snake.move()
        snake.update_direction()

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            continue

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake_positions=snake.positions)

        screen.fill(BOARD_BACKGROUND_COLOR)

        snake.draw()
        apple.draw()

        pygame.display.flip()


if __name__ == '__main__':
    main()
