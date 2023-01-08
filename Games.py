class GameHackenbush:
    def __init__(self, list_of_vertex, matrix, node):
        self.children = []
        self.parents = []
        self.terms = []
        self.root = node
        self.list_of_vertexes = list_of_vertex
        self.matrix = matrix
        self.mark = ""
        self.id = "0"
        self.pos = [100, 100]
        self.lvl = 0

    def create_child(self, list_of_vertex, matrix):
        child = GameHackenbush(list_of_vertex, matrix, self.root)
        self.children.append(child)
        child.lvl = self.lvl + 1
        child.parents.append(self)

    def check_lose(self):
        for value in self.matrix[self.root]:
            if value == 1:
                return False
        return True

    def get_root(self):
        if not self.parents:
            return self
        else:
            working_node = self.parents[0]
            while working_node.parents:
                working_node = working_node.parents[0]
            return working_node

    def can_do_move(self, v1, v2):
        def dfs_hack(node, matrix):
            nonlocal v_vertexes
            v_vertexes.append(node)
            for v in range(len(matrix[node])):
                if matrix[node][v] == 1 and v not in v_vertexes:
                    dfs_hack(v, matrix)
        v_vertexes = []
        dfs_hack(self.root, self.matrix)
        if v1 not in v_vertexes or v2 not in v_vertexes:
            return False
        elif self.matrix[v1][v2] == 1:
            return True
        return False

    def __len__(self):
        return len(self.matrix)

    def __str__(self):
        return str(self.matrix)


class Game_xxx:
    def __init__(self, field : list):
        self.field = field
        self.children = list()
        self.parents = list()
        self.terms = list()
        self.mark = ""
        self.id = "0"
        self.pos = [100, 100]
        self.lvl = 0

    def create_child(self, field):
        child = Game_xxx(field)
        self.children.append(child)
        child.lvl = self.lvl + 1
        child.parents.append(self)

    def check_lose(self):
        for i in range(len(self.field)):
            if self.field[i-1] == "X" and self.field[i] == "X" and self.field[(i+1) % len(self.field)] == "X":
                return True
        return False

    def get_root(self):
        if not self.parents:
            return self
        else:
            working_node = self.parents[0]
            while working_node.parents:
                working_node = working_node.parents[0]
            return working_node

    def __str__(self):
        return "".join(self.field) + self.mark

    def can_do_move(self, i):
        if self.field[i] == "X":
            return False
        else:
            return True

    def __len__(self):
        return len(self.field)


class GameCircle:
    def __init__(self, edges, n):
        self.children = list()
        self.parents = list()
        self.terms = list()
        self.edges = edges
        self.nodes = [True]*n
        self.mark = ""
        self.id = "0"
        self.pos = [100, 100]
        self.lvl = 0
        for edge in self.edges:
            self.nodes[edge[0]] = False
            self.nodes[edge[1]] = False

    def create_child(self, edges):
        child = GameCircle(edges, len(self))
        self.children.append(child)
        child.lvl = self.lvl + 1
        child.parents.append(self)

    def check_lose(self):
        for i in range(len(self.nodes)):
            for j in range(len(self.nodes)):
                if self.can_do_move(i, j):
                    return False
        return True

    def get_root(self):
        if not self.parents:
            return self
        else:
            working_node = self.parents[0]
            while working_node.parents:
                working_node = working_node.parents[0]
            return working_node

    def __str__(self):
        s = ""
        for edge in self.edges:
            s += "[" + str(edge[0]) + "-" + str(edge[1]) + "]"
        return s + self.mark

    def can_do_move(self, i, j):
        mi = min(i, j)
        ma = max(i, j)
        if self.nodes[i] and self.nodes[j] and mi != ma:
            for edge in self.edges:
                if (edge[0] < mi or edge[0] > ma) and (edge[1] > mi and edge[1] < ma):
                    return False
                elif (edge[1] < mi or edge[1] > ma) and (edge[0] > mi and edge[0] < ma):
                    return False
            return True
        return False

    def __len__(self):
        return len(self.nodes)

