import random
import numpy as np
import os
import subprocess
import time
import logging
import datetime

from flowchart import Flowchart
from constant import *

def get_normal_random_int(mean: float, std: float, low: int, high: int) -> int:
    """Get a random integer from a normal distribution"""
    ret = round(np.random.normal(mean, std))
    if ret < low:
        ret = low
    elif ret > high:
        ret = high
    return ret

def gen_random_str() -> str:
    """Generate a random string with given length"""
    length = get_normal_random_int(mean=7, std=1.8, low=1, high=16)
    return ''.join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=length))

def gen_random_flowchart():
    """Generate a random flowchart"""
    type = 0 if random.random() < 0.8 else 1
    node_num = get_normal_random_int(mean=6.5, std=1, low=3, high=25)
    node_num = round(np.random.normal(6.5, 1))
    nodes, edges = [], []
    if type == 0:  # non-decision flowchart
        for i in range(node_num):
            nodes.append((f"{gen_random_str()}", 0))  # all nodes are non-decision nodes
        for i in range(node_num):
            # node i have [1, node_num - i - 1] out edges, except the last node
            forward_num = get_normal_random_int(mean=1.2, std=0.8, low=1, high=node_num - i - 1)
            if i == node_num - 1:
                forward_num = 0
            forward_nodes = random.sample(range(i + 1, node_num), forward_num)
            for forward_node in forward_nodes:
                edges.append((i, forward_node, ""))
            # node i have 15% chance to have a back edge, except the first node
            if i > 0 and random.random() < 0.15:
                back_node = random.randint(0, i - 1)
                edges.append((i, back_node, ""))
    else:
        decision_num = get_normal_random_int(mean=node_num/4, std=1, low=1, high=node_num)
        decision_nodes = random.sample(range(node_num), decision_num)
        for i in range(node_num):
            if i in decision_nodes:
                nodes.append((f"{gen_random_str()}", 1))
            else:
                nodes.append((f"{gen_random_str()}", 0))
        for i in range(node_num):
            if nodes[i][1] == 0:  # non-decision node
                forward_num = get_normal_random_int(mean=2, std=0.8, low=1, high=node_num - i - 1)
                if i == node_num - 1:
                    forward_num = 0
                out_nodes = random.sample(range(i + 1, node_num), forward_num)
                for out_node in out_nodes:
                    edges.append((i, out_node, ""))
                if i > 0 and random.random() < 0.15:
                    back_node = random.randint(0, i - 1)
                    edges.append((i, back_node, ""))
            else:  # decision node
                # for 70% chance, all out edges are forward (if valid)
                # for 10% chance, all out edges are backward (if valid)
                # for 20% chance, one forward and one backward (if valid)
                predcessor_num, successor_num = i, node_num - i - 1
                out_nodes = []
                random_num = random.random()
                if random_num < 0.8:
                    if successor_num >= 2:
                        out_nodes = random.sample(range(i + 1, node_num), 2)
                    elif successor_num == 1:
                        out_nodes = [random.choice(range(0, i)), i + 1]
                    else:
                        out_nodes = random.sample(range(0, i), 2)
                elif random_num < 0.9:
                    if predcessor_num >= 2:
                        out_nodes = random.sample(range(0, i), 2)
                    elif predcessor_num == 1:
                        out_nodes = [i - 1, random.choice(range(i + 1, node_num))]
                    else:
                        out_nodes = random.sample(range(i + 1, node_num), 2)
                else:
                    if predcessor_num >= 1 and successor_num >= 1:
                        out_nodes = [random.choice(range(0, i)), random.choice(range(i + 1, node_num))]
                    elif predcessor_num >= 2:
                        out_nodes = random.sample(range(0, i), 2)
                    else:
                        out_nodes = random.sample(range(i + 1, node_num), 2)
                edges.append((i, out_nodes[0], "Y"))
                edges.append((i, out_nodes[1], "N"))
                
    return Flowchart(type, node_num, nodes, edges)

def gen_mmds(chart_num: int):
    # first check if the directories exist, if not, create them
    if not os.path.exists(mmd_dir):
        os.makedirs(mmd_dir)
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
    if not os.path.exists(pkl_dir):
        os.makedirs(pkl_dir)
    for i in range(chart_num):
        flowchart = gen_random_flowchart()
        flowchart.save_mmd(os.path.join(mmd_dir, f"flowchart_{i}.mmd"))
        flowchart.save_pickle(os.path.join(pkl_dir, f"flowchart_{i}.pkl"))

def gen_imgs(chart_num: int):
    gen_mmds(chart_num)
    if gen_imgs_on:
        st_clk = time.time()
        cnt = 1
        # Configure logging
        logging.basicConfig(filename=f'log/flowchart-generation-{date_time}.log', level=logging.INFO, 
                            format='%(asctime)s - %(levelname)s - %(message)s')

        for filename in os.listdir(mmd_dir):
            if filename.endswith(".mmd"):
                input_path = os.path.join(mmd_dir, filename)
                output_path = os.path.join(img_dir, filename.replace(".mmd", ".png"))
                try:
                    subprocess.run(["mmdc", "-i", input_path, "-o", output_path, "-s", "4", "-q"], timeout=10)
                    if filename.replace(".mmd", ".png") in os.listdir(img_dir):
                        logging.info(f"{cnt} images generated in {time.time() - st_clk:.2f} seconds")
                        print(f"{cnt} images generated in {time.time() - st_clk:.2f} seconds")
                        cnt += 1
                    else:
                        logging.error(f"Failed to generate image for {filename}")
                        print(f"Failed to generate image for {filename}")
                except subprocess.TimeoutExpired:
                    logging.error(f"Timeout expired for {filename}")
                    print(f"Timeout expired for {filename}")
        logging.info(f"---Generated {cnt - 1} images successfully, {chart_num - cnt + 1} images failed---")
        print(f"---Generated {cnt - 1} images successfully, {chart_num - cnt + 1} images failed---")
    

if __name__ == "__main__":
    gen_imgs(flowchart_num)