import os
import json
from typing import List, Tuple
import random

from flowchart import Flowchart
from constant import *
from sample import Sample
from gen_flowcharts import get_normal_random_int

"""
Sample metadata should contain id (a unique identifier), image (the path to the image), and conversations (the conversation data between human and AI).

A sample JSON for finetuning LLaVA for generating tag-style captions for Stable Diffusion:

```[
  {
    "id": "997bb945-628d-4724-b370-b84de974a19f",
    "image": "part-000001/997bb945-628d-4724-b370-b84de974a19f.jpg",
    "conversations": [
      {
        "from": "human",
        "value": "<image>\nWrite a prompt for Stable Diffusion to generate this image."
      },
      {
        "from": "gpt",
        "value": "a beautiful painting of chernobyl by nekro, pascal blanche, john harris, greg rutkowski, sin jong hun, moebius, simon stalenhag. in style of cg art. ray tracing. cel shading. hyper detailed. realistic. ue 5. maya. octane render. "
      },
    ]
  },
  ...
]
```

We will generate a large amount of data about Flowchart Q&A. Possible questions include:
 1. Given that the current state is {X}, is it possible to take action {Y} as the next step?
 2. Given that the current state is {X}, what are the possible next states?
 3. Give that the current state is {Y}, what states might be the previous states?
 4. Give that the current state is {X}, what might be the next states when the condition is {true/false}?
 5. Is the sequence {X}->{Y}->{Z} a valid action sequence?
"""

def get_img_path(flowchart_id):
    return os.path.join("img", f"flowchart_{flowchart_id}.png")

# question templates
def nextok_question(cur_state, next_state):
    return f"{img_placeholder}Given that the current state is {cur_state}, is it possible to take state {next_state} as the next step?"

def allnext_question(cur_state):
    return f"{img_placeholder}Given that the current state is {cur_state}, what are the possible next states?"

def prev_question(cur_state):
    return f"{img_placeholder}Given that the current state is {cur_state}, what states might be the previous states?"

def cond_question(cur_state, value):
    return f"{img_placeholder}Given that the current state is {cur_state}, what might be the next states when the condition is {value}?"

def valid_question(sequence):
    return f"{img_placeholder}Is the sequence {sequence} a valid state sequence?"

# answer methods
def nextok_answer(matrix, cur_id, next_id) -> bool:
    return matrix[cur_id][next_id] == 1

def allnext_answer(matrix, cur_id) -> List[int]:
    return [i for i in range(len(matrix[cur_id])) if matrix[cur_id][i] == 1]

def prev_answer(matrix, cur_id) -> List[int]:
    return [i for i in range(len(matrix)) if matrix[i][cur_id] == 1]

def cond_answer(matrix, cur_id, value_id) -> List[int]:
    return [i for i in range(len(matrix[cur_id])) if matrix[cur_id][i] == value_id]

def valid_answer(matrix, sequence: List[int]) -> bool:
    for i in range(len(sequence) - 1):
        if matrix[sequence[i]][sequence[i + 1]] == 0:
            return False
    return True

# build samples
def build_nextok_samples(flowchart_id, sample_id, matrix, node_data) -> Tuple[List[Sample], int]:
    samples = []
    node_num = len(matrix)
    # nextok, yes
    cur_id = random.randint(0, node_num - 2)
    next_id = random.choice([i for i in range(node_num) if matrix[cur_id][i] != 0 and i != cur_id])
    if nextok_answer(matrix, cur_id, next_id):
        samples.append(Sample(sample_id, get_img_path(flowchart_id), [
            {"from": "human", "value": nextok_question(node_data[cur_id].name, node_data[next_id].name)},
            {"from": "gpt", "value": "yes"}
        ]))
        sample_id += 1
    # nextok, no
    cur_id = random.randint(0, node_num - 1)
    next_ids = [i for i in range(node_num) if matrix[cur_id][i] == 0 and i != cur_id]
    if len(next_ids) > 0:
        next_id = random.choice(next_ids)
        if not nextok_answer(matrix, cur_id, next_id):
            samples.append(Sample(sample_id, get_img_path(flowchart_id), [
                {"from": "human", "value": nextok_question(node_data[cur_id].name, node_data[next_id].name)},
                {"from": "gpt", "value": "no"}
            ]))
            sample_id += 1
    return samples, sample_id

def build_all_next_samples(flowchart_id, sample_id, matrix, node_data) -> Tuple[List[Sample], int]:
    samples = []
    node_num = len(matrix)
    cur_ids = random.sample(range(node_num - 1), 2)
    for cur_id in cur_ids:
        next_ids = allnext_answer(matrix, cur_id)
        samples.append(Sample(sample_id, get_img_path(flowchart_id), [
            {"from": "human", "value": allnext_question(node_data[cur_id].name)},
            {"from": "gpt", "value": ", ".join([node_data[next_id].name for next_id in next_ids])}
        ]))
        sample_id += 1
    return samples, sample_id

def build_prev_samples(flowchart_id, sample_id, matrix, node_data) -> Tuple[List[Sample], int]:
    samples = []
    node_num = len(matrix)
    cur_ids = random.sample(range(1, node_num), 2)
    for cur_id in cur_ids:
        prev_ids = prev_answer(matrix, cur_id)
        samples.append(Sample(sample_id, get_img_path(flowchart_id), [
            {"from": "human", "value": prev_question(node_data[cur_id].name)},
            {"from": "gpt", "value": ", ".join([node_data[prev_id].name for prev_id in prev_ids])}
        ]))
        sample_id += 1
    return samples, sample_id

def build_cond_samples(flowchart_id, sample_id, matrix, node_data) -> Tuple[List[Sample], int]:
    samples = []
    node_num = len(matrix)
    for cur_id in range(node_num):
        if node_data[cur_id].type == 1:  # decision node
            value_id = random.choice([yes_id, no_id])
            value = "true" if value_id == yes_id else "false"
            next_ids = cond_answer(matrix, cur_id, value_id)
            if len(next_ids) > 0:
                samples.append(Sample(sample_id, get_img_path(flowchart_id), [
                    {"from": "human", "value": cond_question(node_data[cur_id].name, value)},
                    {"from": "gpt", "value": ", ".join([node_data[next_id].name for next_id in next_ids])}
                ]))
                sample_id += 1
    return samples, sample_id

def build_valid_samples(flowchart_id, sample_id, matrix, node_data) -> Tuple[List[Sample], int]:
    samples = []
    node_num = len(matrix)
    # valid, yes
    cur_id = random.choice(range(0, node_num//2))
    sequence = [cur_id]
    stop_prob = 0.1
    while random.random() > stop_prob or len(sequence) < 3:
        next_ids = [i for i in range(node_num) if matrix[cur_id][i] != 0 and i not in sequence]
        if len(next_ids) != 0:
            next_id = random.choice(next_ids)
            sequence.append(next_id)
            cur_id = next_id
            stop_prob *= 1.6
        else:
            break
    if len(sequence) >= 3 and valid_answer(matrix, sequence):
        samples.append(Sample(sample_id, get_img_path(flowchart_id), [
            {"from": "human", "value": valid_question("->".join([node_data[node_id].name for node_id in sequence]))},
            {"from": "gpt", "value": "yes"}
        ]))
        sample_id += 1

    # valid, (possibly) no
    sequence = random.sample(range(node_num), get_normal_random_int(mean=3, std=0.8, low=3, high=node_num))
    if_valid = valid_answer(matrix, sequence)
    answer = "yes" if if_valid else "no"
    samples.append(Sample(sample_id, get_img_path(flowchart_id), [
        {"from": "human", "value": valid_question("->".join([node_data[node_id].name for node_id in sequence]))},
        {"from": "gpt", "value": answer}
    ]))

    return samples, sample_id

def check_integrity(flowchart_id) -> bool:
    # check whether all the files (.mmd, .pkl, .png) are generated
    return os.path.exists(os.path.join(mmd_dir, f"flowchart_{flowchart_id}.mmd")) and \
           os.path.exists(os.path.join(pkl_dir, f"flowchart_{flowchart_id}.pkl")) and \
           os.path.exists(os.path.join(img_dir, f"flowchart_{flowchart_id}.png"))

def load_pickle(flowchart_id) -> Flowchart:
    return Flowchart.load_pickle(os.path.join(pkl_dir, f"flowchart_{flowchart_id}.pkl"))

def gen_random_conversation(flowchart_id, sample_id) -> Tuple[List[Sample], int]:
    # Return List of generated Samples and next sample_id
    if not check_integrity(flowchart_id):
        return None
    flowchart = load_pickle(flowchart_id)
    matrix = flowchart.to_matrix()
    node_data = flowchart.build_node_data()
    node_num = flowchart.node_num
    # generate 2 questions for each type, except for "cond"
    # for "yes/no" questions (nextok, valid), we generate 2 questions with answer "yes" and "(possibly) no" respectively

    samples = []
    # nextok
    nextok_samples, sample_id = build_nextok_samples(flowchart_id, sample_id, matrix, node_data)
    samples += nextok_samples
    # allnext
    allnext_samples, sample_id = build_all_next_samples(flowchart_id, sample_id, matrix, node_data)
    samples += allnext_samples
    # prev
    prev_samples, sample_id = build_prev_samples(flowchart_id, sample_id, matrix, node_data)
    samples += prev_samples
    # valid
    valid_samples, sample_id = build_valid_samples(flowchart_id, sample_id, matrix, node_data)
    samples += valid_samples
    # cond
    if flowchart.type == 1:  
        cond_samples, sample_id = build_cond_samples(flowchart_id, sample_id, matrix, node_data)
        samples += cond_samples
    
    sample_id += 1
    return samples, sample_id


if __name__ == "__main__":
    samples = []
    sample_id = 0
    for i in range(flowchart_num):
        result = gen_random_conversation(i, sample_id)
        if result is not None:
            samples += result[0]
            sample_id = result[1]

    with open(os.path.join(convs_dir, "llava_v1_5_flowchart_v2.json"), "w") as f:
        json.dump([sample.to_dict() for sample in samples], f, indent=2)
