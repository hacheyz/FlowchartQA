# Flowchart QA Dataset Generator

[Quick Start](#Environment-Configuration)

## Introduction

This project is designed to generate a synthetic dataset involving flowcharts and conversational question-answer pairs. The generated data can be used for training and evaluating models in areas such as visual question answering, multimodal interaction, and instruction following.
The conversations data (`conversations.json`) strictly follows the format of  [the LLaVA training data](https://github.com/haotian-liu/LLaVA/blob/main/docs/Finetune_Custom_Data.md). However, you can easily adapt it to other formats by modifying `Sample.to_dict()` method in `sample/sample.py`.

The core functionalities include:
- Generating various flowchart structures and rendering them as images.
- Performing OCR on the generated flowchart images to extract text content (optional).
- Creating conversation samples (mainly composed of question-answer pairs) based on the flowcharts.

## Project Structure

The project is organized into several key directories:

- `conv/`: Contains modules for building questions and answers.
- `data/`: The default output directory for all generated data. It's further organized by generation runs identified by `GEN_IDENTIFIER`.
  - `{GEN_IDENTIFIER}/`:
    - `img/`: Stores rendered flowchart images (.png).
    - `mmd/`: Stores Mermaid script files for flowcharts.
    - `pkl/`: Stores pickled Flowchart objects.
    - `qa/`: Stores question-answer pairs for testing.
    - `stats/`: Stores statistics about the generated data.
    - `conversations.json`: Stores conversational data for training.
    - `ocr_results.pkl`: Stores OCR extraction results.
- `flowchart/`: Contains modules for defining, building, and managing flowchart objects.
- `gen/`: Contains scripts for the main data generation processes (flowcharts, OCR, conversations).
- `log/`: Contains log files for the data generation process.
- `sample/`: Contains modules related to conversation sample building and collecting.
- `cog.yml`: Conda environment file for dependency management.
- `constant.py`: Contains global constants and configuration settings for the project.
- `main.py`: The main script to run the data generation pipeline.
- `utils.py`: Contains utility functions used across the project.

## Environment Configuration

This project uses Conda for managing Python dependencies, which are listed in the `cog.yml` file.
For generating flowchart images, `Mermaid-CLI` is also required.

1.  **Install Node.js and npm (Prerequisite for Mermaid-CLI)**:
    If you don\'t have Node.js and npm installed, download and install them from [https://nodejs.org/](https://nodejs.org/). npm is Node\'s package manager and is included with Node.js.

2.  **Create Conda Environment (Installs Python dependencies)**:
    Open your terminal and navigate to the project\'s root directory. Then, run the following command to create a new Conda environment from the `cog.yml` file:
    ```bash
    conda env create -f cog.yml
    ```
    This will create an environment named `tool` (as specified in `cog.yml`). If you wish to use a different name, you can modify the `name` field in `cog.yml` before running the command, or use:
    ```bash
    conda env create -f cog.yml -n your_env_name
    ```

3.  **Activate Conda Environment**:
    After the environment is created, activate it using:
    ```bash
    conda activate tool
    ```
    Or, if you used a custom name:
    ```bash
    conda activate your_env_name
    ```

4.  **Install Mermaid-CLI**:
    Mermaid-CLI is used to convert `.mmd` (Mermaid script) files into images. Install it globally using npm:
    ```bash
    npm install -g @mermaid-js/mermaid-cli
    ```
    Verify the installation:
    ```bash
    mmdc --version
    ```

## How to Run

1.  **Configure Generation Parameters (Optional)**:
    Before running the project, you might want to adjust some parameters in the `constant.py` file. Key parameters include:
    - `GEN_IDENTIFIER`: A string that defines the subdirectory name within `data/` for the current generation run. Change this for different datasets.
    - `USE_COT`: Boolean, whether to use Chain-of-Thought reasoning in QA generation.
    - `USE_OCR`: Boolean, whether to use OCR results in question generation.
    - `GEN_IMGS_ON`: Boolean, whether to generate flowchart images.
    - `FLOWCHART_NUM`: Integer, the number of flowcharts to generate.

2.  **Run the Main Script**:
    Once the environment is activated and configurations are set, run the main script from the project's root directory:
    ```bash
    python main.py
    ```

## Output

The script will generate data in the `data/{GEN_IDENTIFIER}/` directory, as described in the "Project Structure" section. This includes:
- Mermaid files (`.mmd`)
- Pickled flowchart objects (`.pkl`)
- Flowchart images (`.png`)
- OCR results (`ocr_results.pkl`) (optional)
- Question-answer pairs (`questions.jsonl`, `ground_truths.jsonl`)
- Conversational data (`conversations.json`, `conversations_qa.json`)
- Statistics files (`flowchart_statistics.txt`, `conversation_statistics.txt`)

The `IMG_REF_DIR` constant in `constant.py` (e.g., `img`) is used in conversations to refer to the relative path of images.

## Logging

The generation process is logged into files within the `log/` directory. These logs can be helpful for debugging or tracking the generation progress.
