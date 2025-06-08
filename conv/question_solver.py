from typing import List

from utils import is_valid_transition, is_conditionally_valid_transition


class QuestionSolver:
    def __init__(self, matrix: List[List[int]]):
        """
        Initialize the question answerer with an adjacency matrix.
        :param matrix: adjacency matrix representing the flowchart
        """
        self.matrix = matrix
        self.node_num = len(matrix)

    def nextok_answer(self, cur_id: int, next_id: int) -> bool:
        """
        Check if the next state is valid from the current state.
        :param cur_id: current state ID
        :param next_id: next state ID
        :return: True if the transition is valid, False otherwise
        """
        return is_valid_transition(self.matrix, cur_id, next_id)

    def allnext_answer(self, cur_id: int) -> List[int]:
        """
        Get all possible next states from the current state.
        :param cur_id: current state ID
        :return: list of IDs of all possible next states
        """
        return [i for i in range(self.node_num) if is_valid_transition(self.matrix, cur_id, i)]

    def allprev_answer(self, cur_id: int) -> List[int]:
        """
        Get all possible previous states that can lead to the current state.
        :param cur_id: current state ID
        :return: list of IDs of all possible previous states
        """
        return [i for i in range(self.node_num) if is_valid_transition(self.matrix, i, cur_id)]

    def cond_answer(self, cur_id: int, value_id: int) -> List[int]:
        """
        Get all possible next states from the current state given a specific condition.
        :param cur_id: current state ID
        :param value_id: condition value ID
        :return: list of IDs of all possible next states that match the condition
        """
        return [i for i in range(self.node_num) if is_conditionally_valid_transition(self.matrix, cur_id, i, value_id)]

    def valid_answer(self, sequence: List[int]) -> bool:
        """
        Check if a given sequence of states is valid according to the adjacency matrix.
        :param sequence: list of state IDs representing the sequence
        :return: True if the sequence is valid, False otherwise
        """
        for i in range(len(sequence) - 1):
            if not is_valid_transition(self.matrix, sequence[i], sequence[i + 1]):
                return False
        return True
