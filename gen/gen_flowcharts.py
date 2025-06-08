import os
import subprocess
import time
import logging

from constant import *
from flowchart.builder import FlowchartBuilder
from flowchart.statistics import FlowchartStatistics

flowchart_statistics = FlowchartStatistics()

def gen_flowcharts_and_mmds(chart_num: int):
    # first check if the directories exist, if not, create them
    if not os.path.exists(MMD_DIR):
        os.makedirs(MMD_DIR)
    if not os.path.exists(IMG_DIR):
        os.makedirs(IMG_DIR)
    if not os.path.exists(PKL_DIR):
        os.makedirs(PKL_DIR)
    if not os.path.exists(STATS_DIR):
        os.makedirs(STATS_DIR)
    for i in range(chart_num):
        flowchart = FlowchartBuilder().build()
        flowchart_statistics.add_flowchart(flowchart)
        flowchart.save_mmd(os.path.join(MMD_DIR, f"{i}.mmd"))
        flowchart.save_pickle(os.path.join(PKL_DIR, f"{i}.pkl"))

def gen_imgs(chart_num: int):
    st_clk = time.time()
    cnt = 1
    # Configure logging
    logging.basicConfig(filename=f'log/flowchart-generation-{GEN_IDENTIFIER}.log', level=logging.INFO, 
                        format='%(asctime)s - %(levelname)s - %(message)s')

    for filename in os.listdir(MMD_DIR):
        if filename.endswith(".mmd"):
            input_path = os.path.join(MMD_DIR, filename)
            output_path = os.path.join(IMG_DIR, filename.replace(".mmd", ".png"))
            try:
                # Call mmdc to generate the image
                subprocess.run(["mmdc", "-i", input_path, "-o", output_path, "-s", "4", "-q"], timeout=10)
                if filename.replace(".mmd", ".png") in os.listdir(IMG_DIR):
                    logging.info(f"{cnt} images generated in {time.time() - st_clk:.2f} seconds")
                    print(f"{cnt} images generated in {time.time() - st_clk:.2f} seconds")
                    cnt += 1
                else:
                    logging.error(f"Failed to generate image for {filename}")
                    print(f"Failed to generate image for {filename}")
            except subprocess.TimeoutExpired:
                logging.error(f"Timeout expired for {filename}")
                print(f"Timeout expired for {filename}")
    logging.info(f"---Generated {cnt - 1} images successfully, {chart_num - cnt + 1} images failed---")
    print(f"---Generated {cnt - 1} images successfully, {chart_num - cnt + 1} images failed---")


def generate_flowcharts():
    gen_flowcharts_and_mmds(FLOWCHART_NUM)
    if GEN_IMGS_ON:
        gen_imgs(FLOWCHART_NUM)
    flowchart_statistics.save(os.path.join(STATS_DIR, FLOWCHART_STATS_FILE_NAME))


if __name__ == "__main__":
    generate_flowcharts()
