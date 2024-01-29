from os import system
from random import random

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
        icon = "🟦"
        if self.meaby: icon = "❓"
        if self.flag: icon = "🚩"
        if self.checked:
            if self.mine: icon = "💣"
            else: icon = self.getNumerIcon()
        if self.pos == playerPos: icon = f"[{icon}]"
        else: icon = f" {icon} "
        print(icon, end="")
        return

    def getNumerIcon(self):  # determinar icono por numero
        icon = "⬜"
        if self.number == 1: icon = "1️⃣ "
        if self.number == 2: icon = "2️⃣ "
        if self.number == 3: icon = "3️⃣ "
        if self.number == 4: icon = "4️⃣ "
        if self.number == 5: icon = "5️⃣ "
        if self.number == 6: icon = "6️⃣ "
        if self.number == 7: icon = "7️⃣ "
        if self.number == 8: icon = "8️⃣ "
        return icon

# Clase buscaminas
class buscaminas:
    def __init__(self, x = 10, y = 10):
        self.size = {'x':x,'y':y}
        self.playerPos = {"x": 0, "y": 0}
        self.gameover = False
        self.success = False
        self.gameMap = None

    def move_player(self, direction):
        directions = {"s": (0, 1), "w": (0, -1), "d": (1, 0), "a": (-1, 0)}
        if direction in directions:
            dx, dy = directions[direction]
            new_x, new_y = self.playerPos["x"] + dx, self.playerPos["y"] + dy
            if self.is_valid_position(new_x, new_y):
                self.playerPos["x"], self.playerPos["y"] = new_x, new_y

    def play(self):
        self.gameover = False
        self.success = False
        self.gameMap = self.generate_map()
        mines_q = self.count_mines()
        while not self.gameover:
            flags_q = self.count_flags()
            key = ""
            self.clean()
            current = self.gameMap[self.playerPos["y"]][self.playerPos["x"]]
            print(f"--- Buscaminas 💣 ---");
            print(f"💣 : {mines_q}");
            print(f"🚩 : {flags_q}");
            self.draw_map()
            key = input("\nAccion (e: salir, s/w/d/a: mover, z: descubrir, x: poner/quitar bandera, c: poner/quitar interrogante): ")
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
    def clean(self): system("cls")
    # generar mapa
    def is_valid_position(self, x, y):
        return 0 <= x < self.size["x"] and 0 <= y < self.size["y"]
    
    def generate_map(self):
        sx = self.size['x']
        sy = self.size['y']
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
        for x in range(self.size['x']):
            print("")
            for y in range(self.size['y']):
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
        if self.success: print("Ganaste! 🥳🎉")
        else:
            for row in self.gameMap:
                for tile in row:
                    if tile.mine:
                        tile.checked = True
            self.clean()
            self.draw_map()
            print("\nPerdiste... 💀")

        repeat = input("Otra Vez ? (s): ")
        if repeat == "s": self.play()
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

game = buscaminas(3,3)

game.play()