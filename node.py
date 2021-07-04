from __future__ import annotations
from typing import Tuple, List
import pygame
# from main import RED, GREEN, WHITE, BLACK, PURPLE, ORANGE, TURQUOISE

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Node:
    def __init__(self, row, col, width, total_rows) -> None:
        self.row = row
        self.col = col
        self.x = col * width
        self.y = row * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_position(self) -> Tuple[int, int]:
        """
        Return the indexed position of the Node
        """
        return self.row, self.col

    def is_closed(self) -> bool:
        """
        Return true if the node is closed/explored
        """
        return self.color == RED

    def is_open(self) -> bool:
        """
        Return true if the Node is open to explore
        """
        return self.color == GREEN

    def is_barrier(self) -> bool:
        """
        Return true if the Node is a barrier, otherwise return false
        """
        return self.color == BLACK

    def is_start(self) -> bool:
        return self.color == ORANGE

    def is_end(self) -> bool:
        return self.color == TURQUOISE

    def reset(self):
        """
        Reset the node back to the original board color
        """
        self.color = WHITE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def make_start(self):
        self.color = ORANGE

    def draw(self, screen):
        rectangle = pygame.Rect(self.x, self.y, self.width, self.width)
        pygame.draw.rect(screen, self.color, rectangle)

    def update_neighbors(self, grid: List[List[Node]]):
        self.neighbors = []

    # Checking if the TOP node from the current node is a valid node to explore
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])

    # Checking if the LEFT node from the current node is a valid node to explore
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])

    # Checking if BOTTOM node from the current node is a valid node to explore
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])

    # Checking if the RIGHT node from the current node is a valid node
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])

    def __lt__(self, other):
        return False
