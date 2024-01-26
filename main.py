from os import system
from random import random

# Buscaminas en Terminal
sx = 20
sy = 20
playerPos = {"x": 0, "y": 0}


# celda
class Tile:
    def __init__(self, x, y):
        self.mine = random() > 0.8
        self.flag = False
        self.checked = False
        self.number = 0
        self.pos = {"x": x, "y": y}

    def draw(self):  # determinar icono apropiado e imprimirlo
        icon = "🟦"
        if self.flag:
            icon = "🚩"
        if self.checked:
            if self.mine:
                icon = "💣"
            else:
                icon = self.getNumerIcon()
        if self.pos == playerPos:
            icon = f"[{icon}]"
        else:
            icon = f" {icon} "
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


# generar mapa
def is_valid_position(x, y):
    return 0 <= x < sx and 0 <= y < sy

def generate_map(sx, sy):
    gameMap = [[Tile(x, y) for x in range(sx)] for y in range(sy)]

    for y in range(sy):
        for x in range(sx):
            if gameMap[y][x].mine:
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        if dx == dy == 0:
                            continue
                        new_x, new_y = x + dx, y + dy
                        if is_valid_position(new_x, new_y):
                            gameMap[new_y][new_x].number += 1

    return gameMap


# Dibujar Mapa
def draw_map(gameMap: list):
    for x in range(sx):
        print("")
        for y in range(sy):
            gameMap[x][y].draw()


# actualizar celdas
def update(): system("cls")
    
def check(tile: Tile, gameMap):
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
            if is_valid_position(new_x, new_y):
                check(gameMap[new_y][new_x], gameMap)


# game over
def check_success(gameMap):
    for row in gameMap:
        for tile in row:
            if tile.mine:
                if not tile.flag:
                    return False
            else:
                if not tile.checked:
                    return False
    return True


def handle_gameover(success, gameMap):
    if success:
        print("Ganaste! 🥳🎉")
    else:
        for row in gameMap:
            for tile in row:
                if tile.mine:
                    tile.checked = True
        update()
        draw_map(gameMap)
        print("\nPerdiste... 💀")

    repeat = input("Otra Vez ? (s): ")
    if repeat == "s":
        buscaminas()
    return


# contar 
def count_mines(gameMap):
    mines_q = 0
    for row in gameMap:
        for tile in row:
            if tile.mine:
                mines_q += 1
    return mines_q
def count_flags(gameMap):
    flags_q = 0
    for row in gameMap:
        for tile in row:
            if tile.flag:
                flags_q += 1
    return flags_q


# bucle principal
def buscaminas():
    gameover = False
    success = False
    gameMap = generate_map(sx, sy)
    mines_q = count_mines(gameMap)
    while not gameover:
        flags_q = count_flags(gameMap)
        key = ""
        update()
        current = gameMap[playerPos["y"]][playerPos["x"]]
        print(f"--- Buscaminas 💣 ---");
        print(f"💣 : {mines_q}");
        print(f"🚩 : {flags_q}");
        draw_map(gameMap)
        key = input("\nAccion : ")
        if key == "e": gameover = True
        if key == "s": playerPos["y"] += 1
        if key == "w": playerPos["y"] -= 1
        if key == "d": playerPos["x"] += 1
        if key == "a": playerPos["x"] -= 1
        if key == "z": check(current, gameMap)
        if key == "x": current.flag = not current.flag

        success = check_success(gameMap)
        if (current.checked and current.mine) or success:
            gameover = True

    handle_gameover(success, gameMap)

buscaminas()
