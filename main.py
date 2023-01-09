import random
from time import time
from copy import copy
from copy import deepcopy
import pygame as pg
from Games import Game_xxx
from Games import GameCircle
from Games import GameHackenbush
from math import sin, cos, pi
pg.init()
Difficulty = 5


class Button:
    def __init__(self, surface = None, color = None, x = 0, y = 0, length = 0, height = 0, text = None, text_color = None):
        self.surface = surface
        self.color = color
        self.x = x
        self.y = y
        self.length = length
        self.height = height
        self.text = text
        self.text_color = text_color
        if surface is not None:
            self.draw_button()
            self.write_text()
        self.rect = pg.Rect(x, y, length, height)

    def write_text(self):
        my_font = pg.font.SysFont("Calibri", 20)
        my_text = my_font.render(self.text, True, self.text_color)
        self.surface.blit(my_text, ((self.x+self.length/2) - my_text.get_width()/2, (self.y+self.height/2) - my_text.get_height()/2))

    def draw_button(self):
        pg.draw.rect(self.surface, self.color, (self.x, self.y, self.length, self.height), 0)
        pg.draw.rect(self.surface, (190, 190, 190), (self.x, self.y, self.length, self.height), 1)

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


class Edge:
    def __init__(self, v1, v2, vn1, vn2):
        self.v1 = v1
        self.v2 = v2
        self.vn1 = vn1
        self.vn2 = vn2

    def pressed(self, mouse):
        return abs((self.v2[1] - self.v1[1]) * mouse[0] - (self.v2[0] - self.v1[0]) * mouse[1] + self.v2[0] * self.v1[1] - self.v2[1] * self.v1[0]) / ((self.v2[1] - self.v1[1]) ** 2 + (self.v2[0] - self.v1[0]) ** 2) ** 0.5 < 5


def make_game_xxx(game):
    vertexs = []
    edges = []

    def make_game_xx(game):
        nonlocal vertexs
        vertexs.append(game)
        if not game.check_lose():
            for i in range(len(game)):
                if game.can_do_move(i):
                    new_field = copy(game.field)
                    new_field[i] = "X"
                    for node in vertexs:
                        if node.field == new_field:
                            node.parents.append(game)
                            game.children.append(node)
                            edges.append([game, node])
                            break
                    else:
                        game.create_child(new_field)
                        edges.append([game, game.children[-1]])
                        game.children[-1].id = str(game.id) + "_" + str(i)
                        make_game_xx(game.children[-1])

    make_game_xx(game)
    return vertexs, edges


def make_game_circle(game):
    vertexs = []
    edges = []

    def make_game_circl(game):
        nonlocal vertexs
        nonlocal edges
        vertexs.append(game)
        if not game.check_lose():
            for i in range(len(game)):
                for j in range(len(game)):
                    if game.can_do_move(i, j) and i != j:
                        new_edges = copy(game.edges)
                        new_edges.append([i, j])
                        for node in vertexs:
                            if edge_com(node.edges, new_edges):
                                node.parents.append(game)
                                game.children.append(node)
                                edges.append([game, node])
                                break
                        else:
                            game.create_child(new_edges)
                            edges.append([game, game.children[-1]])
                            game.children[-1].id = str(game.id) + "_" + str(i)
                            make_game_circl(game.children[-1])

    make_game_circl(game)
    return vertexs, edges


def make_game_hack(game):
    vertexs = []
    edges = []

    def make_game_h(game):
        nonlocal vertexs
        nonlocal edges
        vertexs.append(game)
        if not game.check_lose():
            for i in range(len(game)):
                for j in range(len(game)):
                    if game.can_do_move(i, j) and i != j:
                        new_matrix = deepcopy(game.matrix)
                        new_matrix[i][j] = 0
                        new_matrix[j][i] = 0
                        for node in vertexs:
                            if matrix_com(node.matrix, new_matrix):
                                node.parents.append(game)
                                game.children.append(node)
                                edges.append([game, node])
                                break
                        else:
                            game.create_child(game.list_of_vertexes, new_matrix)
                            edges.append([game, game.children[-1]])
                            game.children[-1].id = str(game.id) + "_" + str(i)
                            make_game_h(game.children[-1])

    make_game_h(game)
    return vertexs, edges


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


def set_difficulty():
    global Difficulty
    WIDTH = 600
    HEIGTH = 400
    sc = pg.display.set_mode((WIDTH, HEIGTH))
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    sc.fill(BLACK)
    font = pg.font.SysFont('Calibri', 45)
    head = font.render("Размер поля", True, WHITE, 5)
    head_rect = head.get_rect()
    head_x = sc.get_width() / 2 - head_rect.width / 2
    head_y = 10
    sc.blit(head, [head_x, head_y])
    btn = Button(sc, WHITE, 230, 300, 150, 40, "Вернуться к игре", BLACK)

    slider_value = 50

    slider_width = 300
    slider_height = 50
    slider_x = 150
    slider_y = 125
    handle_width = 50
    handle_height = 50
    handle_x = slider_x + (slider_value * (slider_width - handle_width) / 100)
    handle_y = slider_y

    dragging = False
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if btn.pressed(pg.mouse.get_pos()):
                    return 0
                mouse_x, mouse_y = pg.mouse.get_pos()
                if handle_x <= mouse_x <= handle_x + handle_width and handle_y <= mouse_y <= handle_y + handle_height:
                    dragging = True
            elif event.type == pg.MOUSEBUTTONUP:
                dragging = False
            elif event.type == pg.MOUSEMOTION:
                if dragging:
                    mouse_x, mouse_y = pg.mouse.get_pos()
                    handle_x = max(slider_x, min(mouse_x - handle_width / 2, slider_x + slider_width - handle_width))
                    slider_value = int((handle_x - slider_x) * 100 / (slider_width - handle_width))
                    Difficulty = slider_value // 10

        sc.fill(BLACK)
        sc.blit(head, [head_x, head_y])
        btn.draw_button()
        btn.write_text()
        pg.draw.rect(sc, WHITE, (slider_x, slider_y, slider_width, slider_height))
        pg.draw.rect(sc, (100, 0, 0), (handle_x, handle_y, handle_width, handle_height))
        text = font.render(str(Difficulty), True, WHITE, 5)
        text_rect = text.get_rect()
        text_x = sc.get_width() / 2 - text_rect.width / 2
        text_y = 230
        sc.blit(text, [text_x, text_y])
        pg.display.update()


def set_difficulty_circle():
    global Difficulty
    WIDTH = 600
    HEIGTH = 400
    sc = pg.display.set_mode((WIDTH, HEIGTH))
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    sc.fill(BLACK)
    font = pg.font.SysFont('Calibri', 45)
    head = font.render("Размер поля", True, WHITE, 5)
    head_rect = head.get_rect()
    head_x = sc.get_width() / 2 - head_rect.width / 2
    head_y = 10
    sc.blit(head, [head_x, head_y])
    btn = Button(sc, WHITE, 230, 300, 150, 40, "Вернуться к игре", BLACK)

    slider_value = 50

    slider_width = 300
    slider_height = 50
    slider_x = 150
    slider_y = 125
    handle_width = 50
    handle_height = 50
    handle_x = slider_x + (slider_value * (slider_width - handle_width) / 100)
    handle_y = slider_y

    dragging = False
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if btn.pressed(pg.mouse.get_pos()):
                    return 0
                mouse_x, mouse_y = pg.mouse.get_pos()
                if handle_x <= mouse_x <= handle_x + handle_width and handle_y <= mouse_y <= handle_y + handle_height:
                    dragging = True
            elif event.type == pg.MOUSEBUTTONUP:
                dragging = False
            elif event.type == pg.MOUSEMOTION:
                if dragging:
                    mouse_x, mouse_y = pg.mouse.get_pos()
                    handle_x = max(slider_x, min(mouse_x - handle_width / 2, slider_x + slider_width - handle_width))
                    slider_value = int((handle_x - slider_x) * 100 / (slider_width - handle_width))
                    Difficulty = slider_value // 12

        sc.fill(BLACK)
        sc.blit(head, [head_x, head_y])
        btn.draw_button()
        btn.write_text()
        pg.draw.rect(sc, WHITE, (slider_x, slider_y, slider_width, slider_height))
        pg.draw.rect(sc, (100, 0, 0), (handle_x, handle_y, handle_width, handle_height))
        text = font.render(str(Difficulty), True, WHITE, 5)
        text_rect = text.get_rect()
        text_x = sc.get_width() / 2 - text_rect.width / 2
        text_y = 230
        sc.blit(text, [text_x, text_y])
        pg.display.update()


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


def matrix_com(matrix1, matrix2):
    for i in range(len(matrix1)):
        for j in range(len(matrix2)):
            if matrix1[i][j] != matrix2[i][j]:
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


def vertex_merge_hack(vertexes : set):
    vertexes = list(vertexes)
    for v1 in vertexes:
        for v2 in vertexes:
            if v1 != v2 and matrix_com(v1.matrix, v2.matrix):
                v1.parents.extend(v2.parents)
                for v3 in v2.parents:
                    v3.children.append(v1)
                    v3.children.remove(v2)
                vertexes.remove(v2)
    return vertexes


def get_vertexes(root):
    vertexes = set()
    def create_vertex_xxx(root):
        vertexs = []
        qstart = 0
        queue = dict()
        vertexs.append(root)
        queue[root.lvl] = [0]
        while qstart < len(vertexs):
            v = vertexs[qstart]
            qstart += 1
            if v.lvl not in queue.keys():
                queue[v.lvl] = [qstart]
                queue[v.lvl - 1].append(qstart - 1)
            for i in range(len(v.children)):
                vertexs.append(v.children[i])
        print(len(vertexs))
        queue[vertexs[qstart - 1].lvl].append(qstart - 1)
        for v in vertexs:
            i = queue[v.lvl][0]
            while i <= queue[v.lvl][1]:
                try:
                    if v != vertexs[i] and vertexs[i].field == v.field:
                        v.parents.extend(vertexs[i].parents)
                        for v3 in vertexs[i].parents:
                            v3.children.append(v)
                            v3.children.remove(vertexs[i])
                        vertexs.remove(vertexs[i])
                        queue[v.lvl][1] -= 1
                        for j in range(v.lvl + 1, len(queue.keys())):
                            queue[j][0] -= 1
                            queue[j][1] -= 1
                    else:
                        i += 1
                except IndexError:
                    print(i)
                    raise IndexError
        print(len(vertexs))
        return vertexs

    def create_vertex_circle(root):
        vertexs = []
        qstart = 0
        queue = dict()
        vertexs.append(root)
        queue[root.lvl] = [0]
        while qstart < len(vertexs):
            v = vertexs[qstart]
            qstart += 1
            if v.lvl not in queue.keys():
                queue[v.lvl] = [qstart]
                queue[v.lvl - 1].append(qstart - 1)
            for i in range(len(v.children)):
                vertexs.append(v.children[i])

        queue[vertexs[qstart - 1].lvl].append(qstart - 1)
        for v in vertexs:
            i = queue[v.lvl][0]
            while i <= queue[v.lvl][1]:
                try:
                    if v != vertexs[i] and edge_com(v.edges, vertexs[i].edges):
                        v.parents.extend(vertexs[i].parents)
                        for v3 in vertexs[i].parents:
                            v3.children.append(v)
                            v3.children.remove(vertexs[i])
                        vertexs.remove(vertexs[i])
                        queue[v.lvl][1] -= 1
                        for j in range(v.lvl + 1, len(queue.keys())):
                            queue[j][0] -= 1
                            queue[j][1] -= 1
                    else:
                        i += 1
                except IndexError:
                    print(i)
                    raise IndexError
        return vertexs

    def create_vertex_hack(root):
        vertexs = []
        qstart = 0
        queue = dict()
        vertexs.append(root)
        queue[root.lvl] = [0]
        while qstart < len(vertexs):
            v = vertexs[qstart]
            qstart += 1
            if v.lvl not in queue.keys():
                queue[v.lvl] = [qstart]
                queue[v.lvl - 1].append(qstart - 1)
            for i in range(len(v.children)):
                vertexs.append(v.children[i])

        queue[vertexs[qstart - 1].lvl].append(qstart - 1)
        for v in vertexs:
            i = queue[v.lvl][0]
            while i <= queue[v.lvl][1]:
                try:
                    if v != vertexs[i] and matrix_com(v.matrix, vertexs[i].matrix):
                        v.parents.extend(vertexs[i].parents)
                        for v3 in vertexs[i].parents:
                            v3.children.append(v)
                            v3.children.remove(vertexs[i])
                        vertexs.remove(vertexs[i])
                        queue[v.lvl][1] -= 1
                        for j in range(v.lvl + 1, len(queue.keys())):
                            queue[j][0] -= 1
                            queue[j][1] -= 1
                    else:
                        i += 1
                except IndexError:
                    print(i)
                    raise IndexError
        return vertexs

    def create_vertex(root):
        nonlocal vertexes
        vertexes.add(root)
        if root.children:
            for i in range(len(root.children)):
                create_vertex(root.children[i])
    if type(root) is Game_xxx:
        return create_vertex_xxx(root)
    if type(root) is GameCircle:
        return create_vertex_circle(root)
    if type(root) is GameHackenbush:
        return create_vertex_hack(root)


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


def open_info(text):
    WIDTH = 600
    HEIGTH = 400
    sc = pg.display.set_mode((WIDTH, HEIGTH))
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    sc.fill(BLACK)
    font = pg.font.SysFont('Calibri', 45)
    head = font.render("Справка", True, WHITE, 5)
    head_rect = head.get_rect()
    head_x = sc.get_width() / 2 - head_rect.width / 2
    head_y = 10
    sc.blit(head, [head_x, head_y])
    textlines = text.split("\n")
    font = pg.font.SysFont('Calibri', 25)
    text_x = 20
    text_y = 60
    for line in textlines:
        text = font.render(line, True, WHITE, 5)
        sc.blit(text, [text_x, text_y])
        text_y += 25
    btn = Button(sc, WHITE, 230, 300, 150, 40, "Вернуться к игре", BLACK)
    pg.display.update()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if btn.pressed(pg.mouse.get_pos()):
                    return 0


def start_game_xxx():
    global Difficulty
    sizeblock = 100
    margine = 15
    a = Difficulty
    WIDTH = max(sizeblock * a + margine * (a + 1), 1200)
    HEIGTH = 600
    sc = pg.display.set_mode((WIDTH, HEIGTH))
    pg.display.set_caption('Крестики без ноликов!')
    text = """Два игрока играют на поле 1×n (n ≥ 3),
своим ходом игрок может поставить крестик в любую
свободную клетку. Игрок, после хода которого на 
поле есть ряд из трех крестиков, побеждает"""
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
    vertexes, list_of_edges = make_game_xxx(game_xxx)
    #vertexes = get_vertexes(game_xxx)
    #list_of_edges = get_edges(game_xxx)
    vertex_marking(vertexes=vertexes, list_of_edges=list_of_edges, root=game_xxx)
    sc.fill(BLACK)
    for col in range(a):
        x = col * sizeblock + (col + 1) * margine
        y = 0 * sizeblock + 1 * margine
        pg.draw.rect(sc, WHITE, (x, y, sizeblock, sizeblock))
    query = 0
    field = copy(game_xxx.field)
    game_over = False
    btn = Button(sc, WHITE, 10, 150, 150, 40, "Перезапуск", BLACK)
    btn_grph = Button(sc, WHITE, 210, 150, 150, 40, "Вывод графа", BLACK)
    btn_menu = Button(sc, WHITE, 810, 150, 150, 40, "Назад в меню", BLACK)
    btn_ref = Button(sc, WHITE, 410, 150, 150, 40, "Справка", BLACK)
    btn_dif = Button(sc, WHITE, 610, 150, 150, 40, "Размер поля", BLACK)
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
                if y_mouse <= sizeblock + 2*margine and not game_over and x_mouse < sizeblock * a + margine * a:
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
                    btn.draw_button()
                    btn.write_text()
                    btn_grph.draw_button()
                    btn_grph.write_text()
                    btn_menu.draw_button()
                    btn_menu.write_text()
                    btn_ref.draw_button()
                    btn_ref.write_text()
                    btn_dif.draw_button()
                    btn_dif.write_text()
                elif btn_grph.pressed(pg.mouse.get_pos()):
                    print_graph(vertexes, list_of_edges, game_xxx.get_root(), game_xxx)
                    sc.fill(BLACK)
                    for col in range(a):
                        x = col * sizeblock + (col + 1) * margine
                        y = 0 * sizeblock + 1 * margine
                        pg.draw.rect(sc, WHITE, (x, y, sizeblock, sizeblock))
                    btn.draw_button()
                    btn.write_text()
                    btn_grph.draw_button()
                    btn_grph.write_text()
                    btn_menu.draw_button()
                    btn_menu.write_text()
                    btn_ref.draw_button()
                    btn_ref.write_text()
                    btn_dif.draw_button()
                    btn_dif.write_text()
                elif btn_menu.pressed(pg.mouse.get_pos()):
                    return 0
                elif btn_ref.pressed(pg.mouse.get_pos()):
                    open_info(text)
                    sc = pg.display.set_mode((WIDTH, HEIGTH))
                    sc.fill(BLACK)
                    for col in range(a):
                        x = col * sizeblock + (col + 1) * margine
                        y = 0 * sizeblock + 1 * margine
                        pg.draw.rect(sc, WHITE, (x, y, sizeblock, sizeblock))
                    btn.draw_button()
                    btn.write_text()
                    btn_grph.draw_button()
                    btn_grph.write_text()
                    btn_menu.draw_button()
                    btn_menu.write_text()
                    btn_ref.draw_button()
                    btn_ref.write_text()
                    btn_dif.draw_button()
                    btn_dif.write_text()
                elif btn_dif.pressed(pg.mouse.get_pos()):
                    set_difficulty()
                    start_game_xxx()
                    Difficulty = 5
                    return 0
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
    pg.display.set_caption('Игра "ОМакс"!')

    clock = pg.time.Clock()
    text = """Дана окружность, вдоль которой нанесены
несколько различных точек. За один ход разрешается 
провести хорду, которая не должна иметь общих
точек с ранее проведенными хордами (в том числе
они не должны иметь общих концов). Игрок, который
не может провести хорду по этим правилам,
считается проигравшим."""
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
    vertexes, list_of_edges = make_game_circle(game_circle)
    #vertexes = get_vertexes(game_circle)
    #list_of_edges = get_edges(game_circle)
    vertex_marking(vertexes=vertexes, list_of_edges=list_of_edges, root=game_circle)

    sc.fill(BLACK)
    center = (500, 400)
    r = 100
    pg.draw.circle(sc, WHITE, center, r + 2)
    pg.draw.circle(sc, BLACK, center, r)

    dots = []
    angle = 0
    while angle < 2 * pi - 0.1:
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
    btn = Button(sc, WHITE, 10, 150, 150, 40, "Перезапуск", BLACK)
    btn_grph = Button(sc, WHITE, 210, 150, 150, 40, "Вывод графа", BLACK)
    btn_menu = Button(sc, WHITE, 810, 150, 150, 40, "Назад в меню", BLACK)
    btn_ref = Button(sc, WHITE, 410, 150, 150, 40, "Справка", BLACK)
    btn_dif = Button(sc, WHITE, 610, 150, 150, 40, "Размер поля", BLACK)
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
                    btn.draw_button()
                    btn.write_text()
                    btn_grph.draw_button()
                    btn_grph.write_text()
                    btn_menu.draw_button()
                    btn_menu.write_text()
                    btn_ref.draw_button()
                    btn_ref.write_text()
                    btn_dif.draw_button()
                    btn_dif.write_text()
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
                    btn.draw_button()
                    btn.write_text()
                    btn_grph.draw_button()
                    btn_grph.write_text()
                    btn_menu.draw_button()
                    btn_menu.write_text()
                    btn_ref.draw_button()
                    btn_ref.write_text()
                    btn_dif.draw_button()
                    btn_dif.write_text()
                elif btn_menu.pressed(pg.mouse.get_pos()):
                    return 0
                elif btn_ref.pressed(pg.mouse.get_pos()):
                    open_info(text)
                    sc = pg.display.set_mode((WIDTH, HEIGTH))
                    sc.fill(BLACK)
                    pg.draw.circle(sc, WHITE, center, r + 2)
                    pg.draw.circle(sc, BLACK, center, r)
                    for dot in dots:
                        pg.draw.circle(sc, RED, dot, 4)
                    for edge in game_circle.edges:
                        pg.draw.line(sc, WHITE, dots[edge[0]], dots[edge[1]])
                        pg.draw.circle(sc, RED, dots[edge[0]], 4)
                        pg.draw.circle(sc, RED, dots[edge[1]], 4)
                    btn.draw_button()
                    btn.write_text()
                    btn_grph.draw_button()
                    btn_grph.write_text()
                    btn_menu.draw_button()
                    btn_menu.write_text()
                    btn_ref.draw_button()
                    btn_ref.write_text()
                    btn_dif.draw_button()
                    btn_dif.write_text()
                elif btn_dif.pressed(pg.mouse.get_pos()):
                    set_difficulty_circle()
                    start_game_circle()
                    return 0

        pg.display.update()
        clock.tick(FPS)


def edit_hack():
    sc = pg.display.set_mode((800, 600))
    pg.display.set_caption("Редактор")

    clock = pg.time.Clock()
    FPS = 30
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    list_node = dict()
    matrix = []
    node_selected = False
    node_selected_index = -1
    idd = 0
    sc.fill(WHITE)
    btn_end = Button(sc, WHITE, 110, 450, 150, 40, "Задать", BLACK)
    btn_menu = Button(sc, WHITE, 310, 450, 150, 40, "Назад в меню", BLACK)
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pg.mouse.get_pos()
                if event.button == 1:
                    if btn_end.pressed(pg.mouse.get_pos()):
                        return list_node, matrix
                    elif btn_menu.pressed(pg.mouse.get_pos()):
                        return 0, 0
                    else:
                        for i in list_node.keys():
                            if abs(list_node[i][0] - mouse_x) < 15 and abs(list_node[i][1] - mouse_y) < 15:
                                node_selected = True
                                node_selected_index = i
                                break
                        else:
                            node_selected = False
                            list_node[idd] = (mouse_x, mouse_y)
                            idd += 1
                            matrix.append([0] * idd)
                            for line in matrix:
                                line.extend([0] * (idd - len(line)))

                if event.button == 3:
                    nodekeys = [i for i in list_node.keys()]
                    nodekeys.sort()
                    for i in range(len(nodekeys)):
                        if abs(list_node[nodekeys[i]][0] - mouse_x) < 15 and abs(
                                list_node[nodekeys[i]][1] - mouse_y) < 15:
                            list_node.pop(nodekeys[i])
                            for line in matrix:
                                line.pop(i)
                            matrix.pop(i)
                            idd -= 1
                            break
            if event.type == pg.MOUSEBUTTONUP:
                mouse_x, mouse_y = pg.mouse.get_pos()
                if event.button == 1:
                    if node_selected:
                        nodekeys = [i for i in list_node.keys()]
                        nodekeys.sort()
                        for i in range(len(nodekeys)):
                            if abs(list_node[nodekeys[i]][0] - mouse_x) < 15 and abs(
                                    list_node[nodekeys[i]][1] - mouse_y) < 15:
                                if i != node_selected_index:
                                    matrix[node_selected_index][i] = 1
                                    matrix[i][node_selected_index] = 1
                                break
                        node_selected = False

        sc.fill(WHITE)
        if node_selected:
            pg.draw.line(sc, (0, 0, 0), list_node[node_selected_index], pg.mouse.get_pos(), 4)

        nodekeys = [i for i in list_node.keys()]
        nodekeys.sort()
        for i in range(len(nodekeys)):
            for j in range(len(nodekeys)):
                if matrix[i][j] == 1:
                    pg.draw.line(sc, BLACK, list_node[nodekeys[i]], list_node[nodekeys[j]], 5)

        for key in list_node.keys():
            pg.draw.circle(sc, GREEN, list_node[key], 15)
        btn_end.draw_button()
        btn_end.write_text()
        btn_menu.draw_button()
        btn_menu.write_text()
        clock.tick(FPS)
        pg.display.update()


def start_game_hack():
    list_node, matrix = edit_hack()
    if list_node == 0 and matrix == 0:
        return 0

    for key in list_node.keys():
        list_node[key] = (list_node[key][0], list_node[key][1] + 150)
    WIDTH = 1200
    HEIGTH = 600
    sc = pg.display.set_mode((WIDTH, HEIGTH))
    pg.display.set_caption('Игра "Хакенбуш"!')

    clock = pg.time.Clock()
    text = """Пусть задан неориентированный граф G и вершина s
в нем. Два игрока делают ходы по очереди. Своим 
ходом игрок может выбрать любое ребро графа и 
удалить его. Игрок, который не может сделать ход,
поскольку граф состоит из единственной вершины
s — проигрывает"""
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


    game_hack = GameHackenbush(list_node, matrix, 0)
    vertexes, list_of_edges = make_game_hack(game_hack)
    #vertexes = get_vertexes(game_hack)

    #list_of_edges = get_edges(game_hack)
    vertex_marking(vertexes=vertexes, list_of_edges=list_of_edges, root=game_hack)

    sc.fill(BLACK)
    edges = []
    nodekeys = [i for i in list_node.keys()]
    nodekeys.sort()
    for i in range(len(nodekeys)):
        for j in range(len(nodekeys)):
            if matrix[i][j] == 1:
                pg.draw.line(sc, WHITE, list_node[nodekeys[i]], list_node[nodekeys[j]], 5)
                edges.append(Edge(list_node[nodekeys[i]], list_node[nodekeys[j]], nodekeys[i], nodekeys[j]))

    for key in list_node.keys():
        pg.draw.circle(sc, GREEN, list_node[key], 15)

    pg.draw.circle(sc, RED, list_node[game_hack.root], 15)
    query = 0
    field = deepcopy(game_hack.matrix)

    game_over = False
    btn = Button(sc, WHITE, 10, 150, 150, 40, "Перезапуск", BLACK)
    btn_grph = Button(sc, WHITE, 210, 150, 150, 40, "Вывод графа", BLACK)
    btn_menu = Button(sc, WHITE, 810, 150, 150, 40, "Назад в меню", BLACK)
    btn_ref = Button(sc, WHITE, 410, 150, 150, 40, "Справка", BLACK)
    while True:
        game_over = game_over if game_over else game_hack.check_lose()
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
                for col in range(len(edges)):
                    if edges[col].pressed((x_mouse, y_mouse)) and not game_over:
                        if game_hack.can_do_move(edges[col].vn1, edges[col].vn2):
                            query = 0
                            field[edges[col].vn1][edges[col].vn2] = 0
                            field[edges[col].vn2][edges[col].vn1] = 0
                            for i in range(len(game_hack.children)):
                                if matrix_com(game_hack.children[i].matrix, field):
                                    game_hack = game_hack.children[i]
                                    break
                            sc.fill(BLACK)
                            nodekeys = [i for i in list_node.keys()]
                            nodekeys.sort()
                            for i in range(len(nodekeys)):
                                for j in range(len(nodekeys)):
                                    if field[i][j] == 1:
                                        pg.draw.line(sc, WHITE, list_node[nodekeys[i]], list_node[nodekeys[j]], 5)

                            for key in list_node.keys():
                                pg.draw.circle(sc, GREEN, list_node[key], 15)

                            pg.draw.circle(sc, RED, list_node[game_hack.root], 15)
                            btn.draw_button()
                            btn.write_text()
                            btn_grph.draw_button()
                            btn_grph.write_text()
                            btn_menu.draw_button()
                            btn_menu.write_text()
                            btn_ref.draw_button()
                            btn_ref.write_text()
                            game_hack, flag = bot_decision(game_hack)
                            if flag:
                                field = deepcopy(game_hack.matrix)
                                query = 1
                                sc.fill(BLACK)
                                nodekeys = [i for i in list_node.keys()]
                                nodekeys.sort()
                                for i in range(len(nodekeys)):
                                    for j in range(len(nodekeys)):
                                        if field[i][j] == 1:
                                            pg.draw.line(sc, WHITE, list_node[nodekeys[i]], list_node[nodekeys[j]], 5)

                                for key in list_node.keys():
                                    pg.draw.circle(sc, GREEN, list_node[key], 15)

                                pg.draw.circle(sc, RED, list_node[game_hack.root], 15)
                                btn.draw_button()
                                btn.write_text()
                                btn_grph.draw_button()
                                btn_grph.write_text()
                                btn_menu.draw_button()
                                btn_menu.write_text()
                                btn_ref.draw_button()
                                btn_ref.write_text()
                            else:
                                game_over = True
                if btn.pressed((x_mouse, y_mouse)):
                    game_over = False
                    game_hack = game_hack.get_root()
                    field = deepcopy(game_hack.matrix)
                    sc.fill(BLACK)
                    nodekeys = [i for i in list_node.keys()]
                    nodekeys.sort()
                    for i in range(len(nodekeys)):
                        for j in range(len(nodekeys)):
                            if field[i][j] == 1:
                                pg.draw.line(sc, WHITE, list_node[nodekeys[i]], list_node[nodekeys[j]], 5)

                    for key in list_node.keys():
                        pg.draw.circle(sc, GREEN, list_node[key], 15)

                    pg.draw.circle(sc, RED, list_node[game_hack.root], 15)
                    btn.draw_button()
                    btn.write_text()
                    btn_grph.draw_button()
                    btn_grph.write_text()
                    btn_menu.draw_button()
                    btn_menu.write_text()
                    btn_ref.draw_button()
                    btn_ref.write_text()
                elif btn_grph.pressed((x_mouse, y_mouse)):
                    print_graph(vertexes, list_of_edges, game_hack.get_root(), game_hack)
                    sc.fill(BLACK)
                    nodekeys = [i for i in list_node.keys()]
                    nodekeys.sort()
                    for i in range(len(nodekeys)):
                        for j in range(len(nodekeys)):
                            if field[i][j] == 1:
                                pg.draw.line(sc, WHITE, list_node[nodekeys[i]], list_node[nodekeys[j]], 5)

                    for key in list_node.keys():
                        pg.draw.circle(sc, GREEN, list_node[key], 15)

                    pg.draw.circle(sc, RED, list_node[game_hack.root], 15)
                    btn.draw_button()
                    btn.write_text()
                    btn_grph.draw_button()
                    btn_grph.write_text()
                    btn_menu.draw_button()
                    btn_menu.write_text()
                    btn_ref.draw_button()
                    btn_ref.write_text()
                elif btn_menu.pressed(pg.mouse.get_pos()):
                    return 0
                elif btn_ref.pressed(pg.mouse.get_pos()):
                    open_info(text)
                    sc = pg.display.set_mode((WIDTH, HEIGTH))
                    sc.fill(BLACK)
                    nodekeys = [i for i in list_node.keys()]
                    nodekeys.sort()
                    for i in range(len(nodekeys)):
                        for j in range(len(nodekeys)):
                            if field[i][j] == 1:
                                pg.draw.line(sc, WHITE, list_node[nodekeys[i]], list_node[nodekeys[j]], 5)

                    for key in list_node.keys():
                        pg.draw.circle(sc, GREEN, list_node[key], 15)

                    pg.draw.circle(sc, RED, list_node[game_hack.root], 15)
                    btn.draw_button()
                    btn.write_text()
                    btn_grph.draw_button()
                    btn_grph.write_text()
                    btn_menu.draw_button()
                    btn_menu.write_text()
                    btn_ref.draw_button()
                    btn_ref.write_text()

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

    btn = Button(sc, WHITE, (3 / 4) * sc.get_width(), 150, 150, 40, "Вернуться к игре", BLACK)
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
                font = pg.font.SysFont('Calibri', 25)
                text1 = font.render(str(v), True, BLACK, WHITE)
                text_rect = text1.get_rect()
                text_x = (1 / 2) * sc.get_width() - text_rect.width / 2
                text_y = 10

                sc.blit(text1, [text_x, text_y])

        if flag:
            pg.draw.rect(sc, WHITE, (0, 0, 1200, 50))
        pg.display.update()
        clock.tick(FPS)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (225, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
surface = pg.display.set_mode((600, 400))
surface.fill(BLACK)
font = pg.font.SysFont('Calibri', 45)
text1 = font.render("Игры на графах", True, WHITE, 5)
clock = pg.time.Clock()
x = surface.get_width() / 2 - 125
y = 75
FPS = 30
surface.blit(text1, [surface.get_width() / 2 - text1.get_rect().width / 2, y - 25])
btn_menu1 = Button(surface, WHITE, x, y + 50, 250, 40, "Хакенбуш", BLACK)
btn_menu2 = Button(surface, WHITE, x, y + 100, 250, 40, "Крестики без ноликов", BLACK)
btn_menu3 = Button(surface, WHITE, x, y + 150, 250, 40, 'Игра "ОМакс"', BLACK)
btn_menu4 = Button(surface, WHITE, x, y + 200, 250, 40, "Выход", BLACK)
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()
        elif event.type == pg.MOUSEBUTTONDOWN:
            if btn_menu1.pressed(pg.mouse.get_pos()):
                start_game_hack()
                surface = pg.display.set_mode((600, 400))
                surface.blit(text1, [surface.get_width() / 2 - text1.get_rect().width / 2, y - 25])
                btn_menu1.draw_button()
                btn_menu1.write_text()
                btn_menu2.draw_button()
                btn_menu2.write_text()
                btn_menu3.draw_button()
                btn_menu3.write_text()
                btn_menu4.draw_button()
                btn_menu4.write_text()
            elif btn_menu2.pressed(pg.mouse.get_pos()):
                start_game_xxx()
                surface = pg.display.set_mode((600, 400))
                surface.blit(text1, [surface.get_width() / 2 - text1.get_rect().width / 2, y - 25])
                btn_menu1.draw_button()
                btn_menu1.write_text()
                btn_menu2.draw_button()
                btn_menu2.write_text()
                btn_menu3.draw_button()
                btn_menu3.write_text()
                btn_menu4.draw_button()
                btn_menu4.write_text()
            elif btn_menu3.pressed(pg.mouse.get_pos()):
                start_game_circle()
                surface = pg.display.set_mode((600, 400))
                surface.blit(text1, [surface.get_width() / 2 - text1.get_rect().width / 2, y - 25])
                btn_menu1.draw_button()
                btn_menu1.write_text()
                btn_menu2.draw_button()
                btn_menu2.write_text()
                btn_menu3.draw_button()
                btn_menu3.write_text()
                btn_menu4.draw_button()
                btn_menu4.write_text()
            elif btn_menu4.pressed(pg.mouse.get_pos()):
                pg.quit()
                quit()

    pg.display.update()
    clock.tick(FPS)