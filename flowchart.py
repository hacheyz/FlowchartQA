import random
from typing import List, Tuple
import mermaid as md
from mermaid import Graph
import pickle

from node import Node
from constant import yes_id, no_id

class Flowchart:
    def __init__(self, type: int, node_num: int, nodes: List[Tuple[str, int]], edges: List[Tuple[int, int, str]]):
        self.type = type
        self.node_num = node_num
        self.nodes = nodes
        self.edges = edges

    def __str__(self):
        return f"Flowchart(type={self.type},\n node_num={self.node_num},\n nodes={self.nodes},\n edges={self.edges})"
    
    def __repr__(self):
        return self.__str__()
    
    def build_node_data(self) -> List[Node]:
        """Build node data list of all nodes"""
        node_data = []
        for i in range(self.node_num):
            node = self.nodes[i]
            node_data.append(Node(i, chr(ord('A') + i), node[0], node[1]))
        return node_data
    
    @staticmethod 
    def edge_to_str(edge: Tuple[int, int, str], node_data: List[Node]) -> str:
        """Convert an edge to a string"""
        first_id, second_id, condition = edge
        first, second = node_data[first_id], node_data[second_id]
        ret = f"\t{first.code}"
        if first.type == 0:  # non-decision node
            ret += f"({first.name})"
        else:  # decision node
            ret += f"{{{first.name}}}"
        if condition != "":
            ret += f"-- {condition} -->{second.code}"
        else:
            ret += f"-->{second.code}"
        if second.type == 0:
            ret += f"({second.name})"
        else:
            ret += f"{{{second.name}}}"
        return ret
    
    def to_matrix(self) -> List[List[int]]:
        """Convert the flowchart to an adjacency matrix"""
        matrix = [[0 for _ in range(self.node_num)] for _ in range(self.node_num)]
        if self.type == 0:  # non-decision flowchart
            for edge in self.edges:
                matrix[edge[0]][edge[1]] = 1
        else:  # decision flowchart
            for edge in self.edges:
                if edge[2] == "":
                    matrix[edge[0]][edge[1]] = 1
                elif edge[2] == "Y":
                    matrix[edge[0]][edge[1]] = yes_id
                else:
                    matrix[edge[0]][edge[1]] = no_id
        return matrix
    
    def to_mmd(self) -> str:
        """Generate mermaid script of this flowchart"""
        # 70% LR, 30% TB
        direction = "LR" if random.random() < 0.7 else "TB"
        mmd = f"flowchart {direction}\n"
        node_data = self.build_node_data()
        # the code of each node is assigned with "A", "B", "C", ..., !!!do not use more than 26 nodes!!!
        for edge in self.edges:
            mmd += Flowchart.edge_to_str(edge, node_data) + "\n"
        return mmd
    
    def save_mmd(self, filename: str):
        """Save mermaid script to a file"""
        with open(filename, "w") as f:
            f.write(self.to_mmd())

    def save_pickle(self, filename: str):
        """Save the flowchart to a pickle file"""
        with open(filename, "wb") as f:
            pickle.dump(self, f)

    @staticmethod
    def load_pickle(filename: str):
        """Load the flowchart from a pickle file"""
        with open(filename, "rb") as f:
            return pickle.load(f)

    def show(self):
        """Render the flowchart"""
        g = Graph("", self.to_mmd())
        render = md.Mermaid(g)
        return render
