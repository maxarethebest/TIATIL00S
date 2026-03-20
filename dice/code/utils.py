import pygame

def check_quit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True


def object_movement(screen, object, start_x, start_y, direction, iteration_distance, iterations):
    
    x_mult = 1
    y_mult = 1
    match direction:
        
        case "N":
            x_mult = 0
            y_mult = -1
        case "NE":
            x_mult = 1
            y_mult = -1
        case "E":
            x_mult = 1
            y_mult = 0
        case "SE":
            x_mult = 1
            y_mult = 1
        case "S":
            x_mult = 0
            y_mult = 1
        case "SW":
            x_mult = -1
            y_mult = 1
        case "W":
            x_mult = -1
            y_mult = 0
        case "NW":
            x_mult = -1
            y_mult = -1
    
    
    for iteration in iterations:     
         
        x_location = start_x + iteration_distance * iteration * x_mult
        y_location = start_y + iteration_distance * iteration * y_mult
        
        screen.blit(object, )