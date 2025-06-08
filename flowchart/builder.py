import random
from typing import List, Tuple

from flowchart.flowchart import Flowchart
from constant import *
from utils import get_normal_random_int, gen_random_str

class FlowchartBuilder:
    def __init__(self):
        self.type = NORMAL_TYPE if random.random() < 0.8 else DECISION_TYPE
        self.node_num = get_normal_random_int(mean=6.5, std=1, low=3, high=MAX_NODE_NUM)
        self.edges = []
        self.nodes = []

    def build(self) -> Flowchart:
        """Build a flowchart with given type and node number"""
        if self.type == NORMAL_TYPE:
            self.build_normal_flowchart()
        else:
            self.build_decision_flowchart()
        return Flowchart(self.type, self.node_num, self.nodes, self.edges)

    @staticmethod
    def gen_node(node_type: int) -> Tuple[str, int]:
        """Generate a random node with given type (0 for non-decision, 1 for decision)"""
        return gen_random_str(), node_type
    
    @staticmethod
    def gen_edges_for_normal_node(node_id: int, node_num: int) -> List[Tuple[int, int, str]]:
        """Generate edges for a normal node with given id and total node number"""
        edges = []
        # node i have [1, node_num - i - 1] out edges, except the last node
        forward_num = get_normal_random_int(mean=1.2, std=0.8, low=1, high=node_num - node_id - 1)
        if node_id == node_num - 1:
            forward_num = 0
        forward_nodes = random.sample(range(node_id + 1, node_num), forward_num)
        for forward_node in forward_nodes:
            edges.append((node_id, forward_node, ""))
        # node i have 15% chance to have a back edge, except the first node
        if node_id > 0 and random.random() < 0.15:
            back_node = random.randint(0, node_id - 1)
            edges.append((node_id, back_node, ""))
        return edges
    
    @staticmethod
    def gen_edges_for_decision_node(node_id: int, node_num: int) -> List[Tuple[int, int, str]]:
        """
        A decision node has two out edges:
        for 70% chance, all out edges are forward (if valid)
        for 10% chance, all out edges are backward (if valid)
        for 20% chance, one forward and one backward
        """
        edges = []
        predecessor_num, successor_num = node_id, node_num - node_id - 1
        random_num = random.random()
        if random_num < 0.7:
            if successor_num >= 2:
                out_nodes = random.sample(range(node_id + 1, node_num), 2)
            elif successor_num == 1:
                out_nodes = [random.choice(range(0, node_id)), node_id + 1]
            else:
                out_nodes = random.sample(range(0, node_id), 2)
        elif random_num < 0.8:
            if predecessor_num >= 2:
                out_nodes = random.sample(range(0, node_id), 2)
            elif predecessor_num == 1:
                out_nodes = [node_id - 1, random.choice(range(node_id + 1, node_num))]
            else:
                out_nodes = random.sample(range(node_id + 1, node_num), 2)
        else:
            if predecessor_num >= 1 and successor_num >= 1:
                out_nodes = [random.choice(range(0, node_id)), random.choice(range(node_id + 1, node_num))]
            elif predecessor_num >= 2:
                out_nodes = random.sample(range(0, node_id), 2)
            else:
                out_nodes = random.sample(range(node_id + 1, node_num), 2)
        edges.append((node_id, out_nodes[0], "Y"))
        edges.append((node_id, out_nodes[1], "N"))
        return edges
    
    def build_normal_flowchart(self):
        """Generate a random normal flowchart with given node number"""
        for i in range(self.node_num):
            self.nodes.append(self.gen_node(0))  # all nodes are non-decision nodes
        for i in range(self.node_num):
            self.edges.extend(self.gen_edges_for_normal_node(i, self.node_num))
    
    def build_decision_flowchart(self):
        """Generate a random decision flowchart with given node number"""
        decision_num = get_normal_random_int(mean=self.node_num/4, std=1, low=1, high=self.node_num)
        decision_nodes = random.sample(range(self.node_num), decision_num)
        for i in range(self.node_num):
            if i in decision_nodes:
                self.nodes.append(self.gen_node(1))
            else:
                self.nodes.append(self.gen_node(0))
        for i in range(self.node_num):
            if self.nodes[i][1] == NORMAL_TYPE:  # non-decision node
                self.edges.extend(self.gen_edges_for_normal_node(i, self.node_num))
            else:  # decision node
                self.edges.extend(self.gen_edges_for_decision_node(i, self.node_num))
