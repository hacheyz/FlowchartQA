import datetime

date_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

mmd_dir = f"data/{date_time}/mmd"
img_dir = f"data/{date_time}/img"
pkl_dir = f"data/{date_time}/pkl"
convs_dir = "data/{date_time}"

img_placeholder = "<image>\n"

flowchart_num = 2000
gen_imgs_on = True  # whether to generate images

yes_id = 10  # yes_edge id in matrix
no_id = 11  # no_edge id in matrix

use_cot = True  # whether to use chain of thought