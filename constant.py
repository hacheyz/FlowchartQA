"""
This file contains constants and configs used throughout the project.
"""

"""
File structure of generated data:
- data/
  - {GEN_IDENTIFIER}/  # unique id
    - mmd/  # Flowchart Mermaid scripts
    - pkl/  # Flowchart objects in pickle format
    - img/  # Flowchart images
    - qa/  # Question-Answer pairs, for testing
      - questions.jsonl
      - ground_truth.jsonl
    - conversations.json/  # Conversations for training
    - conversations_qa.json/  # Conversations for testing, with more information
    - ocr_results.pkl
    - statistics.txt  # Statistics information for flowcharts and conversations
"""

# id for the data generation process, used in directory names
GEN_IDENTIFIER = "test" # change this to a unique identifier for your generation run

USE_COT = True  # whether to use chain-of-thought reasoning in qa generation
USE_OCR = True  # whether to use OCR results in question generation
GEN_IMGS_ON = True  # whether to generate images
FLOWCHART_NUM = 5

# directories for storing generated data
MMD_DIR = f"data/{GEN_IDENTIFIER}/mmd"
PKL_DIR = f"data/{GEN_IDENTIFIER}/pkl"
IMG_DIR = f"data/{GEN_IDENTIFIER}/img"
CONVS_DIR = f"data/{GEN_IDENTIFIER}"  # conversations
OCR_DIR = f"data/{GEN_IDENTIFIER}"
QA_DIR = f"data/{GEN_IDENTIFIER}/qa"
STATS_DIR = f"data/{GEN_IDENTIFIER}/stats"

CONV_FILE_NAME = "conversations.json"
CONV_QA_FILE_NAME = "conversations_qa.json"
QUESTIONS_FILE_NAME = "questions.jsonl"
GROUND_TRUTH_FILE_NAME = "ground_truths.jsonl"
FLOWCHART_STATS_FILE_NAME = "flowchart_statistics.txt"
CONV_STATS_FILE_NAME = "conversation_statistics.txt"

IMG_REF_DIR = f"img"  # used in conversations to refer to images

# flowchart/node types
NORMAL_TYPE = 0  # normal flowchart/non-decision node
DECISION_TYPE = 1  # decision flowchart/decision node

# question types
NEXTOK_TYPE = 1
ALLNEXT_TYPE = 2
ALLPREV_TYPE = 3
COND_TYPE = 4
VALID_TYPE = 5

# used in convs generation
IMG_PLACEHOLDER = "<image>\n"

# cond ids in matrix
INVALID_ID = 0  # invalid edge id in matrix
YES_ID = 10  # yes_edge id in matrix
NO_ID = 11  # no_edge id in matrix

MAX_NODE_NUM = 25  # max node number in a flowchart

# a-z
ALLOWED_CHARACTERS = "abcdefghijklmnopqrstuvwxyz"

MIN_CONFIDENCE = 0.7

# simple answers
YES_ANSWER = "yes"
NO_ANSWER = "no"
NONE_ANSWER = "none"
