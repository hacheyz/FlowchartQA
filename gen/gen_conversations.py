import os
import json

from sample.builder import SampleBuilder
from sample.collector import SampleCollector
from sample.statistics import SampleStatistics
from constant import FLOWCHART_NUM, CONVS_DIR, QA_DIR, CONV_FILE_NAME, CONV_QA_FILE_NAME, \
    QUESTIONS_FILE_NAME, GROUND_TRUTH_FILE_NAME, STATS_DIR, CONV_STATS_FILE_NAME

conv_statistics = SampleStatistics()

def gen_samples():
    """
    Generate samples from flowchart original data.
    """
    if not os.path.exists(QA_DIR):
        os.makedirs(QA_DIR)
    if not os.path.exists(STATS_DIR):
        os.makedirs(STATS_DIR)
    sample_collector = SampleCollector()
    for i in range(FLOWCHART_NUM):
        sample_builder = SampleBuilder(i, sample_collector.get_id())
        new_sample_collector = sample_builder.build_samples_for_flowchart()
        for sample in new_sample_collector.get_samples():
            conv_statistics.add_sample(sample)
        sample_collector.extend(new_sample_collector.get_samples())

    with open(os.path.join(CONVS_DIR, CONV_FILE_NAME), "w") as f:
        json.dump([sample.to_dict(qa_mode=False) for sample in sample_collector.get_samples()], f, indent=2)
    with open(os.path.join(QA_DIR, CONV_QA_FILE_NAME), "w") as f:
        json.dump([sample.to_dict(qa_mode=True) for sample in sample_collector.get_samples()], f, indent=2)

def gen_qas():
    """
    Generate question-answer pairs from file.
    """
    with open(os.path.join(QA_DIR, CONV_QA_FILE_NAME), "r") as f:
        samples = json.load(f)
    questions = []
    ground_truths = []
    for sample in samples:
        question_id = sample["id"]
        image = sample["image"]
        conversations = sample["conversations"]
        question_type = sample["type"]
        ground_truth = sample["ground_truth"]
        for i, message in enumerate(conversations):
            if message["from"] == "human":
                question_id = question_id
                # remove "<image>\n" from the question
                question_text = message["value"].replace("<image>\n", "")
                question_type = question_type
                questions.append({
                    "question_id": question_id,
                    "image": image,
                    "text": question_text,
                    "type": question_type
                })
        ground_truths.append({
            "question_id": question_id,
            "ground_truth": ground_truth
        })

    with open(os.path.join(QA_DIR, QUESTIONS_FILE_NAME), "w") as f:
        for q in questions:
            f.write(json.dumps(q) + "\n")

    with open(os.path.join(QA_DIR, GROUND_TRUTH_FILE_NAME), "w") as f:
        for gt in ground_truths:
            f.write(json.dumps(gt) + "\n")

def gen_samples_and_qas():
    gen_samples()
    gen_qas()
    conv_statistics.save(os.path.join(STATS_DIR, CONV_STATS_FILE_NAME))

if __name__ == "__main__":
    gen_samples_and_qas()
