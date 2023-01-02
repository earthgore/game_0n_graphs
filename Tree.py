class Game:
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
        child = Game(field)
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

    def move(self, i):
        self.field[i] = "X"

    def can_do_move(self, i):
        if self.field[i] == "X":
            return False
        else:
            return True

    def __len__(self):
        return len(self.field)
