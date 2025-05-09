import json
import pickle
import os

from constant import *

"""
    Extracts questions.jsonl and ground_truths.jsonl from conversations.json file.
    conversations.json file example:
    [
        {
            "id": 0,
            "image": "img/flowchart_0.png",
            "conversations": [
                {
                    "from": "human",
                    "value": "<image>\nGiven that the current state is xeehtd, is it possible to take state abbxsugrz as the next step? Please first find all the possible next states from xeehtd, then check if abbxsugrz is among them, and finally give your answer. [OCR] Node List: jrdbrp, dirmcy, ctinxg, xeehtd, ogdub, abbxsugrz, pwpkvopl."
                },
                {
                    "from": "gpt",
                    "value": "Step 1: Find all possible next states from xeehtd. The possible next states are abbxsugrz. \nStep 2: Check if abbxsugrz is among them. Since abbxsugrz is in the list, the answer is yes.",
                    "ground_truth": ["yes"]
                }
            ]
        },
        ...
    }

    question.jsonl file example:
    {"question_id": 0, "image": "img/flowchart_0.png", "text": "<image>\nGiven that the current state is xeehtd, is it possible to take state abbxsugrz as the next step? Please first find all the possible next states from xeehtd, then check if abbxsugrz is among them, and finally give your answer. [OCR] Node List: jrdbrp, dirmcy, ctinxg, xeehtd, ogdub, abbxsugrz, pwpkvopl."}, ...

    ground_truth.jsonl file example:
    {"question_id": 0, "ground_truth": ["yes"]},
    {"question_id": 1, "ground_truth": ["a", "b", "c"]},
    {"question_id": 2, "ground_truth": ["no"]}, ...
"""

if __name__ == "__main__":
    # Load the conversations.json file
    with open(f"{convs_dir}/conversations_answers.json", "r") as f:
        conversations = json.load(f)

    # Initialize lists to store questions and ground truths
    questions = []
    ground_truths = []

    # Iterate through each conversation
    for sample in conversations:
        image = sample["image"]
        for i, message in enumerate(sample["conversations"]):
            if message["from"] == "human":
                question_id = sample["id"]
                question = message["value"]
                # remove "<image>\n" from the question
                question = question.replace("<image>\n", "")
                question_type = message["type"]
                questions.append({
                    "question_id": question_id,
                    "image": image,
                    "text": question,
                    "type": question_type
                })
            elif message["from"] == "gpt" and "ground_truth" in message:
                ground_truth = message["ground_truth"]
                ground_truths.append({
                    "question_id": question_id,
                    "ground_truth": ground_truth
                })
                
    # Save the questions to a JSONL file
    with open(f"{qa_dir}/questions.jsonl", "w") as f:
        for q in questions:
            f.write(json.dumps(q) + "\n")

    # Save the ground truths to a JSONL file
    with open(f"{qa_dir}/ground_truths.jsonl", "w") as f:
        for gt in ground_truths:
            f.write(json.dumps(gt) + "\n")