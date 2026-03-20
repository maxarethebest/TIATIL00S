# main.py - Huvudfilen för DDRP.
# __author__: Max Valentin
# __version__: 1.0
# __email__: max.valentin@elev.ga.dbgy.se

import pygame
import sys
from pathlib import Path
from songs import SONGS

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()


PIXEL_SCALE = 8

number_path = Path("ddrp/assets/images/numbers")
HIGHSCORE_FILE = "ddrp/assets/data/highscore.txt"

numbers = {}

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("DDR-P")
clock = pygame.time.Clock()


for i in range(10):
    img = pygame.image.load(number_path / f"{i}icon.png").convert_alpha()
    img = pygame.transform.scale(
        img,
        (img.get_width()*PIXEL_SCALE, img.get_height()*PIXEL_SCALE)
    )
    numbers[i] = img

WHITE = (255,255,255)


GAME_WIDTH = 600
GAME_HEIGHT = 600
ARROW_SIZE = 145
LANE_GAP = 4
ARROW_SPEED = 3

HIT_TOLERANCE = 50

GAME_X = (SCREEN_WIDTH - GAME_WIDTH) // 2
GAME_Y = (SCREEN_HEIGHT - GAME_HEIGHT) // 2
HIT_ZONE_Y = 474

TRAVEL_DISTANCE = HIT_ZONE_Y - (GAME_Y - ARROW_SIZE)
TRAVEL_TIME_MS = int((TRAVEL_DISTANCE / ARROW_SPEED) * (1000 / FPS))


def load_img(path):
    return pygame.image.load(path).convert_alpha()

def draw_number(screen, numbers, value, x, y, spacing=4):
    for digit in str(value):
        img = numbers[int(digit)]
        screen.blit(img, (x, y))
        x += img.get_width() + spacing
        
def try_load_img(path):
    try:
        return load_img(path)
    except pygame.error as e:
        print(f"Error loading image '{path}': {e}")
        return None

def load_highscore():
    try:
        with open(HIGHSCORE_FILE, "r") as f:
            return int(f.read())
    except Exception:
        # Om filen inte finns eller inte går att läsa
        return 0

def save_highscore(score):
    try:
        with open(HIGHSCORE_FILE, "w") as f:
            f.write(str(score))
    except Exception as e:
        print(f"[ERROR] Kunde inte spara highscore: {e}")
    
arrow_up_img = try_load_img("ddrp/assets/images/arrowup145x145.png")
arrow_down_img = try_load_img("ddrp/assets/images/arrowdown145x145.png")
arrow_left_img = try_load_img("ddrp/assets/images/arrowleft145x145.png")
arrow_right_img = try_load_img("ddrp/assets/images/arrowright145x145.png")

bg_img = try_load_img("ddrp/assets/images/ddr_borders_witharrowsat474_600x600.png")

play_button_img = try_load_img("ddrp/assets/images/playbutton21x7.png")
play_button_img = pygame.transform.scale(play_button_img,(play_button_img.get_width()*8,play_button_img.get_height()*8))


ARROW_IMAGES = {
    "UP": arrow_up_img,
    "DOWN": arrow_down_img,
    "LEFT": arrow_left_img,
    "RIGHT": arrow_right_img,
}

LANES = {
    "LEFT":  GAME_X + LANE_GAP,
    "DOWN":  GAME_X + (ARROW_SIZE + LANE_GAP * 2),
    "UP":    GAME_X + (ARROW_SIZE * 2 + LANE_GAP * 3),
    "RIGHT": GAME_X + (ARROW_SIZE * 3 + LANE_GAP * 4),
}

KEY_BINDINGS = {            #Funkar med WASD och piltangentetr
    pygame.K_w: "UP",
    pygame.K_UP: "UP",
    pygame.K_s: "DOWN",
    pygame.K_DOWN: "DOWN",
    pygame.K_a: "LEFT",
    pygame.K_LEFT: "LEFT",
    pygame.K_d: "RIGHT",
    pygame.K_RIGHT: "RIGHT",
}

highscore = load_highscore()

running = True
game_state = "MENU"
music_started = False

arrows = []
score = 0

current_song = None
absolute_chart = []
chart_index = 0
song_start_time = 0

font = pygame.font.SysFont(None,36)
big_font = pygame.font.SysFont(None,64)


class Arrow:

    def __init__(self,direction):
        self.direction = direction
        self.image = ARROW_IMAGES[direction]
        self.x = LANES[direction]
        self.y = GAME_Y - ARROW_SIZE
        self.hit = False

    def update(self):
        self.y += ARROW_SPEED

    def draw(self):
        screen.blit(self.image,(self.x,self.y))

    def center_y(self):
        return self.y + ARROW_SIZE//2

class ImageButton:

    def __init__(self,image,x,y):
        self.image = image
        self.rect = image.get_rect(topleft=(x,y))

    def draw(self):
        screen.blit(self.image,self.rect)

    def clicked(self,event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)


play_button = ImageButton(play_button_img,SCREEN_WIDTH//2-play_button_img.get_width()//2,260)


while running:

    clock.tick(FPS)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False


        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:

                if game_state == "LEVEL_SELECT":
                    game_state = "MENU"
                else:
                    running = False
            
            if game_state == "RESULT":

                if event.key == pygame.K_RETURN:

                    game_state = "MENU"

            if game_state == "PLAYING" and event.key in KEY_BINDINGS:

                direction = KEY_BINDINGS[event.key]

                for arrow in arrows:

                    if arrow.direction == direction and not arrow.hit:

                        accuracy = abs(arrow.center_y() - HIT_ZONE_Y)

                        if accuracy < HIT_TOLERANCE:
                            arrow.hit = True
                            match accuracy:
                                case a if a < 1:
                                    score += 25
                                    #PERFECT
                                case a if a < 5:
                                    score += 10
                                    #GREAT
                                case a if a < 10:
                                    score += 5
                                    #GOOD
                                case a if a < 25:
                                    score += 3
                                    #OK
                                case _:
                                    score += 1
                            break

        if game_state == "MENU":

            if play_button.clicked(event):

                current_song = SONGS[0]

                absolute_chart = []
                t = 0

                for delta,dirs in current_song["chart"]:
                    t += delta
                    absolute_chart.append((t,dirs))

                arrows.clear()
                score = 0
                chart_index = 0

                song_start_time = pygame.time.get_ticks()

                pygame.mixer.music.load(current_song["music"])
                
                if absolute_chart:
                    min_hit_time = min(hit_time for hit_time, _ in absolute_chart)
                    delay = current_song.get("delay", 0)
                    music_start_delay = min_hit_time + current_song["start_offset"] - delay
                else:
                    music_start_delay = 0
                
                music_started = False
                
                game_state = "PLAYING"



    if game_state == "PLAYING" and current_song:

        song_time = pygame.time.get_ticks() - song_start_time
        
        if not music_started and song_time >= music_start_delay:
            pygame.mixer.music.play()
            music_started = True
        
        while chart_index < len(absolute_chart):

            hit_time,dirs = absolute_chart[chart_index]

            spawn_time = hit_time - TRAVEL_TIME_MS + current_song["start_offset"]
            if song_time >= spawn_time:

                for d in dirs:
                    arrows.append(Arrow(d))

                chart_index += 1

            else:
                break

        for arrow in arrows:
            arrow.update()

        arrows = [a for a in arrows if a.y < GAME_Y+GAME_HEIGHT and not a.hit]

        if chart_index >= len(absolute_chart) and not arrows:
            game_state = "RESULT"
            
            if score > highscore:
                highscore = score
                save_highscore(highscore)


    screen.fill("lightblue")


    if game_state == "MENU":

        title = big_font.render("DDR-P",True,WHITE)
        screen.blit(title,(SCREEN_WIDTH//2-title.get_width()//2,140))
        
        highscore_text = font.render(f"Highscore: {highscore}", True, WHITE)
        screen.blit(highscore_text, (SCREEN_WIDTH//2 - highscore_text.get_width()//2, 400))
        
        play_button.draw()

    elif game_state == "LEVEL_SELECT":

        title = big_font.render("SELECT SONG",True,WHITE)

        screen.blit(title,(SCREEN_WIDTH//2-title.get_width()//2,140))

    elif game_state == "RESULT":

        title = big_font.render("RESULT",True,WHITE)
        screen.blit(title,(SCREEN_WIDTH//2-title.get_width()//2,150))
        
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, 250))

        highscore_text = font.render(f"Highscore: {highscore}", True, WHITE)
        screen.blit(highscore_text, (SCREEN_WIDTH//2 - highscore_text.get_width()//2, 300))

        retry = font.render("Press ENTER to play again", True, WHITE)
        screen.blit(retry, (SCREEN_WIDTH//2 - retry.get_width()//2, 350))




    elif game_state == "PLAYING":
        
        screen.blit(bg_img,(100,0))

        for arrow in arrows:
            arrow.draw()
            
        draw_number(screen, numbers, score, 702, 20)

    pygame.display.flip()

pygame.quit()
sys.exit()