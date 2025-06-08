import random

from sample.sample import Sample
from conv.question_builder import NextOkQuestionBuilder, AllNextQuestionBuilder, AllPrevQuestionBuilder, \
    CondQuestionBuilder, ValidQuestionBuilder
from conv.question_solver import QuestionSolver
from conv.inference_builder import InferenceBuilder
from utils import check_integrity, load_pickle, is_valid_transition, is_conditionally_valid_transition, \
    get_img_relative_path, get_ocr_content, conv_builder, simple_answer_builder, get_normal_random_int
from constant import USE_COT, USE_OCR, YES_ANSWER, NO_ANSWER, YES_ID, NO_ID, DECISION_TYPE, \
    NEXTOK_TYPE, ALLNEXT_TYPE, ALLPREV_TYPE, COND_TYPE, VALID_TYPE
from sample.collector import SampleCollector

class SampleBuilder:
    """
    SampleBuilder is responsible for building samples for a given flowchart.
    """
    def __init__(self, flowchart_id: int, base_id: int):
        self.flowchart_id = flowchart_id
        if not check_integrity(self.flowchart_id):
            raise ValueError(f"Invalid flowchart ID: {self.flowchart_id}")
        self.sample_collector = SampleCollector(base_id=base_id)
        self.flowchart = load_pickle(self.flowchart_id)
        self.matrix = self.flowchart.build_matrix()
        self.node_num = len(self.matrix)
        self.node_data = self.flowchart.build_node_data()
        self.question_solver = QuestionSolver(self.matrix)
        self.ocr_content = get_ocr_content(self.flowchart_id) if USE_OCR else ""

    def build_samples_for_flowchart(self):
        self.build_nextok_samples()
        self.build_allnext_samples()
        self.build_allprev_samples()
        self.build_valid_samples()
        if self.flowchart.type == DECISION_TYPE:
            self.build_cond_samples()
        return self.sample_collector

    def build_nextok_samples(self):
        # nextok, yes
        cur_id = random.randint(0, self.node_num - 2)
        next_id = random.choice([i for i in range(self.node_num) if is_valid_transition(self.matrix, cur_id, i)])
        if self.question_solver.nextok_answer(cur_id, next_id):
            cur_state = self.node_data[cur_id].name
            next_state = self.node_data[next_id].name
            all_next_states = [self.node_data[i].name for i in range(self.node_num) if is_valid_transition(self.matrix, cur_id, i)]
            answer = InferenceBuilder.build_nextok_inference(cur_state, next_state, all_next_states, reachable=True) \
                if USE_COT else YES_ANSWER
            question_builder = NextOkQuestionBuilder(cur_state, next_state)
            sample = Sample(
                id_=self.sample_collector.get_id(),
                image=get_img_relative_path(self.flowchart_id),
                conversations=conv_builder(question_builder.build(self.ocr_content), answer),
                question_type=NEXTOK_TYPE,
                ground_truth=[YES_ANSWER]
            )
            self.sample_collector.append(sample)
        # nextok, no
        cur_id = random.randint(0, self.node_num - 1)
        next_ids = [i for i in range(self.node_num) if i != cur_id and not is_valid_transition(self.matrix, cur_id, i)]
        next_id = random.choice(next_ids) if next_ids else random.randint(0, self.node_num - 1)
        if not self.question_solver.nextok_answer(cur_id, next_id):
            cur_state = self.node_data[cur_id].name
            next_state = self.node_data[next_id].name
            all_next_states = [self.node_data[i].name for i in range(self.node_num) if is_valid_transition(self.matrix, cur_id, i)]
            answer = InferenceBuilder.build_nextok_inference(cur_state, next_state, all_next_states, reachable=False) \
                if USE_COT else NO_ANSWER
            question_builder = NextOkQuestionBuilder(cur_state, next_state)
            sample = Sample(
                id_=self.sample_collector.get_id(),
                image=get_img_relative_path(self.flowchart_id),
                conversations=conv_builder(question_builder.build(self.ocr_content), answer),
                question_type=NEXTOK_TYPE,
                ground_truth=[NO_ANSWER]
            )
            self.sample_collector.append(sample)
        
    def build_allnext_samples(self):
        cur_ids = random.sample(range(self.node_num), 2)
        for cur_id in cur_ids:
            cur_state = self.node_data[cur_id].name
            next_ids = self.question_solver.allnext_answer(cur_id)
            next_states = [self.node_data[i].name for i in next_ids]
            answer = InferenceBuilder.build_allnext_inference(cur_state, next_states) \
                if USE_COT else simple_answer_builder(next_states)
            question_builder = AllNextQuestionBuilder(cur_state)
            sample = Sample(
                id_=self.sample_collector.get_id(),
                image=get_img_relative_path(self.flowchart_id),
                conversations=conv_builder(question_builder.build(self.ocr_content), answer),
                question_type=ALLNEXT_TYPE,
                ground_truth=next_states
            )
            self.sample_collector.append(sample)

    def build_allprev_samples(self):
        cur_ids = random.sample(range(1, self.node_num), 2)
        for cur_id in cur_ids:
            cur_state = self.node_data[cur_id].name
            prev_ids = self.question_solver.allprev_answer(cur_id)
            prev_states = [self.node_data[i].name for i in prev_ids]
            answer = InferenceBuilder.build_allprev_inference(cur_state, prev_states) \
                if USE_COT else simple_answer_builder(prev_states)
            question_builder = AllPrevQuestionBuilder(cur_state)
            sample = Sample(
                id_=self.sample_collector.get_id(),
                image=get_img_relative_path(self.flowchart_id),
                conversations=conv_builder(question_builder.build(self.ocr_content), answer),
                question_type=ALLPREV_TYPE,
                ground_truth=prev_states
            )
            self.sample_collector.append(sample)

    def build_cond_samples(self):
        for cur_id in range(self.node_num):
            if self.node_data[cur_id].type == DECISION_TYPE:
                cur_state = self.node_data[cur_id].name
                value_id = random.choice([YES_ID, NO_ID])
                value = "true" if value_id == YES_ID else "false"
                branches = []
                for i in range(self.node_num):
                    if is_conditionally_valid_transition(self.matrix, cur_id, i, YES_ID):
                        branches.append(("true", self.node_data[i].name))
                    elif is_conditionally_valid_transition(self.matrix, cur_id, i, NO_ID):
                        branches.append(("false", self.node_data[i].name))
                cond_ids = self.question_solver.cond_answer(cur_id, value_id)
                cond_states = [self.node_data[i].name for i in cond_ids]
                answer = InferenceBuilder.build_cond_inference(cur_state, value, branches) \
                    if USE_COT else simple_answer_builder(cond_states)
                question_builder = CondQuestionBuilder(cur_state, value)
                sample = Sample(
                    id_=self.sample_collector.get_id(),
                    image=get_img_relative_path(self.flowchart_id),
                    conversations=conv_builder(question_builder.build(self.ocr_content), answer),
                    question_type=COND_TYPE,
                    ground_truth=cond_states
                )
                self.sample_collector.append(sample)

    def build_valid_samples(self):
        # valid, yes
        cur_id = random.choice(range(0, self.node_num//2))
        sequence = [cur_id]
        stop_prob = 0.1
        while random.random() > stop_prob or len(sequence) < 3:
            next_ids = [i for i in range(self.node_num) if is_valid_transition(self.matrix, cur_id, i) and i not in sequence]
            if len(next_ids) != 0:
                next_id = random.choice(next_ids)
                sequence.append(next_id)
                cur_id = next_id
                stop_prob *= 1.6
            else:
                break
        if len(sequence) >= 3 and self.question_solver.valid_answer(sequence):
            sequence_states = [self.node_data[node_id].name for node_id in sequence]
            answer = InferenceBuilder.build_valid_reasoning(self.matrix, self.node_data, sequence) \
                if USE_COT else YES_ANSWER
            question_builder = ValidQuestionBuilder("->".join(sequence_states))
            sample = Sample(
                id_=self.sample_collector.get_id(),
                image=get_img_relative_path(self.flowchart_id),
                conversations=conv_builder(question_builder.build(self.ocr_content), answer),
                question_type=VALID_TYPE,
                ground_truth=[YES_ANSWER],
                sequence_len=len(sequence)
            )
            self.sample_collector.append(sample)
        # valid, (possibly) no
        sequence = random.sample(range(self.node_num), get_normal_random_int(mean=3, std=0.8, low=3, high=self.node_num))
        is_valid = self.question_solver.valid_answer(sequence)
        sequence_states = [self.node_data[node_id].name for node_id in sequence]
        answer = InferenceBuilder.build_valid_reasoning(self.matrix, self.node_data, sequence) \
            if USE_COT else NO_ANSWER
        question_builder = ValidQuestionBuilder("->".join(sequence_states))
        sample = Sample(
            id_=self.sample_collector.get_id(),
            image=get_img_relative_path(self.flowchart_id),
            conversations=conv_builder(question_builder.build(self.ocr_content), answer),
            question_type=VALID_TYPE,
            ground_truth=[NO_ANSWER] if not is_valid else [YES_ANSWER],
            sequence_len=len(sequence)
        )
        self.sample_collector.append(sample)
