#Cellular automaton
#ruleset:
#Any live cell with fewer than two live neighbours dies.
#Any live cell with two or three live neighbours lives on to the next generation.
#Any live cell with more than three live neighbours dies, as if by overpopulation.
#Any dead cell with exactly three live neighbours becomes a live cell.

import pygame
import numpy as np
import random
import time

#Inputs
pygame.init()
pygame.display.set_caption("Game of live")
ROWS = int(input('Amount of rows: '))
COLUMNS = int(input('Amount of columns: '))
scaling_factor = 15
cells_size = (COLUMNS, ROWS)
window_size = (int(COLUMNS*scaling_factor), int(ROWS*scaling_factor))
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Conway's Game of Life")
FPS = 100
sec_per_step = 1
FramePerSec = pygame.time.Clock()
last_event_time = pygame.time.get_ticks()


#colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)



#creation
def create_cells(cells_size):
    cells = [0 for x in range(int(cells_size[0]*cells_size[1]))]
    return cells

cells = create_cells(cells_size)

def ind2coo(index):
    x = index%ROWS
    y = index//ROWS
    return (x,y)

def coo2ind(coord):
    x = coord[0]
    y = coord[1]
    return int(y*ROWS+x)

def neighbors(coords):
    '''input; The coords as a tupple
    
    output: indices the 8 (unless boarder) surrounding points as a set'''

    x = coords[0]
    y = coords[1]
    neighbors_coords = [(x,y+1),(x,y-1),(x+1,y),(x+1,y+1),(x+1,y-1),(x-1,y),(x-1,y+1),(x-1,y-1)]
    neighbors = set()
    for nbr in neighbors_coords:
        if nbr[0]>=0 and nbr[1]>=0 and nbr[0]<ROWS and nbr[1]<COLUMNS:
            result = coo2ind(nbr)
            neighbors.add(result)
    return neighbors
    
def new_gen(cells):
    new_gen = cells[:] #creates a copy?

    for i, cell in enumerate(cells):
        coords = ind2coo(i)
        if cell == 1: #rules for a living cell
            sum = 0
            for nbr in neighbors(coords):
                #looking at other neighbors
                if cells[nbr] == 0:
                    for adj in neighbors(ind2coo(nbr)):
                        sum += cells[adj]
                    if sum == 3:
                        new_gen[nbr] = 1
                    sum = 0
            for nbr in neighbors(coords):
                sum += cells[nbr] 
            if sum < 2:
                new_gen[i] = 0
            elif sum == 2 or sum == 3:
                new_gen[i] = 1
            elif sum> 3:
                new_gen[i] = 0

    return new_gen

def draw(position):
    coords = ind2coo(position)
    x = coords[0]
    y = coords[1]
    pygame.draw.rect(screen, WHITE, [x*scaling_factor, y*scaling_factor, scaling_factor, scaling_factor])

#starting position alive cells
#list_starting_points = input("input the starting cells as (x,y) seperated by a space: ")
#tuple_strings = list_starting_points.split()
#tuple_list = []
#for tuple_str in tuple_strings:
    # Remove the parentheses and split by comma
    #tuple_elements = tuple_str.strip('()').split(',')
    # Convert the elements to integers and create a tuple
    #tuple_list.append((int(tuple_elements[0]), int(tuple_elements[1])))
#for starting_point in tuple_list:
    #cells[coo2ind(starting_point)]=1
#pygame.display.flip()



#main loop
running = True
toggle_sim = False
while running:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                toggle_sim = not toggle_sim
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            x = pos[0]//scaling_factor
            y = pos[1]//scaling_factor
            new_cell = coo2ind((x,y))
            cells[new_cell]=1

    #drawing
    screen.fill(BLACK)
    for i, cell in enumerate(cells):
        if cell == 1:
            draw(i)

    #new generation
    if toggle_sim:
        if current_time - last_event_time >= sec_per_step*1000:
            cells = new_gen(cells)
            print("simulating")
            last_event_time = current_time
    
    FramePerSec.tick(FPS)          

    pygame.display.flip()
           