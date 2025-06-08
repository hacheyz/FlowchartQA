from typing import Any, Dict, List


class Sample:
    def __init__(self, id_: int, image: str, conversations: List[Dict[str, str]], question_type: int, ground_truth: List[str], sequence_len: int=0):
        self.id = id_
        self.image = image
        self.conversations = conversations

        self.question_type = question_type
        self.ground_truth = ground_truth
        self.sequence_len = sequence_len

    def to_dict(self, qa_mode: bool = False) -> Dict[str, Any]:
        if qa_mode:  # used in q&a dataset
            return {
                "id": self.id,
                "image": self.image,
                "conversations": self.conversations,
                "type": self.question_type,
                "ground_truth": self.ground_truth
            }   
        return {
            "id": self.id,
            "image": self.image,
            "conversations": self.conversations
        }
