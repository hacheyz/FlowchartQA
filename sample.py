from typing import Any, Dict, List

class Sample:
    def __init__(self, id: int, image: str, conversations: List[Dict[str, str]]):
        self.id = id
        self.image = image
        self.conversations = conversations

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "image": self.image,
            "conversations": self.conversations
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Sample':
        return Sample(data['id'], data['image'], data['conversations'])