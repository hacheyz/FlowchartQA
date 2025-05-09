import os
import json
from typing import List, Tuple
import random
import pickle

from flowchart import Flowchart
from constant import *
from sample import Sample
from gen_flowcharts import get_normal_random_int
from sample_statistics import SampleStatistics

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

random.seed()
sampleStatistics = SampleStatistics()

# load OCR results
with open(os.path.join(convs_dir, "ocr_results.pkl"), "rb") as f:
    ocr_results = pickle.load(f)

def get_img_path(flowchart_id):
    return os.path.join("img", f"flowchart_{flowchart_id}.png")

# CoT question templates
def nextok_question(cur_state, next_state):
    return (f"{img_placeholder}Given that the current state is {cur_state}, is it possible to take state {next_state} as the next step? "
            f"Please first find all the possible next states from {cur_state}, then check if {next_state} is among them, and finally give your answer.")

def allnext_question(cur_state):
    return (f"{img_placeholder}Given that the current state is {cur_state}, what are the possible next states? "
            f"Please first list all outgoing edges from {cur_state}, explain each, and then summarize the possible next states.")

def prev_question(cur_state):
    return (f"{img_placeholder}Given that the current state is {cur_state}, what states might be the previous states? "
            f"Please first find all incoming edges to {cur_state}, explain the origin of each, and then list the possible previous states.")

def cond_question(cur_state, value):
    return (f"{img_placeholder}Given that the current state is {cur_state}, what might be the next states when the condition is {value}? "
            f"Please first list all conditional branches from {cur_state}, identify the branch where the condition is {value}, and then specify the possible next states accordingly.")

def valid_question(sequence):
    return (f"{img_placeholder}Is the sequence {sequence} a valid state sequence? "
            f"Please first check the transition between each pair of consecutive states in {sequence}, verify if each transition is valid, and then give your final answer.")

# answer methods
def nextok_answer(matrix, cur_id, next_id) -> bool:
    return matrix[cur_id][next_id] != 0

def allnext_answer(matrix, cur_id) -> List[int]:
    return [i for i in range(len(matrix[cur_id])) if matrix[cur_id][i] != 0 and i != cur_id]

def prev_answer(matrix, cur_id) -> List[int]:
    return [i for i in range(len(matrix)) if matrix[i][cur_id] != 0 and i != cur_id]

def cond_answer(matrix, cur_id, value_id) -> List[int]:
    return [i for i in range(len(matrix[cur_id])) if matrix[cur_id][i] == value_id]

def valid_answer(matrix, sequence: List[int]) -> bool:
    for i in range(len(sequence) - 1):
        if matrix[sequence[i]][sequence[i + 1]] == 0:
            return False
    return True

# CoT reasoning templates
def build_nextok_reasoning(cur_state_name: str, next_state_name: str, next_states: List[str], reachable: bool) -> str:
    # Step 1: list all possible next states
    if next_states:
        next_states_str = ', '.join(next_states)
        step1 = (f"Step 1: Find all possible next states from {cur_state_name}. "
                 f"The possible next states are {next_states_str}. ")
    else:
        step1 = (f"Step 1: Find all possible next states from {cur_state_name}. "
                 f"There are no possible next states. ")
    # Step 2: check if the next state is among them
    if reachable:
        step2 = (f"Step 2: Check if {next_state_name} is among them. "
                 f"Since {next_state_name} is in the list, the answer is yes.")
    else:
        step2 = (f"Step 2: Check if {next_state_name} is among them. "
                 f"Since {next_state_name} is NOT in the list, the answer is no.")
    return '\n'.join([step1, step2])

def build_allnext_reasoning(cur_state_name: str, next_states: List[str]) -> str:
    if next_states:
        next_states_str = ', '.join(next_states)
        step1 = (f"Step 1: Find all outgoing edges from {cur_state_name}. "
                 f"The outgoing edges point to {next_states_str}. ")

        explanations = []
        for state in next_states:
            explanations.append(f"- {cur_state_name} can transition to {state}.")
        step2 = "Step 2: Explain each outgoing edge:\n" + "\n".join(explanations) + " "

        step3 = (f"Step 3: Summarize. "
                 f"The possible next states from {cur_state_name} are {next_states_str}.")
    else:
        step1 = (f"Step 1: Find all outgoing edges from {cur_state_name}. "
                 f"There are no outgoing edges. ")
        step2 = (f"Step 2: No edges to explain. ")
        step3 = (f"Step 3: Summarize. There are no possible next states from {cur_state_name}.")

    return '\n'.join([step1, step2, step3])

def build_prev_reasoning(cur_state_name: str, prev_states: List[str]) -> str:
    if prev_states:
        prev_states_str = ', '.join(prev_states)
        step1 = (f"Step 1: Find all incoming edges to {cur_state_name}. "
                 f"The incoming edges come from {prev_states_str}. ")

        explanations = []
        for state in prev_states:
            explanations.append(f"- There is an edge from {state} to {cur_state_name}.")
        step2 = "Step 2: Explain each incoming edge:\n" + "\n".join(explanations) + " "

        step3 = (f"Step 3: Summarize. "
                 f"The possible previous states leading to {cur_state_name} are {prev_states_str}.")
    else:
        step1 = (f"Step 1: Find all incoming edges to {cur_state_name}. "
                 f"There are no incoming edges. ")
        step2 = (f"Step 2: No edges to explain. ")
        step3 = (f"Step 3: Summarize. There are no possible previous states leading to {cur_state_name}.")

    return '\n'.join([step1, step2, step3])

def build_cond_reasoning(cur_state_name: str, value: str, branches: List[Tuple[str, str]]) -> str:
    """
    branches: List of (condition_value, next_state_name)
    """
    if branches:
        all_branches_str = ', '.join([f"{cond}->{state}" for cond, state in branches])
        step1 = (f"Step 1: List all conditional branches from {cur_state_name}. "
                 f"The branches are: {all_branches_str}. ")

        matched_states = [state for cond, state in branches if cond.lower() == value.lower()]
        if matched_states:
            matched_states_str = ', '.join(matched_states)
            step2 = (f"Step 2: Identify branches where the condition is {value}. "
                     f"The matching branches lead to {matched_states_str}. ")
            step3 = (f"Step 3: Summarize. When the condition is {value}, "
                     f"the possible next states from {cur_state_name} are {matched_states_str}.")
        else:
            step2 = (f"Step 2: Identify branches where the condition is {value}. "
                     f"No branches match this condition. ")
            step3 = (f"Step 3: Summarize. When the condition is {value}, "
                     f"there are no next states from {cur_state_name}.")
    else:
        step1 = (f"Step 1: List all conditional branches from {cur_state_name}. "
                 f"There are no conditional branches. ")
        step2 = (f"Step 2: Identify branches where the condition is {value}. "
                 f"No branches exist. ")
        step3 = (f"Step 3: Summarize. No possible next states from {cur_state_name}.")

    return '\n'.join([step1, step2, step3])

def valid_answer(matrix, sequence: List[int]) -> bool:
    for i in range(len(sequence) - 1):
        if matrix[sequence[i]][sequence[i + 1]] == 0:
            return False
    return True

def build_valid_reasoning(matrix, node_data, sequence: List[int]) -> str:
    sequence_str = '->'.join([node_data[node_id].name for node_id in sequence])

    step1 = (f"Step 1: Check the transition between each pair of consecutive states in {sequence_str}. "
                f"The transitions are: ")
    transitions = []
    for i in range(len(sequence) - 1):
        transitions.append(f"{node_data[sequence[i]].name} -> {node_data[sequence[i + 1]].name}")
    step1 += ', '.join(transitions) + "."

    step2 = (f"Step 2: Verify if each transition is valid.")
    if_valid = True
    invalid_transitions = []
    for i in range(len(sequence) - 1):
        if matrix[sequence[i]][sequence[i + 1]] != 0:
            step2 += (f"\nThe transition from {node_data[sequence[i]].name} to {node_data[sequence[i + 1]].name} is valid.")
        else:
            step2 += (f"\nThe transition from {node_data[sequence[i]].name} to {node_data[sequence[i + 1]].name} is NOT valid.")
            invalid_transitions.append(f"{node_data[sequence[i]].name} -> {node_data[sequence[i + 1]].name}")
            if_valid = False
    
    if if_valid:
        step3 = (f"Step 3: Final answer. "
                 f"Since all transitions are valid, the sequence {sequence_str} is valid.")
    else:
        step3 = (f"Step 3: Final answer. "
                 f"Since transitions {', '.join(invalid_transitions)} are NOT valid, "
                 f"the sequence {sequence_str} is NOT valid.")
    
    return '\n'.join([step1, step2, step3])

# build samples
def build_nextok_samples(flowchart_id, sample_id, matrix, node_data) -> Tuple[List[Sample], int]:
    samples = []
    node_num = len(matrix)
    # nextok, yes
    cur_id = random.randint(0, node_num - 2)
    next_id = random.choice([i for i in range(node_num) if matrix[cur_id][i] != 0 and i != cur_id])
    if nextok_answer(matrix, cur_id, next_id):
        reasoning_steps = build_nextok_reasoning(
            node_data[cur_id].name,
            node_data[next_id].name,
            [node_data[i].name for i in range(node_num) if matrix[cur_id][i] != 0 and i != cur_id],
            reachable = True
        )
        samples.append(Sample(sample_id, get_img_path(flowchart_id), [
            {"from": "human", "value": nextok_question(node_data[cur_id].name, node_data[next_id].name) + " " + ocr_results[flowchart_id], "type": "1"},
            {"from": "gpt", "value": reasoning_steps, "ground_truth": ["yes"]}
        ]))
        sample_id += 1
        sampleStatistics.nextok["yes"] += 1
    # nextok, no
    cur_id = random.randint(0, node_num - 1)
    next_ids = [i for i in range(node_num) if matrix[cur_id][i] == 0 and i != cur_id]
    reasoning_steps = build_nextok_reasoning(
        node_data[cur_id].name,
        node_data[next_id].name,
        [node_data[i].name for i in range(node_num) if matrix[cur_id][i] != 0 and i != cur_id],
        reachable = False
    )
    next_id = random.choice(next_ids) if next_ids else random.randint(0, node_num - 1)
    samples.append(Sample(sample_id, get_img_path(flowchart_id), [
        {"from": "human", "value": nextok_question(node_data[cur_id].name, node_data[next_id].name) + " " + ocr_results[flowchart_id], "type": "1"},
        {"from": "gpt", "value": reasoning_steps, "ground_truth": ["no"]}
    ]))
    sample_id += 1
    sampleStatistics.nextok["no"] += 1
    return samples, sample_id

def build_all_next_samples(flowchart_id, sample_id, matrix, node_data) -> Tuple[List[Sample], int]:
    samples = []
    node_num = len(matrix)
    cur_ids = random.sample(range(node_num), 2)
    for cur_id in cur_ids:
        next_ids = allnext_answer(matrix, cur_id)
        reasoning_steps = build_allnext_reasoning(
            node_data[cur_id].name,
            [node_data[i].name for i in next_ids]
        )
        samples.append(Sample(sample_id, get_img_path(flowchart_id), [
            {"from": "human", "value": allnext_question(node_data[cur_id].name) + " " + ocr_results[flowchart_id], "type": "2"},
            {"from": "gpt", "value": reasoning_steps, "ground_truth": [node_data[i].name for i in next_ids]}
        ]))
        sample_id += 1
        sampleStatistics.allnext[len(next_ids)] += 1

    return samples, sample_id

def build_prev_samples(flowchart_id, sample_id, matrix, node_data) -> Tuple[List[Sample], int]:
    samples = []
    node_num = len(matrix)
    cur_ids = random.sample(range(1, node_num), 2)
    for cur_id in cur_ids:
        prev_ids = prev_answer(matrix, cur_id)
        reasoning_steps = build_prev_reasoning(
            node_data[cur_id].name,
            [node_data[i].name for i in prev_ids]
        )
        samples.append(Sample(sample_id, get_img_path(flowchart_id), [
            {"from": "human", "value": prev_question(node_data[cur_id].name) + " " + ocr_results[flowchart_id], "type": "3"},
            {"from": "gpt", "value": reasoning_steps, "ground_truth": [node_data[i].name for i in prev_ids]}
        ]))
        sample_id += 1
        sampleStatistics.prev[len(prev_ids)] += 1

    return samples, sample_id

def build_cond_samples(flowchart_id, sample_id, matrix, node_data) -> Tuple[List[Sample], int]:
    samples = []
    node_num = len(matrix)
    for cur_id in range(node_num):
        if node_data[cur_id].type == 1:  # decision node
            value_id = random.choice([yes_id, no_id])
            value = "true" if value_id == yes_id else "false"
            branches = []
            for i in range(node_num):
                if matrix[cur_id][i] == yes_id:
                    branches.append(("true", node_data[i].name))
                elif matrix[cur_id][i] == no_id:
                    branches.append(("false", node_data[i].name))
            reasoning_steps = build_cond_reasoning(
                node_data[cur_id].name,
                value,
                branches
            )
            next_ids = cond_answer(matrix, cur_id, value_id)
            if len(next_ids) > 0:
                samples.append(Sample(sample_id, get_img_path(flowchart_id), [
                    {"from": "human", "value": cond_question(node_data[cur_id].name, value) + " " + ocr_results[flowchart_id], "type": "4"},
                    {"from": "gpt", "value": reasoning_steps, "ground_truth": [node_data[i].name for i in next_ids]}
                ]))
                sample_id += 1
                sampleStatistics.cond += 1

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
    reasoning_steps = build_valid_reasoning(
        matrix,
        node_data,
        sequence
    )
    if len(sequence) >= 3 and valid_answer(matrix, sequence):
        samples.append(Sample(sample_id, get_img_path(flowchart_id), [
            {"from": "human", "value": valid_question("->".join([node_data[node_id].name for node_id in sequence])) + " " + ocr_results[flowchart_id], "type": "5"},
            {"from": "gpt", "value": reasoning_steps, "ground_truth": ["yes"]}
        ]))
        sample_id += 1
        sampleStatistics.valid["yes"] += 1
        sampleStatistics.valid_len[len(sequence)] += 1

    # valid, (possibly) no
    sequence = random.sample(range(node_num), get_normal_random_int(mean=3, std=0.8, low=3, high=node_num))
    if_valid = valid_answer(matrix, sequence)
    reasoning_steps = build_valid_reasoning(
        matrix,
        node_data,
        sequence
    )
    samples.append(Sample(sample_id, get_img_path(flowchart_id), [
        {"from": "human", "value": valid_question("->".join([node_data[node_id].name for node_id in sequence])) + " " + ocr_results[flowchart_id], "type": "5"},
        {"from": "gpt", "value": reasoning_steps, "ground_truth": ["no"] if if_valid else ["yes"]}
    ]))
    sample_id += 1
    if if_valid:
        sampleStatistics.valid["yes"] += 1
    else:
        sampleStatistics.valid["no"] += 1
    sampleStatistics.valid_len[len(sequence)] += 1

    return samples, sample_id

def check_integrity(flowchart_id) -> bool:
    # check whether all the files (.mmd, .pkl, .png) are generated
    return os.path.exists(os.path.join(mmd_dir, f"flowchart_{flowchart_id}.mmd")) and \
           os.path.exists(os.path.join(pkl_dir, f"flowchart_{flowchart_id}.pkl")) and \
           os.path.exists(os.path.join(img_dir, f"flowchart_{flowchart_id}.png"))

def load_pickle(flowchart_id) -> Flowchart:
    return Flowchart.load_pickle(os.path.join(pkl_dir, f"flowchart_{flowchart_id}.pkl"))

def gen_random_conversation(flowchart_id, sample_id, ocr_result: str) -> Tuple[List[Sample], int]:
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
    
    return samples, sample_id


if __name__ == "__main__":
    samples = []
    sample_id = 0
    for i in range(flowchart_num):
        result = gen_random_conversation(i, sample_id, ocr_results[i])
        if result is not None:
            samples += result[0]
            sample_id = result[1]

    with open(os.path.join(convs_dir, "conversations_answers.json"), "w") as f:
        json.dump([sample.to_dict() for sample in samples], f, indent=2)

    sampleStatistics.save(os.path.join(convs_dir, "sample_statistics.txt"))