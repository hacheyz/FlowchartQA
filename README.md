<!-- filepath: /home/zhangzifan/project/data_gen/README.md -->
[English](#flowchart-qa-dataset-generator) | [中文](#流程图问答数据集生成器)

# Flowchart QA Dataset Generator

[Quick Start](#Environment-Configuration)

## Introduction

This project is designed to generate a synthetic dataset involving flowcharts and conversational question-answer pairs. The generated data can be used for training and evaluating models in areas such as visual question answering, multimodal interaction, and instruction following.
The conversations data (`conversations.json`) strictly follows the format of  [the LLaVA training data](https://github.com/haotian-liu/LLaVA/blob/main/docs/Finetune_Custom_Data.md). However, you can easily adapt it to other formats by modifying `Sample.to_dict()` method in `sample/sample.py`.

This project is completely **free of using AI-generated content**, ensuring that all generated data is synthetic and does not rely on any pre-existing datasets.

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

---

# 流程图问答数据集生成器

[快速开始](#环境配置-中文)

## 简介

本项目旨在生成一个包含流程图和对话式问答对的合成数据集。生成的数据可用于训练和评估视觉问答、多模态交互和指令遵循等领域的模型。
对话数据（`conversations.json`）严格遵循 [LLaVA 训练数据](https://github.com/haotian-liu/LLaVA/blob/main/docs/Finetune_Custom_Data.md)的格式。但是，您可以通过修改 `sample/sample.py` 文件中的 `Sample.to_dict()` 方法轻松地将其调整为其他格式。

本项目完全**不使用 AI 生成的内容**，确保所有生成的数据都是合成的，并且不依赖任何预先存在的数据集。

核心功能包括：
- 生成各种流程图结构并将其渲染为图像。
- 对生成的流程图图像执行 OCR 以提取文本内容（可选）。
- 基于流程图及其内容创建对话样本（主要由问答对组成）。

## 项目结构

项目组织成以下几个关键目录：

- `conv/`: 包含用于构建问题和答案的模块。
- `data/`: 所有生成数据的默认输出目录。它按 `GEN_IDENTIFIER` 标识的生成运行进一步组织。
  - `{GEN_IDENTIFIER}/`:
    - `img/`: 存储渲染的流程图图像 (.png)。
    - `mmd/`: 存储 Mermaid 脚本文件 (.mmd)。
    - `pkl/`: 存储序列化的 Flowchart 对象 (.pkl)。
    - `qa/`: 存储用于测试的问答对。
    - `stats/`: 存储有关生成数据的统计信息。
    - `conversations.json`: 存储用于训练的对话数据。
    - `ocr_results.pkl`: 存储 OCR 提取结果。
- `flowchart/`: 包含用于定义、构建和管理流程图对象的模块。
- `gen/`: 包含主要数据生成过程（流程图、OCR、对话）的脚本。
- `log/`: 包含数据生成过程的日志文件。
- `sample/`: 包含与对话样本构建和收集相关的模块。
- `cog.yml`: Conda 环境文件，用于依赖管理。
- `constant.py`: 包含项目的全局常量和配置设置。
- `main.py`: 运行数据生成流水线的主脚本。
- `utils.py`: 包含项目中使用的实用函数。

## 环境配置 (中文)

本项目使用 Conda 管理 Python 依赖项，这些依赖项在 `cog.yml` 文件中列出。
为了生成流程图图像，还需要 `Mermaid-CLI`。

1.  **安装 Node.js 和 npm (Mermaid-CLI 的先决条件)**:
    如果您尚未安装 Node.js 和 npm，请从 [https://nodejs.org/](https://nodejs.org/) 下载并安装。npm 是 Node 的包管理器，随 Node.js 一起提供。

2.  **创建 Conda 环境 (安装 Python 依赖项)**:
    打开终端并导航到项目的根目录。然后，运行以下命令从 `cog.yml` 文件创建一个新的 Conda 环境：
    ```bash
    conda env create -f cog.yml
    ```
    这将创建一个名为 `tool` 的环境（在 `cog.yml` 中指定）。如果您希望使用不同的名称，可以在运行命令之前修改 `cog.yml` 中的 `name` 字段，或使用：
    ```bash
    conda env create -f cog.yml -n your_env_name
    ```

3.  **激活 Conda 环境**:
    创建环境后，使用以下命令激活它：
    ```bash
    conda activate tool
    ```
    或者，如果您使用了自定义名称：
    ```bash
    conda activate your_env_name
    ```

4.  **安装 Mermaid-CLI**:
    Mermaid-CLI 用于将 `.mmd` (Mermaid 脚本) 文件转换为图像。使用 npm 全局安装它：
    ```bash
    npm install -g @mermaid-js/mermaid-cli
    ```
    验证安装：
    ```bash
    mmdc --version
    ```

## 如何运行

1.  **配置生成参数 (可选)**:
    在运行项目之前，您可能需要调整 `constant.py` 文件中的一些参数。关键参数包括：
    - `GEN_IDENTIFIER`: 一个字符串，定义当前生成运行在 `data/` 中的子目录名称。为不同的数据集更改此设置。
    - `USE_COT`: 布尔值，是否在问答生成中使用思维链推理。
    - `USE_OCR`: 布尔值，是否在问题生成中使用 OCR 结果。
    - `GEN_IMGS_ON`: 布尔值，是否生成流程图图像。
    - `FLOWCHART_NUM`: 整数，要生成的流程图数量。

2.  **运行主脚本**:
    激活环境并设置配置后，从项目的根目录运行主脚本：
    ```bash
    python main.py
    ```

## 输出

脚本将在 `data/{GEN_IDENTIFIER}/` 目录中生成数据，如“项目结构”部分所述。这包括：
- Mermaid 文件 (`.mmd`)
- 序列化的流程图对象 (`.pkl`)
- 流程图图像 (`.png`)
- OCR 结果 (`ocr_results.pkl`) (可选)
- 问答对 (`questions.jsonl`, `ground_truths.jsonl`)
- 对话数据 (`conversations.json`, `conversations_qa.json`)
- 统计文件 (`flowchart_statistics.txt`, `conversation_statistics.txt`)

`constant.py` 中的 `IMG_REF_DIR` 常量 (例如, `img`) 用于在对话中引用图像的相对路径。

## 日志

生成过程记录在 `log/` 目录中的文件中。这些日志有助于调试或跟踪生成进度。
