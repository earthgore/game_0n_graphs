import random
from copy import copy
import pygame as pg
from Games import Game_xxx
from Games import GameCircle
from math import sin, cos, pi
import pygame_menu
pg.init()
Difficulty = 5

class Button:
    def __init__(self, surface = None, color = None, x = 0, y = 0, length = 0, height = 0, width = None, text = None, text_color = None):
        if surface is not None:
            surface = self.draw_button(surface, color, length, height, x, y, width)
            self.write_text(surface, text, text_color, length, height, x, y)
        self.rect = pg.Rect(x,y, length, height)

    def write_text(self, surface, text, text_color, length, height, x, y):
        myFont = pg.font.SysFont("Calibri", 20)
        myText = myFont.render(text, True, text_color)
        surface.blit(myText, ((x+length/2) - myText.get_width()/2, (y+height/2) - myText.get_height()/2))
        return surface

    def draw_button(self, surface, color, length, height, x, y, width):
        for i in range(1,10):
            s = pg.Surface((length+(i*2),height+(i*2)))
            s.fill(color)
            alpha = (255/(i+2))
            if alpha <= 0:
                alpha = 1
            s.set_alpha(alpha)
            pg.draw.rect(s, color, (x-i,y-i,length+i,height+i), width)
            surface.blit(s, (x-i,y-i))
        pg.draw.rect(surface, color, (x,y,length,height), 0)
        pg.draw.rect(surface, (190,190,190), (x,y,length,height), 1)
        return surface

    def pressed(self, mouse):
        if mouse[0] > self.rect.topleft[0]:
            if mouse[1] > self.rect.topleft[1]:
                if mouse[0] < self.rect.bottomright[0]:
                    if mouse[1] < self.rect.bottomright[1]:
                        return True
                    else: return False
                else: return False
            else: return False
        else: return False


def make_game_xxx(game):
    if not game.check_lose():
        for i in range(len(game)):
            if game.can_do_move(i):
                new_field = copy(game.field)
                new_field[i] = "X"
                game.create_child(new_field)
                game.children[-1].id = str(game.id) + "_" + str(i)
                make_game_xxx(game.children[-1])
    else:
        root = game.get_root()
        root.terms.append(game)


def make_game_circle(game):
    if not game.check_lose():
        for i in range(len(game)):
            for j in range(len(game)):
                if game.can_do_move(i, j) and i != j:
                    new_edges = copy(game.edges)
                    new_edges.append([i, j])
                    game.create_child(new_edges)
                    game.children[-1].id = str(game.id) + "_" + str(i)
                    make_game_circle(game.children[-1])
    else:
        root = game.get_root()
        root.terms.append(game)


def bfs_lvl(root):
    Q = []
    Qstart = 0
    List = []
    Q.append(root)
    while(Qstart < len(Q)):
        v = Q[Qstart]
        Qstart += 1
        for i in range(len(v.children)):
            if v.children[i] not in List:
                v.children[i].pos[1] = v.pos[1] + 80
                Q.append(v.children[i])
                List.append(v.children[i])
                if Q[-2].pos[1] == v.pos[1] + 80:
                    v.children[i].pos[0] = Q[-2].pos[0] + 50


def vertex_marking(root, list_of_edges, vertexes):
    new_matrix = create_matrix(list_of_edges, vertexes)
    for w_vertex in root.terms:
        w_vertex.mark = "P"

    while new_matrix:
        for vertex1 in new_matrix.keys():
            flag = True
            for vertex2 in new_matrix[vertex1].values():
                if vertex2 != 0:
                    flag = False
            if flag:
                w_vertex = vertex1
                break
        if w_vertex.mark != "N":
            w_vertex.mark = "P"
        for vertex1 in new_matrix.keys():
            if new_matrix[vertex1][w_vertex] == 1 and w_vertex.mark == "P":
                vertex1.mark = "N"
        new_matrix.pop(w_vertex)
        for vertex1 in new_matrix.keys():
            new_matrix[vertex1].pop(w_vertex)


def create_matrix(list_of_edges, vertexes):
    matrix = dict()
    for vertex1 in vertexes:
        vtxs = dict()
        for vertex2 in vertexes:
            vtxs[vertex2] = 0
        matrix[vertex1] = vtxs

    for edge in list_of_edges:
        vertex1 = edge[0]
        vertex2 = edge[1]
        if vertex1 in matrix.keys() and vertex2 in matrix[vertex1].keys():
            matrix[vertex1][vertex2] = 1

    return matrix


def set_difficulty(value = "5"):
    global Difficulty
    Difficulty = int(value)


def win_check_xxx(field):
    for i in range(len(field)):
        if field[i - 1] == "X" and field[i] == "X" and field[(i + 1) % len(field)] == "X":
            return True
    return False


def edge_com(edges1, edges2):
    if edges1 == [] or edges2 == []:
        return False
    elif len(edges1) != len(edges2):
        return False
    for i in range(len(edges1)):
        if (edges1[i][0] != edges2[i][0] or edges1[i][1] != edges2[i][1]) and (edges1[i][1] != edges2[i][0] or edges1[i][0] != edges2[i][1]):
            return False
    return True


def vertex_merge_circle(vertexes : set):
    vertexes = list(vertexes)
    for v1 in vertexes:
        for v2 in vertexes:
            if v1 != v2 and edge_com(v1.edges, v2.edges):
                v1.parents.extend(v2.parents)
                for v3 in v2.parents:
                    v3.children.append(v1)
                    v3.children.remove(v2)
                vertexes.remove(v2)
    return vertexes


def vertex_merge_xxx(vertexes : set):
    vertexes = list(vertexes)
    for v1 in vertexes:
        for v2 in vertexes:
            if v1 != v2 and v1.field == v2.field:
                v1.parents.extend(v2.parents)
                for v3 in v2.parents:
                    v3.children.append(v1)
                    v3.children.remove(v2)
                vertexes.remove(v2)
    return vertexes


def get_vertexes(root):
    vertexes = set()

    def create_vertex(root):
        nonlocal vertexes
        """flag = True
        v1 = root
        for v2 in vertexes:
            if v1.field == v2.field:
                v2.parents.extend(v1.parents)
                flag = False
                for v3 in v1.parents:
                    v3.children.append(v2)
                    v3.children.remove(v1)
                break
        if flag:"""
        vertexes.add(root)
        if root.children:
            for i in range(len(root.children)):
                create_vertex(root.children[i])

    create_vertex(root)
    if type(root) is GameCircle:
        return vertex_merge_circle(vertexes)
    else:
        return vertex_merge_xxx(vertexes)


def get_edges(root):
    list_of_edges = []

    def create_edges(root):
        nonlocal list_of_edges
        if root.children:
            for i in range(len(root.children)):
                list_of_edges.append([root, root.children[i]])
                create_edges(root.children[i])

    create_edges(root)
    return list_of_edges


def bot_decision(root : Game_xxx):
    if root.mark == "N":
        for i in range(len(root.children)):
            if root.children[i].mark == "P":
                return root.children[i], True
    else:
        if root.children:
            return root.children[random.randint(0, len(root.children) - 1)], True
        else:
            return root, False


def start_game_xxx():
    global Difficulty
    sizeblock = 100
    margine = 15
    a = Difficulty
    WIDTH = max(sizeblock * a + margine * (a + 1), 1200)
    HEIGTH = 600
    sc = pg.display.set_mode((WIDTH, HEIGTH))
    pg.display.set_caption('Крестики без ноликов!')

    clock = pg.time.Clock()

    FPS = 30

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    sc.fill(BLACK)
    font = pg.font.SysFont('Calibri', 45)
    text1 = font.render("Loading", True, WHITE, 5)
    text_rect = text1.get_rect()
    text_x = sc.get_width() / 2 - text_rect.width / 2
    text_y = (1 / 2) * sc.get_height() - text_rect.height / 2
    sc.blit(text1, [text_x, text_y])
    pg.display.update()
    game_xxx = Game_xxx(["_" for i in range(a)])
    make_game_xxx(game_xxx)
    vertexes = get_vertexes(game_xxx)
    list_of_edges = get_edges(game_xxx)
    vertex_marking(vertexes=vertexes, list_of_edges=list_of_edges, root=game_xxx)
    sc.fill(BLACK)
    for col in range(a):
        x = col * sizeblock + (col + 1) * margine
        y = 0 * sizeblock + 1 * margine
        pg.draw.rect(sc, WHITE, (x, y, sizeblock, sizeblock))
    query = 0
    field = copy(game_xxx.field)
    game_over = False
    btn = Button(sc, WHITE, 10, 150, 150, 40, 40, "Перезапуск", BLACK)
    btn_grph = Button(sc, WHITE, 210, 150, 150, 40, 40, "Вывод графа", BLACK)
    while True:
        game_over = game_over if game_over else win_check_xxx(field)
        if game_over:
            font = pg.font.SysFont('Calibri', 45)
            if query == 0:
                text1 = font.render("You win", True, WHITE, 5)
            else:
                text1 = font.render("You lose", True, WHITE, 5)
            text_rect = text1.get_rect()
            text_x = sc.get_width() / 2 - text_rect.width / 2
            text_y = (3 / 4) * sc.get_height() - text_rect.height / 2
            sc.blit(text1, [text_x, text_y])

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                x_mouse, y_mouse = pg.mouse.get_pos()
                if y_mouse <= sizeblock + 2*margine and not game_over:
                    col = x_mouse // (sizeblock + margine)
                    if field[col] == "_":
                        query = 0
                        field[col] = "X"
                        for i in range(len(game_xxx.children)):
                            if game_xxx.children[i].field == field:
                                game_xxx = game_xxx.children[i]
                                break
                        for col in range(a):
                            if field[col] == "X":
                                x = col * sizeblock + (col + 1) * margine
                                y = 0 * sizeblock + 1 * margine
                                pg.draw.line(sc, BLACK, (x + 10, y + 10), (x + sizeblock - 10, y + sizeblock - 10), 5)
                                pg.draw.line(sc, BLACK, (x + sizeblock - 10, y + 10), (x + 10, y + sizeblock - 10), 5)

                        game_xxx, flag = bot_decision(game_xxx)

                        if flag:
                            field = copy(game_xxx.field)
                            query = 1
                        else:
                            game_over = True
                elif btn.pressed(pg.mouse.get_pos()):
                    game_over = False
                    game_xxx = game_xxx.get_root()
                    field = copy(game_xxx.field)
                    sc.fill(BLACK)
                    for col in range(a):
                        x = col * sizeblock + (col + 1) * margine
                        y = 0 * sizeblock + 1 * margine
                        pg.draw.rect(sc, WHITE, (x, y, sizeblock, sizeblock))
                    btn.draw_button(sc, WHITE, 150, 40, 10, 150, 40)
                    btn.write_text(sc, "Перезапуск", BLACK, 150, 40, 10, 150)
                    btn_grph.draw_button(sc, WHITE, 150, 40, 210, 150, 40)
                    btn_grph.write_text(sc, "Вывод графа", BLACK, 150, 40, 210, 150)
                elif btn_grph.pressed(pg.mouse.get_pos()):
                    print_graph(vertexes, list_of_edges, game_xxx.get_root(), game_xxx)
                    sc.fill(BLACK)
                    for col in range(a):
                        x = col * sizeblock + (col + 1) * margine
                        y = 0 * sizeblock + 1 * margine
                        pg.draw.rect(sc, WHITE, (x, y, sizeblock, sizeblock))
                    btn.draw_button(sc, WHITE, 150, 40, 10, 150, 40)
                    btn.write_text(sc, "Перезапуск", BLACK, 150, 40, 10, 150)
                    btn_grph.draw_button(sc, WHITE, 150, 40, 210, 150, 40)
                    btn_grph.write_text(sc, "Вывод графа", BLACK, 150, 40, 210, 150)
        for col in range(a):
            if field[col] == "X":
                x = col * sizeblock + (col + 1) * margine
                y = 0 * sizeblock + 1 * margine
                pg.draw.line(sc, BLACK, (x + 10, y + 10), (x + sizeblock - 10, y + sizeblock - 10), 5)
                pg.draw.line(sc, BLACK, (x + sizeblock - 10, y + 10), (x + 10, y + sizeblock - 10), 5)



        pg.display.update()
        clock.tick(FPS)


def start_game_circle():
    global Difficulty
    a = Difficulty
    WIDTH = 1200
    HEIGTH = 600
    sc = pg.display.set_mode((WIDTH, HEIGTH))
    pg.display.set_caption('Крeub!')

    clock = pg.time.Clock()

    FPS = 30

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)

    sc.fill(BLACK)
    font = pg.font.SysFont('Calibri', 45)
    text1 = font.render("Loading", True, WHITE, 5)
    text_rect = text1.get_rect()
    text_x = sc.get_width() / 2 - text_rect.width / 2
    text_y = (1 / 2) * sc.get_height() - text_rect.height / 2
    sc.blit(text1, [text_x, text_y])
    pg.display.update()

    game_circle = GameCircle([], a)
    make_game_circle(game_circle)
    vertexes = get_vertexes(game_circle)
    list_of_edges = get_edges(game_circle)
    vertex_marking(vertexes=vertexes, list_of_edges=list_of_edges, root=game_circle)

    sc.fill(BLACK)
    center = (500, 400)
    r = 100
    pg.draw.circle(sc, WHITE, center, r + 2)
    pg.draw.circle(sc, BLACK, center, r)

    dots = []
    angle = 0
    while angle < 2 * pi:
        dots.append((int(-sin(angle) * r + center[0]), int(cos(angle) * r + center[1])))
        angle += 2 * pi / a
    dot_btns = []
    for dot in dots:
        pg.draw.circle(sc, RED, dot, 4)
        dot_btns.append(Button(x=dot[0] - 4, y=dot[1] - 4, length=2*4, height=2*4))

    query = 0
    field = copy(game_circle.nodes)
    edges = []
    game_over = False
    btn = Button(sc, WHITE, 10, 150, 150, 40, 40, "Перезапуск", BLACK)
    btn_grph = Button(sc, WHITE, 210, 150, 150, 40, 40, "Вывод графа", BLACK)
    move = []
    while True:
        game_over = game_over if game_over else game_circle.check_lose()
        if game_over:
            font = pg.font.SysFont('Calibri', 45)
            if query == 0:
                text1 = font.render("You win", True, WHITE, 5)
            else:
                text1 = font.render("You lose", True, WHITE, 5)
            text_rect = text1.get_rect()
            text_x = sc.get_width() / 2 - text_rect.width / 2 + 100
            text_y = (3 / 4) * sc.get_height() - text_rect.height / 2
            sc.blit(text1, [text_x, text_y])

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                x_mouse, y_mouse = pg.mouse.get_pos()
                for col in range(len(dot_btns)):
                    if dot_btns[col].pressed((x_mouse, y_mouse)) and not game_over:
                        if field[col]:
                            move.append(col)
                            query = 0
                            if len(move) == 2:
                                if game_circle.can_do_move(move[0], move[1]):
                                    field[move[0]] = False
                                    field[move[1]] = False
                                    edges.append(move)
                                    for i in range(len(game_circle.children)):
                                        if game_circle.children[i].nodes == field:
                                            game_circle = game_circle.children[i]
                                            break
                                    pg.draw.line(sc, WHITE, dots[move[0]], dots[move[1]])
                                    pg.draw.circle(sc, RED, dots[move[0]], 4)
                                    pg.draw.circle(sc, RED, dots[move[1]], 4)
                                    move.clear()
                                    game_circle, flag = bot_decision(game_circle)
                                    if flag:
                                        for i in range(len(field)):
                                            if field[i] != game_circle.nodes[i]:
                                                move.append(i)

                                        pg.draw.line(sc, WHITE, dots[move[0]], dots[move[1]])
                                        pg.draw.circle(sc, RED, dots[move[0]], 4)
                                        pg.draw.circle(sc, RED, dots[move[1]], 4)
                                        move.clear()
                                        field = copy(game_circle.nodes)
                                        edges = game_circle.edges[::]
                                        query = 1
                                    else:
                                        game_over = True
                                else:
                                    pg.draw.circle(sc, RED, dots[move[0]], 4)
                                    pg.draw.circle(sc, RED, dots[move[1]], 4)
                                    move.clear()
                            pg.draw.circle(sc, GREEN, dots[col], 4)
                if btn.pressed((x_mouse, y_mouse)):
                    game_over = False
                    game_circle = game_circle.get_root()
                    field = copy(game_circle.nodes)
                    edges.clear()
                    sc.fill(BLACK)
                    pg.draw.circle(sc, WHITE, center, r + 2)
                    pg.draw.circle(sc, BLACK, center, r)
                    for dot in dots:
                        pg.draw.circle(sc, RED, dot, 4)
                    btn.draw_button(sc, WHITE, 150, 40, 10, 150, 40)
                    btn.write_text(sc, "Перезапуск", BLACK, 150, 40, 10, 150)
                    btn_grph.draw_button(sc, WHITE, 150, 40, 210, 150, 40)
                    btn_grph.write_text(sc, "Вывод графа", BLACK, 150, 40, 210, 150)
                elif btn_grph.pressed((x_mouse, y_mouse)):
                    print_graph(vertexes, list_of_edges, game_circle.get_root(), game_circle)
                    sc.fill(BLACK)
                    pg.draw.circle(sc, WHITE, center, r + 2)
                    pg.draw.circle(sc, BLACK, center, r)
                    for dot in dots:
                        pg.draw.circle(sc, RED, dot, 4)
                    for edge in game_circle.edges:
                        pg.draw.line(sc, WHITE, dots[edge[0]], dots[edge[1]])
                        pg.draw.circle(sc, RED, dots[edge[0]], 4)
                        pg.draw.circle(sc, RED, dots[edge[1]], 4)
                    btn.draw_button(sc, WHITE, 150, 40, 10, 150, 40)
                    btn.write_text(sc, "Перезапуск", BLACK, 150, 40, 10, 150)
                    btn_grph.draw_button(sc, WHITE, 150, 40, 210, 150, 40)
                    btn_grph.write_text(sc, "Вывод графа", BLACK, 150, 40, 210, 150)

        pg.display.update()
        clock.tick(FPS)


def print_graph(vertexes, list_of_edges, game, position):
    WIDTH = 1200
    HEIGTH = 600
    sc = pg.display.set_mode((WIDTH, HEIGTH))
    pg.display.set_caption('Вывод графа')
    clock = pg.time.Clock()
    FPS = 30
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (225, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    sc.fill(WHITE)
    game.pos = [100, 100]
    bfs_lvl(game)
    for edge in list_of_edges:
        if edge[0] in vertexes and edge[1] in vertexes:
            pg.draw.line(sc, BLACK, edge[0].pos, edge[1].pos)

    buttons = dict()
    r = 20
    for v in vertexes:
        if v == position:
            color = BLUE
        elif v.mark == "N":
            color = GREEN
        else:
            color = RED
        pg.draw.circle(sc, color, v.pos, radius=r)
        buttons[v] = Button(x=(v.pos[0] - r), y=(v.pos[1] - r), length=2*r, height=2*r)

    btn = Button(sc, WHITE, (3 / 4) * sc.get_width(), 150, 150, 40, 40, "Вернуться к игре", BLACK)
    pg.display.update()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            elif event.type == pg.MOUSEBUTTONDOWN and btn.pressed(pg.mouse.get_pos()):
                return 0
        flag = True
        for v in vertexes:
            if buttons[v].pressed(pg.mouse.get_pos()):
                flag = False
                font = pg.font.SysFont('Calibri', 30)
                text1 = font.render(str(v), True, BLACK, WHITE)
                text_rect = text1.get_rect()
                text_x = (3 / 4) * sc.get_width() - text_rect.width / 2
                text_y = 100

                sc.blit(text1, [text_x, text_y])

        if flag:
            pg.draw.rect(sc, WHITE, ((3 / 4) * sc.get_width() - 100, 100, 300, 50))
        pg.display.update()
        clock.tick(FPS)


surface = pg.display.set_mode((600, 400))
menu = pygame_menu.Menu('Игры на графах', 400, 300, theme=pygame_menu.themes.THEME_BLUE)
menu.add.text_input('Количество клеток: ', default='5', onreturn=set_difficulty)
menu.add.button('Крестики без ноликов', start_game_xxx)
menu.add.button('Круги', start_game_circle)
menu.add.button('Выход', pygame_menu.events.EXIT)
menu.mainloop(surface)