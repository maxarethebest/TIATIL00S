import pygame
from settings import *
from utils import *

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game name placeholder")

running = True
while running:
    
    running = check_quit()
            
    # for event in pygame.event.get():
    #     if event.type == pygame.MOUSEBUTTONDOWN:
    #         ...
    screen.blit()
    
    screen.fill((RED))
    
    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
