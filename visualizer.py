from __future__ import annotations
import pygame
from typing import List
from algorithms import dfs, dijkstra, a_star
from node import Node
pygame.init()

SCREEN_WIDTH = 700
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_WIDTH))
pygame.display.set_caption("Path Finding Visualizer")

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


def make_grid(rows, width) -> List[List[Node]]:
    """
    Return a 2 by 2 matrix grid consisted of Nodes
    """
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)

            # Create outer barrier
            if i == 0 or j == 0 or i == rows - 1 or j == rows - 1:
                node.make_barrier()

    return grid


def draw_grid(screen, rows, width):
    gap = width // rows

    # draw horizontal lines of the grid
    for i in range(rows):
        pygame.draw.line(screen, GREY, (0, i*gap), (width, i*gap))

    # draw vertical lines of the grid
    for j in range(rows):
        pygame.draw.line(screen, GREY, (j*gap, 0), (j*gap, width))


def draw(screen, grid, rows, width):
    screen.fill(WHITE)

    # draw each node in the grid
    for row in grid:
        for node in row:
            node.draw(screen)

    draw_grid(screen, rows, width)
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    """
    Return row, col based on the clicked position x, y
    """
    gap = width // rows
    x, y = pos

    row = y // gap
    col = x // gap

    return row, col


def main(screen, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True
    started = False

    while run:
        draw(screen, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if started:
                continue

            if pygame.mouse.get_pressed(3)[0]:  # Left mouse button
                # Set the required color of the selected node
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                if not start:
                    start = node
                    start.make_start()
                elif not end and node != start:
                    end = node
                    end.make_end()
                elif node != end and node != start:
                    node.make_barrier()
            elif pygame.mouse.get_pressed(3)[2]:  # Right mouse button
                # Reset the selected node
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                if node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    # print("TRUE", event.key, pygame.K_SPACE)

                    # Get all the neighbors for each node in the grid
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    dijkstra(lambda: draw(screen, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

    pygame.quit()


if __name__ == "__main__":
    main(SCREEN, SCREEN_WIDTH)
