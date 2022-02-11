import pygame
import math
import random
import time
import itertools
import numba

def factorial(n):
    if n == 1:
        return 1
    return n * factorial(n - 1)

def get_distance(dot1, dot2):
    return math.sqrt((dot2[0] - dot1[0]) ** 2 + (dot2[1] - dot1[1]) ** 2)

def get_possible_total_distance(dots, order):
    total = float(0)
    for i in range(len(order)):
        dot_index = order[i]
        if i == 0:
            total += get_distance(dots[0], dots[dot_index])
        else:
            previous_dot_index = order[i - 1]
            total += get_distance(dots[previous_dot_index], dots[dot_index])
    final_dot_index = order[-1]
    total += get_distance(dots[final_dot_index], dots[0])
    return total

def draw_lines(order, dots):
    for i in range(len(order)):
        index = order[i]
        if i == 0:
            pygame.draw.line(screen, (0, 0, 0), dots[0], dots[index])
        else:
            previous_index = order[i - 1]
            pygame.draw.line(screen, (0, 0, 0), dots[previous_index], dots[index])
    pygame.draw.line(screen, (0, 0, 0), dots[index], dots[0])

# @numba.njit
def solve(dots, display):
    min_total = float("inf")
    min_order = None
    count = int()
    end_count = factorial(len(dots) - 1)
    for order in itertools.permutations([x + 1 for x in range(len(dots) - 1)]):
        total = get_possible_total_distance(dots, order)
        if total < min_total:
            min_total = total
            min_order = order
            display.fill((255, 255, 255))
            for i in range(len(order)):
                index = order[i]
                if i == 0:
                    pygame.draw.line(display, (255, 0, 0), dots[0], dots[index])
                else:
                    previous_index = order[i - 1]
                    pygame.draw.line(display, (255, 0, 0), dots[previous_index], dots[index])
            pygame.draw.line(display, (255, 0, 0), dots[index], dots[0])
            for dot in dots:
                pygame.draw.circle(display, (0, 0, 0), dot, 5)
            pygame.display.flip()
        count += 1
        if count % 1000 == 0:
            print("{}%".format(round(100 * count / end_count, 2)))
    return min_order

def main():
    pygame.init()
    pygame.display.set_caption("Traveling Salesman")
    screen = pygame.display.set_mode((800, 800))

    screen.fill((255, 255, 255))
    pygame.display.flip()

    dots = []

    running = True

    solution = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                dots.append(mouse)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    random.shuffle(dots)
                    start = time.time()
                    solution = solve(dots, screen)
                    end = time.time()
                    print("Length {} takes {} seconds.".format(len(solution) + 1, end - start))
        screen.fill((255, 255, 255))
        if solution != None:
            for i in range(len(solution)):
                index = solution[i]
                if i == 0:
                    pygame.draw.line(screen, (0, 0, 0), dots[0], dots[index])
                else:
                    previous_index = solution[i - 1]
                    pygame.draw.line(screen, (0, 0, 0), dots[previous_index], dots[index])
            pygame.draw.line(screen, (0, 0, 0), dots[index], dots[0])
        for dot in dots:
            pygame.draw.circle(screen, (0, 0, 0), dot, 5)
        pygame.display.flip()


if __name__ == "__main__":
    main()
