import heapq
import numpy as np

class EnemyFSM:
    def __init__(self):
        self.state = "PATROL"
        self.path = [] # List koordinat langkah
        
    def update(self, enemy_pos, player_pos, maze_grid):
        """
        Input: Posisi Enemy (x,y), Player (x,y), dan Grid Map
        Output: Koordinat langkah selanjutnya (next_x, next_y)
        """
        # Hitung jarak Manhattan (Grid distance)
        dist = abs(enemy_pos[0] - player_pos[0]) + abs(enemy_pos[1] - player_pos[1])
        
        # --- 1. LOGIKA TRANSISI STATE (Automata) ---
        if dist < 8: # Jika pemain dekat (Jarak pandang)
            self.state = "CHASE"
        elif dist > 12 and self.state == "CHASE":
            self.state = "PATROL" # Kehilangan jejak
            self.path = [] # Reset jalur
            
        # --- 2. LOGIKA AKSI (Action) ---
        
        # KASUS A: MENGEJAR (CHASE)
        if self.state == "CHASE":
            # Selalu hitung ulang jalur ke player (karena player bergerak)
            self.path = a_star_search(maze_grid, enemy_pos, player_pos)
            
            if len(self.path) > 1:
                return self.path[1] # Ambil langkah kedua (langkah pertama adalah posisi sendiri)
        
        # KASUS B: PATROLI (PATROL)
        elif self.state == "PATROL":
            # Jika tidak punya tujuan atau sudah sampai tujuan
            if not self.path or len(self.path) < 2:
                # Cari titik random baru yang valid (Lantai)
                h, w = maze_grid.shape
                for _ in range(20): # Coba 20 kali cari titik valid
                    rx = np.random.randint(1, w-1)
                    ry = np.random.randint(1, h-1)
                    if maze_grid[ry, rx] == 1:
                        # Hitung jalur ke titik random tsb
                        self.path = a_star_search(maze_grid, enemy_pos, (rx, ry))
                        if len(self.path) > 1:
                            break
            
            # Eksekusi Jalur
            if self.path and len(self.path) > 1:
                # Cek apakah kita sudah di node pertama path? Hapus kalau ya.
                if self.path[0] == enemy_pos:
                    self.path.pop(0)
                
                # Ambil langkah berikutnya
                if self.path:
                    return self.path[0]

        return enemy_pos # Diam jika bingung

def a_star_search(grid, start, goal):
    """
    Algoritma A* (A-Star) Standar
    """
    w, h = grid.shape[1], grid.shape[0]
    pq = [(0, start)]
    came_from = {start: None}
    cost_so_far = {start: 0}
    
    while pq:
        _, current = heapq.heappop(pq)
        
        if current == goal:
            break
            
        cx, cy = current
        # Cek 4 arah (Atas, Bawah, Kiri, Kanan)
        neighbors = [(cx+1, cy), (cx-1, cy), (cx, cy+1), (cx, cy-1)]
        
        for next_node in neighbors:
            nx, ny = next_node
            # Cek batas & tembok (grid 1 = jalan)
            if 0 <= nx < w and 0 <= ny < h and grid[ny, nx] == 1:
                new_cost = cost_so_far[current] + 1
                if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                    cost_so_far[next_node] = new_cost
                    # Heuristik Manhattan Distance
                    priority = new_cost + (abs(nx - goal[0]) + abs(ny - goal[1]))
                    heapq.heappush(pq, (priority, next_node))
                    came_from[next_node] = current
                    
    # Rekonstruksi Jalur (Backtracking)
    path = []
    curr = goal
    if curr not in came_from: # Jika tujuan tidak terjangkau
        return []
        
    while curr is not None:
        path.append(curr)
        curr = came_from[curr]
    path.reverse()
    return path