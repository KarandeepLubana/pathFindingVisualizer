from __future__ import annotations
import pygame
from typing import List, Callable
from queue import PriorityQueue, Queue
from node import Node


def reconstruct_path(came_from, current_node, draw):
    while current_node in came_from:
        current_node = came_from[current_node]
        current_node.make_path()
        draw()


def dfs(draw: Callable, start: Node, end: Node):
    frontier = Queue()
    frontier_hash = set()
    came_from = dict()
    stack = [start]

    while stack is not None:
        current_node = stack.pop()
        frontier.put(current_node)
        frontier_hash.add(current_node)
        current_node.make_open()

        for neighbor in current_node.neighbors:
            if neighbor in frontier_hash:
                continue
            came_from[neighbor] = current_node
            if neighbor == end:
                reconstruct_path(came_from, end, draw)
                end.make_path()
                return True
            stack.append(neighbor)
        draw()

    return False


def h(p1, p2):
    """
    Return the manhattan distance from <p1> to <p2>
    """
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def a_star(draw: Callable, grid: List[List[Node]], start: Node, end: Node):
    count = 0
    frontier = PriorityQueue()
    frontier.put((0, count, start))
    came_from = dict()
    g_cost = {node: float("inf") for row in grid for node in row}
    g_cost[start] = 0
    f_cost = {node: float("inf") for row in grid for node in row}
    f_cost[start] = h(start.get_position(), end.get_position())

    frontier_hash = {start}

    while not frontier.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current_node = frontier.get()[2]
        frontier_hash.remove(current_node)
        current_node.make_closed()

        if current_node == end:
            reconstruct_path(came_from, end, draw)
            end.make_path()
            # end.make_end()
            # start.make_start()
            return True

        for neighbor in current_node.neighbors:
            if neighbor.is_closed():
                continue

            temp_g_cost = g_cost[current_node] + 1

            if temp_g_cost < g_cost[neighbor]:
                came_from[neighbor] = current_node
                g_cost[neighbor] = temp_g_cost
                f_cost[neighbor] = temp_g_cost + h(neighbor.get_position(),
                                                   end.get_position())
                if neighbor not in frontier_hash:
                    count += 1
                    frontier.put((f_cost[neighbor], count, neighbor))
                    frontier_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        # if current_node != start:
        #     current_node.make_closed()
    return None


def dijkstra(draw: Callable, grid: List[List[Node]], start: Node, end: Node):
    count = 0
    frontier = PriorityQueue()
    frontier.put((0, count, start))
    frontier_hash = {start}
    came_from = dict()
    g_cost = {node: float("inf") for row in grid for node in row}
    g_cost[start] = 0

    while not frontier.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current_node = frontier.get()[2]
        frontier_hash.remove(current_node)
        current_node.make_closed()

        if current_node == end:
            reconstruct_path(came_from, end, draw)
            end.make_path()
            return True

        for neighbor in current_node.neighbors:
            temp_g_cost = g_cost[current_node] + 1

            if temp_g_cost < g_cost[neighbor]:
                came_from[neighbor] = current_node
                g_cost[neighbor] = temp_g_cost

                if neighbor not in frontier_hash:
                    count += 1
                    frontier.put((temp_g_cost, count, neighbor))
                    frontier_hash.add(neighbor)
                    neighbor.make_open()

        draw()
    return False
