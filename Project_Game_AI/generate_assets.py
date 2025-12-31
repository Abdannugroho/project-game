# FILE: generate_assets.py
import pygame
import os
import wave
import math
import struct

# Buat folder assets
if not os.path.exists("assets"):
    os.makedirs("assets")

pygame.init()

def create_sound(filename, frequency, duration, volume=0.5):
    """Membuat sound effect"""
    sample_rate = 44100
    n_samples = int(sample_rate * duration)
    with wave.open(f"assets/{filename}", 'w') as wav_file:
        wav_file.setnchannels(1); wav_file.setsampwidth(2); wav_file.setframerate(sample_rate)
        for i in range(n_samples):
            val = int(volume * 32767.0 * math.sin(2.0 * math.pi * frequency * i / sample_rate))
            val = int(val * ((n_samples - i) / n_samples))
            wav_file.writeframesraw(struct.pack('<h', val))
    print(f"Sound generated: {filename}")

def draw_bear(surf, color):
    """Menggambar Beruang Lucu (Boneka)"""
    # Telinga
    pygame.draw.circle(surf, color, (12, 12), 10)
    pygame.draw.circle(surf, color, (52, 12), 10)
    # Kepala
    pygame.draw.circle(surf, color, (32, 32), 26)
    # Mata Putih
    pygame.draw.circle(surf, (255, 255, 255), (22, 28), 8)
    pygame.draw.circle(surf, (255, 255, 255), (42, 28), 8)
    # Pupil Hitam
    pygame.draw.circle(surf, (0, 0, 0), (22, 28), 3)
    pygame.draw.circle(surf, (0, 0, 0), (42, 28), 3)
    # Hidung/Mulut
    pygame.draw.ellipse(surf, (255, 200, 200), (22, 40, 20, 14))
    pygame.draw.circle(surf, (0, 0, 0), (32, 44), 3)

def draw_ghost(surf, color):
    """Menggambar Hantu/Monster"""
    # Badan
    pygame.draw.circle(surf, color, (32, 28), 24)
    pygame.draw.rect(surf, color, (8, 28, 48, 25))
    # Kaki bergelombang
    pygame.draw.circle(surf, color, (14, 56), 6)
    pygame.draw.circle(surf, color, (32, 56), 6)
    pygame.draw.circle(surf, color, (50, 56), 6)
    # Mata Marah
    pygame.draw.polygon(surf, (255, 255, 0), [(18, 25), (28, 20), (28, 30)]) # Kiri
    pygame.draw.polygon(surf, (255, 255, 0), [(46, 25), (36, 20), (36, 30)]) # Kanan

def create_character_sprite(filename, type_char, color):
    surf = pygame.Surface((64, 64), pygame.SRCALPHA)
    
    if type_char == "bear":
        draw_bear(surf, color)
    elif type_char == "ghost":
        draw_ghost(surf, color)
    elif type_char == "goal":
        # Gambar Bintang/Bendera
        pygame.draw.polygon(surf, color, [(32, 5), (40, 25), (60, 25), (45, 40), (50, 60), (32, 50), (14, 60), (19, 40), (4, 25), (24, 25)])
        pygame.draw.polygon(surf, (255, 255, 200), [(32, 15), (35, 25), (45, 25), (37, 32), (40, 42), (32, 37), (24, 42), (27, 32), (19, 25), (29, 25)])

    pygame.image.save(surf, f"assets/{filename}")
    print(f"Image generated: {filename}")

def create_tile(filename, color, border):
    surf = pygame.Surface((64, 64))
    surf.fill(color)
    pygame.draw.rect(surf, border, (0, 0, 64, 64), 4) # Bingkai tebal
    pygame.draw.rect(surf, (border[0]//2, border[1]//2, border[2]//2), (10, 10, 44, 44), 2) # Detail dalam
    pygame.image.save(surf, f"assets/{filename}")
    print(f"Tile generated: {filename}")

# --- JALANKAN ---
print("Generating Cute Assets...")

# 1. Karakter (Boneka/Hewan)
create_character_sprite("player.png", "bear", (0, 180, 255))   # Beruang Biru
create_character_sprite("enemy.png", "ghost", (255, 60, 60))   # Hantu Merah
create_character_sprite("goal.png", "goal", (255, 215, 0))     # Bintang Emas

# 2. Lantai & Tembok (Style Kartun)
create_tile("wall.png", (60, 40, 40), (40, 20, 20))    # Tembok Coklat Bata
create_tile("floor.png", (20, 20, 30), (40, 40, 60))   # Lantai Gelap

# 3. Suara
create_sound("move.wav", 400, 0.08, 0.3)
create_sound("alert.wav", 600, 0.4, 0.4)
create_sound("win.wav", 1000, 0.8, 0.6)
create_sound("lose.wav", 100, 0.8, 0.6)

print("DONE! Jalankan game_main.py sekarang.")
pygame.quit()