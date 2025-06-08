import easyocr
import pickle

from constant import FLOWCHART_NUM, OCR_DIR, IMG_DIR, ALLOWED_CHARACTERS, MIN_CONFIDENCE

reader = easyocr.Reader(['en'], gpu=True)

def extract_text_from_image(image):
    """
    Returns a list of node names extracted from the image using EasyOCR.
    """
    result = reader.readtext(image, allowlist=ALLOWED_CHARACTERS)
    extracted_texts = [text for _, text, conf in result if conf >= MIN_CONFIDENCE\
                       and text != 'y' and text != 'n']
    return extracted_texts

def generate_node_list_content(node_list):
    description = f"[OCR] Node List: {', '.join(node_list)}."
    return description

def generate_ocr_contents():
    # Generate OCR results for each flowchart image
    # and save them in a list   
    ocr_results = []
    for i in range(FLOWCHART_NUM):
        image_path = f"{IMG_DIR}/{i}.png"
        node_list = extract_text_from_image(image_path)
        print(f"Extracted node list from {image_path}: {node_list}")
        ocr_results.append(generate_node_list_content(node_list))
    # Save the OCR results to a binary file
    with open(f"{OCR_DIR}/ocr_results.pkl", "wb") as f:
        pickle.dump(ocr_results, f)

if __name__ == "__main__":
    generate_ocr_contents()
