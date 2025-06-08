from abc import ABC, abstractmethod

from constant import IMG_PLACEHOLDER, NEXTOK_TYPE, ALLNEXT_TYPE, ALLPREV_TYPE, COND_TYPE, VALID_TYPE, USE_COT, USE_OCR


class QuestionBuilder(ABC):
    """
    Abstract base class for building questions based on flowchart states.
    This class defines the interface for building different types of questions.
    Subclasses should implement the methods to build specific question texts.
    """

    @abstractmethod
    def build_basic_question(self):
        raise NotImplementedError("Subclasses should implement this method.")

    @abstractmethod
    def build_cot_prompt(self):
        raise NotImplementedError("Subclasses should implement this method.")

    def build(self, ocr_content: str = "") -> str:
        """
        Build the question with optional OCR contents.
        :param ocr_content: Additional OCR contents to append to the question.
        :return: The complete question string.
        """
        question = self.build_basic_question()
        if USE_COT:
            question += " " + self.build_cot_prompt()
        if USE_OCR:
            question += " " + ocr_content
        return question


class NextOkQuestionBuilder(QuestionBuilder):
    def __init__(self, cur_state: str, next_state: str):
        self.type = NEXTOK_TYPE
        self.cur_state = cur_state
        self.next_state = next_state

    def build_basic_question(self):
        return f"{IMG_PLACEHOLDER}Given that the current state is {self.cur_state}, is it possible to take state {self.next_state} as the next step?"

    def build_cot_prompt(self):
        return f"Please first find all the possible next states from {self.cur_state}, then check if {self.next_state} is among them, and finally give your answer."


class AllNextQuestionBuilder(QuestionBuilder):
    def __init__(self, cur_state: str):
        self.type = ALLNEXT_TYPE
        self.cur_state = cur_state

    def build_basic_question(self):
        return f"{IMG_PLACEHOLDER}Given that the current state is {self.cur_state}, what are the possible next states?"

    def build_cot_prompt(self):
        return f"Please first list all outgoing edges from {self.cur_state}, explain each, and then summarize the possible next states."


class AllPrevQuestionBuilder(QuestionBuilder):
    def __init__(self, cur_state: str):
        self.type = ALLPREV_TYPE
        self.cur_state = cur_state

    def build_basic_question(self):
        return f"{IMG_PLACEHOLDER}Given that the current state is {self.cur_state}, what states might be the previous states?"

    def build_cot_prompt(self):
        return f"Please first find all incoming edges to {self.cur_state}, explain the origin of each, and then list the possible previous states."


class CondQuestionBuilder(QuestionBuilder):
    def __init__(self, cur_state: str, value: str):
        self.type = COND_TYPE
        self.cur_state = cur_state
        self.value = value

    def build_basic_question(self):
        return f"{IMG_PLACEHOLDER}Given that the current state is {self.cur_state}, what might be the next states when the condition is {self.value}?"

    def build_cot_prompt(self):
        return f"Please first list all conditional branches from {self.cur_state}, identify the branch where the condition is {self.value}, and then specify the possible next states accordingly."


class ValidQuestionBuilder(QuestionBuilder):
    def __init__(self, sequence: str):
        self.type = VALID_TYPE
        self.sequence = sequence

    def build_basic_question(self):
        return f"{IMG_PLACEHOLDER}Is the sequence {self.sequence} a valid state sequence?"

    def build_cot_prompt(self):
        return f"Please first check the transition between each pair of consecutive states in {self.sequence}, verify if each transition is valid, and then give your final answer."
