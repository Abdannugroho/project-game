# FILE: game_main.py
import pygame
import sys
import time
import random
import math
from modules.maze_gen import generate_maze_prim
from modules.ai_agent import EnemyFSM

# --- CONFIG ---
CELL_SIZE = 32
GRID_W, GRID_H = 25, 19
SCREEN_WIDTH = CELL_SIZE * GRID_W
SCREEN_HEIGHT = CELL_SIZE * GRID_H + 80
FPS = 60

# Warna Background
BG_COLOR = (15, 10, 20)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("UAS Graph Theory: Cute Dungeon")
clock = pygame.time.Clock()

# Font
try:
    font_main = pygame.font.Font(None, 40)
    font_sub = pygame.font.Font(None, 24)
except:
    font_main = pygame.font.SysFont("arial", 30, bold=True)
    font_sub = pygame.font.SysFont("consolas", 18)

class Game:
    def __init__(self):
        self.load_assets()
        self.reset_game()

    def load_assets(self):
        try:
            # Load gambar yang baru digenerate
            self.img_player = pygame.transform.scale(pygame.image.load("assets/player.png"), (CELL_SIZE, CELL_SIZE))
            self.img_enemy = pygame.transform.scale(pygame.image.load("assets/enemy.png"), (CELL_SIZE, CELL_SIZE))
            self.img_goal = pygame.transform.scale(pygame.image.load("assets/goal.png"), (CELL_SIZE, CELL_SIZE))
            self.img_wall = pygame.transform.scale(pygame.image.load("assets/wall.png"), (CELL_SIZE, CELL_SIZE))
            self.img_floor = pygame.transform.scale(pygame.image.load("assets/floor.png"), (CELL_SIZE, CELL_SIZE))
            
            # Load Suara
            self.snd_move = pygame.mixer.Sound("assets/move.wav")
            self.snd_alert = pygame.mixer.Sound("assets/alert.wav")
            self.snd_win = pygame.mixer.Sound("assets/win.wav")
            self.snd_lose = pygame.mixer.Sound("assets/lose.wav")
        except Exception as e:
            print("Error asset:", e)
            print("Jalankan 'generate_assets.py' dulu!")
            sys.exit()

    def reset_game(self):
        # 1. Buat Map Baru
        self.maze = generate_maze_prim(GRID_W, GRID_H)
        
        # 2. Player
        self.player_pos = [1, 1]
        
        # 3. Goal (Cari titik valid pojok)
        self.goal_pos = [GRID_W-2, GRID_H-2]
        while self.maze[self.goal_pos[1], self.goal_pos[0]] == 0:
            self.goal_pos = [self.goal_pos[0]-1, self.goal_pos[1]-1]

        # 4. Musuh (Spawn jauh dari player)
        while True:
            ex, ey = random.randint(1, GRID_W-2), random.randint(1, GRID_H-2)
            if self.maze[ey, ex] == 1:
                if (abs(ex - 1) + abs(ey - 1)) > 10:
                    self.enemy_pos = [ex, ey]
                    break
        
        # 5. Reset AI & Status
        self.enemy_brain = EnemyFSM()
        self.last_enemy_move = time.time()
        self.enemy_speed = 0.5
        self.game_over = False
        self.win = False
        self.alert_played = False
        print("Game Reset!") # Debug print

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    # --- PERBAIKAN 1: RESET SELALU JALAN ---
                    # Ditaruh paling atas, tidak peduli status menang/kalah
                    if event.key == pygame.K_r:
                        self.reset_game()
                        continue # Skip sisa kode, langsung frame baru

                    # Gerak Player (Hanya kalau main)
                    if not self.game_over and not self.win:
                        dx, dy = 0, 0
                        if event.key == pygame.K_LEFT: dx = -1
                        elif event.key == pygame.K_RIGHT: dx = 1
                        elif event.key == pygame.K_UP: dy = -1
                        elif event.key == pygame.K_DOWN: dy = 1
                        
                        nx, ny = self.player_pos[0]+dx, self.player_pos[1]+dy
                        if 0 <= nx < GRID_W and 0 <= ny < GRID_H:
                            if self.maze[ny, nx] == 1: # Cek jalan
                                self.player_pos = [nx, ny]
                                self.snd_move.play()

            # --- LOGIC ---
            if not self.game_over and not self.win:
                # Cek Menang
                if self.player_pos == self.goal_pos:
                    self.win = True
                    self.snd_win.play()
                
                # Cek Kalah
                if self.player_pos == self.enemy_pos:
                    self.game_over = True
                    self.snd_lose.play()

                # AI Move
                curr_time = time.time()
                if curr_time - self.last_enemy_move > self.enemy_speed:
                    next_step = self.enemy_brain.update(tuple(self.enemy_pos), tuple(self.player_pos), self.maze)
                    self.enemy_pos = list(next_step)
                    self.last_enemy_move = curr_time
                    
                    # Suara Musuh Marah
                    if self.enemy_brain.state == "CHASE" and not self.alert_played:
                        self.snd_alert.play(); self.alert_played = True
                    elif self.enemy_brain.state == "PATROL":
                        self.alert_played = False

            # --- GAMBAR ---
            screen.fill(BG_COLOR)

            # Map
            for y in range(GRID_H):
                for x in range(GRID_W):
                    pos = (x*CELL_SIZE, y*CELL_SIZE)
                    if self.maze[y, x] == 0: screen.blit(self.img_wall, pos)
                    else: screen.blit(self.img_floor, pos)

            # Animasi Denyut Lucu
            pulse = 1.0 + 0.05 * math.sin(time.time() * 6)
            
            def draw_anim(img, grid_pos, scale=1.0):
                size = int(CELL_SIZE * scale)
                s_img = pygame.transform.scale(img, (size, size))
                off = (size - CELL_SIZE)//2
                screen.blit(s_img, (grid_pos[0]*CELL_SIZE - off, grid_pos[1]*CELL_SIZE - off))

            # Gambar Aktor
            draw_anim(self.img_goal, self.goal_pos, pulse)
            draw_anim(self.img_player, self.player_pos, 1.0) # Player stabil
            
            # Musuh membesar kalau marah
            e_scale = 1.1 if self.enemy_brain.state == "CHASE" else 1.0
            draw_anim(self.img_enemy, self.enemy_pos, e_scale)

            # --- UI ---
            pygame.draw.rect(screen, (30, 25, 40), (0, SCREEN_HEIGHT-80, SCREEN_WIDTH, 80))
            
            # Status AI
            if self.enemy_brain.state == "CHASE":
                st_txt, st_col = "MUSUH: MENGEJAR!", (255, 100, 100)
            else:
                st_txt, st_col = "MUSUH: PATROLI", (100, 255, 100)
            screen.blit(font_main.render(st_txt, True, st_col), (20, SCREEN_HEIGHT-65))
            screen.blit(font_sub.render("Panah: Gerak | 'R': Peta Baru | Cari Bintang Kuning!", True, (200, 200, 200)), (20, SCREEN_HEIGHT-30))

            # Overlay Menang/Kalah
            if self.game_over or self.win:
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 180))
                screen.blit(overlay, (0,0))
                
                if self.win:
                    t1, c1 = "KAMU MENANG!", (100, 255, 100)
                else:
                    t1, c1 = "YAH... TERTANGKAP", (255, 100, 100)
                
                txt1 = font_main.render(t1, True, c1)
                txt2 = font_sub.render("Tekan 'R' untuk main lagi", True, (255, 255, 255))
                
                cx, cy = SCREEN_WIDTH//2, SCREEN_HEIGHT//2
                screen.blit(txt1, txt1.get_rect(center=(cx, cy-20)))
                screen.blit(txt2, txt2.get_rect(center=(cx, cy+20)))

            pygame.display.flip()
            clock.tick(FPS)

if __name__ == "__main__":
    Game().run()