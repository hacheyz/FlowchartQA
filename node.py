class Node:
    def __init__(self, id: int, code: str, name: str, type: int):
        self.id = id  # 0, 1, 2, ...
        self.code = code  # A, B, C, ...
        self.name = name  # given random string
        self.type = type  # 0 for non-decision node, 1 for decision node
        pass