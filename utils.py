import numpy as np
import random
import os
from typing import List, Dict
import pickle

from constant import ALLOWED_CHARACTERS, MMD_DIR, PKL_DIR, IMG_DIR, IMG_REF_DIR, OCR_DIR, NONE_ANSWER
from flowchart.flowchart import Flowchart

def get_normal_random_int(mean: float, std: float, low: int, high: int) -> int:
    """Get a random integer from an Integer truncated normal distribution"""
    ret = round(np.random.normal(mean, std))
    if ret < low:
        ret = low
    elif ret > high:
        ret = high
    return ret

def gen_random_str() -> str:
    """Generate a random string with given length"""
    length = get_normal_random_int(mean=7, std=1.8, low=1, high=16)
    return ''.join(random.choices(ALLOWED_CHARACTERS, k=length))

def check_integrity(flowchart_id) -> bool:
    """check whether all the files (.mmd, .pkl, .png) are generated"""
    return os.path.exists(os.path.join(MMD_DIR, f"{flowchart_id}.mmd")) and \
           os.path.exists(os.path.join(PKL_DIR, f"{flowchart_id}.pkl")) and \
           os.path.exists(os.path.join(IMG_DIR, f"{flowchart_id}.png"))

def load_pickle(flowchart_id) -> Flowchart:
    return Flowchart.load_pickle(os.path.join(PKL_DIR, f"{flowchart_id}.pkl"))

def is_valid_transition(matrix: List[List[int]], from_id: int, to_id: int) -> bool:
    """
    Check if the transition from from_id to to_id is valid.
    
    Args:
        matrix (List[List[int]]): The adjacency matrix of the flowchart.
        from_id (int): The current node ID.
        to_id (int): The next node ID to check.
    
    Returns:
        bool: True if the transition is valid (including conditional transition),
              False otherwise.
    """
    return matrix[from_id][to_id] != 0 and to_id != from_id

def is_conditionally_valid_transition(matrix: List[List[int]], from_id: int, to_id: int, condition_id: int) -> bool:
    """
    Check if the transition from from_id to to_id is valid under a specific condition.
    
    Args:
        matrix (List[List[int]]): The adjacency matrix of the flowchart.
        from_id (int): The current node ID.
        to_id (int): The next node ID to check.
        condition_id (int): The condition ID to check against.
    
    Returns:
        bool: True if the transition is valid under the given condition,
              False otherwise.
    """
    return matrix[from_id][to_id] == condition_id and to_id != from_id

def get_img_relative_path(flowchart_id):
    return os.path.join(IMG_REF_DIR, f"{flowchart_id}.png")

_cached_ocr_results = None

def get_ocr_content(flowchart_id):
    global _cached_ocr_results
    # load OCR results from cache if not already loaded
    if _cached_ocr_results is None:
        with open(os.path.join(OCR_DIR, "ocr_results.pkl"), "rb") as f:
            _cached_ocr_results = pickle.load(f)
    return _cached_ocr_results[flowchart_id]

def conv_builder(human_text: str, gpt_text: str) -> List[Dict[str, str]]:
    """
    Combine human and GPT text into a conversation format.
    
    Args:
        human_text (str): The text from the human.
        gpt_text (str): The text from the GPT model.
    
    Returns:
        str: The formatted conversation string.
    """
    return [{"from": "human", "value": human_text},
            {"from": "gpt", "value": gpt_text}]

def simple_answer_builder(tokens: List[str]) -> str:
    """
    Build a simple answer from a list of tokens.
    
    Args:
        tokens (List[str]): The list of tokens to combine.
    
    Returns:
        str: The combined answer string.
    """
    return ', '.join(tokens) if tokens else NONE_ANSWER
