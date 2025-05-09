gen_index = 9  # index for the data generation process

mmd_dir = f"data/{gen_index}/mmd"
pkl_dir = f"data/{gen_index}/pkl"
img_dir = f"data/{gen_index}/img"
convs_dir = f"data/{gen_index}"
qa_dir = f"data/{gen_index}"

img_placeholder = "<image>\n"

flowchart_num = 1000
gen_imgs_on = True  # whether to generate images

yes_id = 10  # yes_edge id in matrix
no_id = 11  # no_edge id in matrix

use_cot = True  # whether to use chain of thought

max_node_num = 25  # max node number in a flowchart

# a-z
allowed_characters = "abcdefghijklmnopqrstuvwxyz"

MIN_CONFIDENCE = 0.7