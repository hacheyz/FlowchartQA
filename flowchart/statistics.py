from constant import NORMAL_TYPE

class FlowchartStatistics:
    def __init__(self):
        self.total_num = 0
        self.type_count = {"normal": 0, "decision": 0}
        self.node_num = {}
        self.edge_num = {}
        self.edge_density = {}
        self.decision_node_num = {}

    def add_flowchart(self, flowchart):
        self.total_num += 1
        if flowchart.type == NORMAL_TYPE:
            self.type_count["normal"] += 1
        else:
            self.type_count["decision"] += 1
        
        self.node_num[flowchart.node_num] = self.node_num.get(flowchart.node_num, 0) + 1
        edge_count = len(flowchart.edges)
        self.edge_num[edge_count] = self.edge_num.get(edge_count, 0) + 1
        
        density = edge_count / flowchart.node_num if flowchart.node_num > 0 else 0
        self.edge_density[density] = self.edge_density.get(density, 0) + 1
        
        decision_nodes = sum(1 for node in flowchart.nodes if node[1] == 1)
        self.decision_node_num[decision_nodes] = self.decision_node_num.get(decision_nodes, 0) + 1

    def summary(self):
        return ("--- Flowchart Statistics ---\n"
                f"Total Flowcharts: {self.total_num}\n"
                f"Normal Flowcharts: {self.type_count['normal']} ({self.type_count['normal'] / round(self.total_num, 4):.2%})\n"
                f"Decision Flowcharts: {self.type_count['decision']} ({self.type_count['decision'] / round(self.total_num, 4):.2%})\n"
                f"Node Count Distribution: {self.node_num}\n"
                f"  Avg Node Count: {round(sum(k * v for k, v in self.node_num.items()) / self.total_num, 2)}\n"
                f"Edge Count Distribution: {self.edge_num}\n"
                f"  Avg Edge Count: {round(sum(k * v for k, v in self.edge_num.items()) / self.total_num, 2)}\n"
                f"  Avg Edge Density: {round(sum(k * v for k, v in self.edge_density.items()) / self.total_num, 2)}\n"
                f"Decision Node Count Distribution: {self.decision_node_num}\n"
                f"  Avg Decision Node Count: {round(sum(k * v for k, v in self.decision_node_num.items()) / self.type_count['decision'] if self.type_count['decision'] > 0 else 0, 2)}"
        )
    
    def save(self, file):
        with open(file, "w") as f:
            f.write(self.summary())
        f.close()
