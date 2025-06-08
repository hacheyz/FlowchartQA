import random
import numpy as np

from gen.gen_flowcharts import generate_flowcharts
from gen.gen_ocr_contents import generate_ocr_contents
from gen.gen_conversations import gen_samples_and_qas
from constant import USE_OCR

if __name__ == "__main__":
    random.seed(42)  # Set a fixed seed for reproducibility
    np.random.seed(42)  # Set a fixed seed for reproducibility
    generate_flowcharts()
    if USE_OCR:
        generate_ocr_contents()
    gen_samples_and_qas()
