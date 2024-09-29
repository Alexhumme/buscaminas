from os import system, get_terminal_size, terminal_size
from random import random

def centerText(txt:str):
    term_w: int = get_terminal_size().columns
    txt_w: int = len(txt)
    return txt.rjust(int(term_w/2)+int(txt_w/2))
# Buscaminas en Terminal

# Clase celda
class Tile:
    def __init__(self, x, y):
        self.mine = random() > 0.8
        self.flag = False
        self.checked = False
        self.meaby = False
        self.number = 0
        self.pos = {"x": x, "y": y}

    def draw(self, playerPos):  # determinar icono apropiado e imprimirlo
        icon = "\033[34m🟦\033[0m"
        if self.meaby: icon = "❓"
        if self.flag: icon = "\033[31m🏳 \033[0m"
        if self.checked:
            if self.mine: icon = "\033[31m\033[43m💣\033[0m"
            else: icon = self.getNumerIcon()
        if self.pos == playerPos: icon = f"[{icon}]"
        else: icon = f" {icon} "
        print(icon, end="")
        return

    def getNumerIcon(self):  # determinar icono por numero
        icon = "⬜"
        if self.number == 1: icon = "\033[36m1️⃣ "
        if self.number == 2: icon = "\033[32m2️⃣ "
        if self.number == 3: icon = "\033[33m3️⃣ "
        if self.number == 4: icon = "\033[31m4️⃣ "
        if self.number == 5: icon = "\033[35m5️⃣ "
        if self.number == 6: icon = "\033[30m\033[33m6️⃣ "
        if self.number == 7: icon = "\033[30m\033[31m7️⃣ "
        if self.number == 8: icon = "\033[30m\033[35m8️⃣ "
        return icon + "\033[0m"

# Clase buscaminas
class buscaminas:
    def __init__(self):
        self.size = 10
        self.playerPos = {"x": 0, "y": 0}
        self.gameover = False
        self.success = False
        self.gameMap: list = []

    def move_player(self, direction):
        directions = {"s": (0, 1), "w": (0, -1), "d": (1, 0), "a": (-1, 0)}
        if direction in directions:
            dx, dy = directions[direction]
            new_x, new_y = self.playerPos["x"] + dx, self.playerPos["y"] + dy
            if self.is_valid_position(new_x, new_y):
                self.playerPos["x"], self.playerPos["y"] = new_x, new_y

    def choose_difficulty(self):
        term_w: int = get_terminal_size().columns
        
        print(centerText("---------------"))
        print(centerText("| BUSCAMINAS  |"))
        print(centerText("-------------------"))
        print(centerText("|  Nueva partida  |"))
        print(centerText("-------------------"))
        print(centerText("| 1 | Facil       |"))
        print(centerText("| 2 | Medio       |"))
        print(centerText("| 3 | Dificil     |"))
        print(centerText("-------------------"))
        
        difficulty: str = input()
        if difficulty == '1': self.size = 5
        elif difficulty == '2': self.size = 10
        elif difficulty == '3': self.size = 16
        return

    def play(self):
        self.clean()
        self.choose_difficulty()
        self.playerPos = {"x": 0, "y": 0}
        self.gameover = False
        self.success = False
        self.gameMap = self.generate_map()
        while not self.gameover:
            key = ""
            self.clean()
            current = self.gameMap[self.playerPos["y"]][self.playerPos["x"]]
            
            self.draw_header() 
            
            self.draw_map()
            
            print("\n")
            print(centerText("-------------------             -------------"))
            print(centerText("| s/w/a/d | mover |             | e | salir |"))
            print(centerText("-------------------             -------------"))
            print(centerText("-----------------      -----------------------      ----------------------"))
            print(centerText("| z | descrubir |      | x | poner/quitar 🏳 |      | c | poner/quitar ❓|"))
            print(centerText("-----------------      -----------------------      ----------------------"))
            
            key = input("\n>")
            if key == "e": self.gameover = True
            elif key in ["s", "w", "d", "a"]: self.move_player(key)
            elif key == "z": self.check(current)
            elif key == "x": current.flag = not current.flag
            elif key == "c": current.meaby = not current.meaby

            self.success = self.check_success()
            if (current.checked and current.mine) or self.success:
                self.gameover = True

        self.handle_gameover()
    # actualizar celdas
    def clean(self): 
        system("clear")
        print("\n\n\n\n\n\n\n\n\n")

    def draw_header(self):
        print(centerText( " ----------------------------"))
        print(centerText(f"| BUSCAMINAS | 💣 {self.count_mines()} | 🏳  {self.count_flags()} |"))
        print(centerText( " ----------------------------"))

    # generar mapa
    def is_valid_position(self, x, y):
        return 0 <= x < self.size and 0 <= y < self.size
    
    def generate_map(self):
        sx = sy = self.size
        gameMap = [[Tile(x, y) for x in range(sx)] for y in range(sy)]
        for y in range(sy):
            for x in range(sx):
                if gameMap[y][x].mine:
                    for dx in range(-1, 2):
                        for dy in range(-1, 2):
                            if dx == dy == 0:
                                continue
                            new_x, new_y = x + dx, y + dy
                            if self.is_valid_position(new_x, new_y):
                                gameMap[new_y][new_x].number += 1

        return gameMap
    # Dibujar Mapa
    def draw_map(self):
        for x in range(self.size):
            print("")
            for i in range(int(get_terminal_size().columns/2) - int(self.size * 2)): 
                print(" ", end="") 
            for y in range(self.size):
                self.gameMap[x][y].draw(self.playerPos)

    def check(self, tile: Tile):
        if tile.checked:
            return

        tile.checked = True
        tile.flag = False

        if tile.number > 0:
            return

        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx == dy == 0:
                    continue
                new_x, new_y = tile.pos["x"] + dx, tile.pos["y"] + dy
                if self.is_valid_position(new_x, new_y):
                    self.check(self.gameMap[new_y][new_x])
    # game over
    def check_success(self):
        for row in self.gameMap:
            for tile in row:
                if tile.mine:
                    if not tile.flag:
                        return False
                else:
                    if not tile.checked:
                        return False
        return True

    def handle_gameover(self):
        if self.success: print(centerText("Ganaste! ☺ "))
        else:
            for row in self.gameMap:
                for tile in row:
                    if tile.mine:
                        tile.checked = True
            self.clean()
            self.draw_header()
            self.draw_map()
            print("\n")
            print(centerText("Perdiste...  😞"))

        print(centerText("------------------------"))
        print(centerText("| jugar de nuevo ? (r) |"))
        print(centerText("------------------------"))
        
        repeat = input("> ")
        if repeat == "r": self.play()
        return
    # contar 
    def count_mines(self):
        mines_q = 0
        for row in self.gameMap:
            for tile in row:
                if tile.mine:
                    mines_q += 1
        return mines_q
    def count_flags(self):
        flags_q = 0
        for row in self.gameMap:
            for tile in row:
                if tile.flag:
                    flags_q += 1
        return flags_q

game = buscaminas()

game.play()
