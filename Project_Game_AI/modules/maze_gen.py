import numpy as np
import random

def generate_maze_prim(width, height):
    """
    Membuat Labirin menggunakan Algoritma Prim (MST).
    0 = Tembok, 1 = Jalan
    """
    # Pastikan ukuran ganjil agar tembok rapi
    shape = (height, width)
    maze = np.zeros(shape, dtype=int)
    
    # Titik awal
    start_x, start_y = 1, 1
    maze[start_y, start_x] = 1
    
    # Daftar tembok kandidat (Frontier)
    walls = []
    walls.append((start_x, start_y, start_x + 2, start_y))
    walls.append((start_x, start_y, start_x - 2, start_y))
    walls.append((start_x, start_y, start_x, start_y + 2))
    walls.append((start_x, start_y, start_x, start_y - 2))
    
    while walls:
        # Pilih tembok acak
        rand_idx = random.randint(0, len(walls) - 1)
        x_src, y_src, x_dst, y_dst = walls[rand_idx]
        walls.pop(rand_idx)
        
        # Cek apakah tujuan masih tembok & dalam batas
        if 0 < x_dst < width - 1 and 0 < y_dst < height - 1:
            if maze[y_dst, x_dst] == 0:
                # Jebol tembok (Buat Edge baru di Graph)
                maze[y_dst, x_dst] = 1
                # Jebol tembok antaranya
                maze[y_src + (y_dst - y_src) // 2, x_src + (x_dst - x_src) // 2] = 1
                
                # Tambahkan tembok tetangga baru ke daftar
                neighbors = [
                    (x_dst, y_dst, x_dst + 2, y_dst),
                    (x_dst, y_dst, x_dst - 2, y_dst),
                    (x_dst, y_dst, x_dst, y_dst + 2),
                    (x_dst, y_dst, x_dst, y_dst - 2)
                ]
                walls.extend(neighbors)
                
    return maze