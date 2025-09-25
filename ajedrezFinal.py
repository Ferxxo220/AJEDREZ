
tablero1 = [
    ["🏤", "🐴", "🎩", "👩", "👑", "🎩", "🐴", "🏤"],  
    ["⚫", "⚫", "⚫", "⚫", "⚫", "⚫", "⚫", "⚫"],                                          
    ["⬜","⬛","⬜","⬛","⬜","⬛","⬜","⬛"],           
    ["⬛","⬜","⬛","⬜","⬛","⬜","⬛","⬜"],
    ["⬜","⬛","⬜","⬛","⬜","⬛","⬜","⬛"],
    ["⬛","⬜","⬛","⬜","⬛","⬜","⬛","⬜"],
    ["⚪", "⚪", "⚪", "⚪", "⚪", "⚪", "⚪", "⚪"],  
    ["🏰", "🎠", "⛪", "👸", "🤴", "⛪", "🎠", "🏰"]   
]


blancas = ["🏰","🎠","⛪","👸","🤴","⚪"]
negras  = ["🏤","🐴","🎩","👩","👑","⚫"]

columnas = ["a","b","c","d","e","f","g","h"]
game = True
Negritas = False  # False = turno blancas, True = turno negras


def ImprimirTablero(tablero):
    for i in range(8):
        print(8-i, end=" ")  
        for j in range(8):
            print(tablero[i][j], end=" ")
        print()
    print("  " + "  ".join(columnas))


def pedir_movimiento():
    origen = input("Ingresa la casilla de origen (ej: e2): ")
    destino = input("Ingresa la casilla de destino (ej: e4): ")
    return origen, destino


def ajedrez_a_matriz(pos):
    columna = pos[0].lower()  # 'a' a 'h'
    fila = int(pos[1])        # '1' a '8'
    if columna < 'a' or columna > 'h' or fila < 1 or fila > 8:
        raise ValueError("Coordenada inválida")
    fila_matriz = 8 - fila
    columna_matriz = ord(columna) - ord('a')
    return fila_matriz, columna_matriz


def camino_libre(tablero, x1, y1, x2, y2):
    
    dx = (x2 - x1) // max(1, abs(x2 - x1)) if x2 != x1 else 0
    dy = (y2 - y1) // max(1, abs(y2 - y1)) if y2 != y1 else 0

    x, y = x1 + dx, y1 + dy
    while (x, y) != (x2, y2):
        if tablero[x][y] not in ["⬜","⬛"]:  
            return False
        x += dx
        y += dy
    return True


def es_movimiento_valido(tablero, pieza, x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    destino = tablero[x2][y2]

    if dx == 0 and dy == 0:
        return False

    
    if pieza in blancas and destino in blancas:
        return False
    if pieza in negras and destino in negras:
        return False

    
    if pieza == "⚪":  
        if x1 == 6 and dx == -2 and dy == 0 and tablero[x2][y2] in ["⬜","⬛"]:
            return True
        if dx == -1 and dy == 0 and tablero[x2][y2] in ["⬜","⬛"]:
            return True
        if dx == -1 and abs(dy) == 1 and tablero[x2][y2] in negras:
            return True
        return False

    if pieza == "⚫":  
        if x1 == 1 and dx == 2 and dy == 0 and tablero[x2][y2] in ["⬜","⬛"]:
            return True
        if dx == 1 and dy == 0 and tablero[x2][y2] in ["⬜","⬛"]:
            return True
        if dx == 1 and abs(dy) == 1 and tablero[x2][y2] in blancas:
            return True
        return False

    # Torres (🏰, 🏤)
    if pieza in ["🏰","🏤"]:
        if dx == 0 or dy == 0:
            return camino_libre(tablero, x1, y1, x2, y2)
        return False

    # Caballos (🎠, 🐴)
    if pieza in ["🎠","🐴"]:
        return (abs(dx), abs(dy)) in [(2,1), (1,2)]

    # Alfiles (⛪, 🎩)
    if pieza in ["⛪","🎩"]:
        if abs(dx) == abs(dy):
            return camino_libre(tablero, x1, y1, x2, y2)
        return False

    # Reina (👸, 👩)
    if pieza in ["👸","👩"]:
        if dx == 0 or dy == 0 or abs(dx) == abs(dy):
            return camino_libre(tablero, x1, y1, x2, y2)
        return False

    # Rey (🤴, 👑)
    if pieza in ["🤴","👑"]:
        return abs(dx) <= 1 and abs(dy) <= 1

    return False


def tirar(jugador, tablero, origen, destino):
    
   
    try:
        x1, y1 = ajedrez_a_matriz(origen)
        x2, y2 = ajedrez_a_matriz(destino)
    except ValueError:
        print("Coordenadas inválidas ")
        return False

    pieza = tablero[x1][y1]

    
    if pieza in ["⬜", "⬛"]:
        print("No hay pieza en la casilla de origen ")
        return False

    
    if jugador == "blancas" and pieza not in blancas:
        print("Esa no es tu pieza  (blancas)")
        return False
    if jugador == "negras" and pieza not in negras:
        print("Esa no es tu pieza  (negras)")
        return False

    
    if not es_movimiento_valido(tablero, pieza, x1, y1, x2, y2):
        print("Movimiento inválido para esa pieza ")
        return False

    
    if tablero[x2][y2] in ["🤴","👑"]:
        print("¡¡JAQUE")
        global game
        game = False

   
    tablero[x2][y2] = pieza

    
    if (x1 + y1) % 2 == 0:
        tablero[x1][y1] = "⬜"
    else:
        tablero[x1][y1] = "⬛"

    return True



while game:
    if Negritas:  
        print("----- Turno de las negras -----")
        ImprimirTablero(tablero1)
        origen, destino = pedir_movimiento()
        if tirar("negras", tablero1, origen, destino):
            Negritas = False  
    else:  
        print("----- Turno de las blancas -----")
        ImprimirTablero(tablero1)
        origen, destino = pedir_movimiento()
        if tirar("blancas", tablero1, origen, destino):
            Negritas = True  
