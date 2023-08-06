# Given a image pairs (loop closures), estimate R & t
"""
    Takes the loop_pairs file, data source, and algorithm pipeline
    as arguments and saves the transformations in a single file.
"""

# %%
import os
import sys
from pathlib import Path
# Set the './../' from the script folder
dir_name = None
try:
    dir_name = os.path.dirname(os.path.realpath(__file__))
except NameError:
    print('WARN: __file__ not found, trying local')
    dir_name = os.path.abspath('')
lib_path = os.path.realpath(f'{Path(dir_name).parent}')
# Add to path
if lib_path not in sys.path:
    print(f'Adding library path: {lib_path} to PYTHONPATH')
    sys.path.append(lib_path)
else:
    print(f'Library path {lib_path} already in PYTHONPATH')


# %%
import numpy as np
import tyro
from dataclasses import dataclass
import traceback
import time
from typing import Literal
import pandas as pd
from scipy.spatial.transform import Rotation as R
from PIL import Image
from LFM.utilities import pd_row_to_tf, get_pcd_from_dimg, \
    pts_img_to_o3dpc, tf_agent_camera
import matplotlib.pyplot as plt
import einops as ein
import open3d as o3d
from copy import deepcopy


# %%
@dataclass
class LocalArgs:
    # Root folder where the datasets are stored
    ds_dir: Path = "/scratch/avneesh.mishra/divloc/lc"
    # Name of dataset segment in the root dataset folder
    ds_name: str = "qsmall"
    # Loop pair filename
    lp_fname: str = "qsmall_LP.txt1"


# %%
def parse_lc_file(largs: LocalArgs, sort: bool=True):
    """
        Parse the file containing loop closure pairs and return the
        data as dict with keys (all str type):
        - frame_freq:   Frame frequency (int)
        - glob_thresh:  Global threshold (float)
        - ts:           Ignore this (float)
        - naive_lp:     Naive loop pairs (np.ndarray, float64, 
                        shape: [N1, 3]). Each row is [i, j, score]
        - seqs_lp:      Sequence loop pairs (np.ndarray, float64,
                        shape: [N2, 3]). Each row is [i, j, score]
        
        The 'i' and 'j' are poses (frames). If the 'frame_freq' is 4
        (example), then 'i = 0' means '1.jpg', 'i = 1' means '5.jpg',
        and so on (same for 'j').
        
        Parameters:
        - largs:        Local program arguments (for paths)
        - sort:         If True, the loop pairs are sorted by score
                        in the ascending order
    """
    fn = f"{largs.ds_dir}/{largs.ds_name}/loop_pairs/{largs.lp_fname}"
    assert os.path.isfile(fn), "Loop pair file doesn't exist"
    # Read all lines
    lines = open(fn).readlines()
    frame_freq = int(lines[0].split()[-1])
    glob_thresh = float(lines[1].split()[-1])
    ts = float(lines[2].split()[-1])
    # Naive loop pairs
    naive_loop_pairs = []   # [i, j, global_desc_sim]
    i_break = 4
    for line in lines[4:]:
        if line.startswith("seqs_based_loop_pairs"):
            break
        else:
            i_break += 1
        naive_loop_pairs.append(list(map(float, line.split())))
    naive_loop_pairs = np.array(naive_loop_pairs, dtype=np.float64)
    if sort:
        naive_loop_pairs = naive_loop_pairs[np.argsort(
                naive_loop_pairs[:,-1])]
    # Sequence based loop pairs
    seqs_loop_pairs = []    # [i, j, global_desc_sim]
    for line in lines[i_break+1:]:
        seqs_loop_pairs.append(list(map(float, line.split())))
    seqs_loop_pairs = np.array(seqs_loop_pairs, dtype=np.float64)
    if sort:
        seqs_loop_pairs = seqs_loop_pairs[np.argsort(
                seqs_loop_pairs[:, -1])]
    return {
        "frame_freq": frame_freq,
        "glob_thresh": glob_thresh,
        "ts": ts,
        "naive_lp": naive_loop_pairs,
        "seqs_lp": seqs_loop_pairs
    }


# %%
def main(largs: LocalArgs):
    print(f"Arguments: {largs}")
    pass


if __name__ == "__main__" and ("ipykernel" not in sys.argv[0]):
    largs = tyro.cli(LocalArgs)
    _start = time.time()
    try:
        main(largs)
    except:
        print("Unhandled exception")
        traceback.print_exc()
    finally:
        print(f"Program ended in {time.time()-_start:.3f} seconds")


# %%
largs = LocalArgs()

# %%
# Parse file
data = parse_lc_file(largs)


# %%
lp = data["naive_lp"][-1]
i, j, score = int(lp[0]), int(lp[1]), lp[2]
print(f"Investigating loop pair {i}, {j} (score = {score})")
frame_freq = data["frame_freq"]

# %%
img_i = f"{largs.ds_dir}/{largs.ds_name}/color/{frame_freq * i + 1}.jpg"
img_j = f"{largs.ds_dir}/{largs.ds_name}/color/{frame_freq * j + 1}.jpg"
print(f"Image i: {img_i}")
print(f"Image j: {img_j}")

assert all(map(os.path.isfile, [img_i, img_j])), "File not found"
img_i = Image.open(img_i)
img_j = Image.open(img_j)

# %%


# %%
poses = f"{largs.ds_dir}/{largs.ds_name}/poses.csv"
assert os.path.isfile(poses), f"File not found: {poses}"
poses = pd.read_csv(poses, header=None, names=["action", "Tx", "Ty", 
        "Tz", "Qw", "Qx", "Qy", "Qz"])


# %%


# %%
pose_i, pose_j = poses.iloc[i*frame_freq], poses.iloc[j*frame_freq]

# %%
tf_w_i = pd_row_to_tf(pose_i)   # {i} in {world}
tf_w_j = pd_row_to_tf(pose_j)   # {j} in {world}

# %%
tf_i_j = np.linalg.inv(tf_w_i) @ tf_w_j     # {j} in {i}
print(f"Pose [j] in [i] is \n{np.round(tf_i_j, 4)}")

# %%


# %%
# TODO: Read the depths (and return as point clouds)
depth_i = f"{largs.ds_dir}/{largs.ds_name}/depth/"\
            f"{frame_freq * i + 1}.png"
depth_j = f"{largs.ds_dir}/{largs.ds_name}/depth/"\
            f"{frame_freq * j + 1}.png"
assert all(map(os.path.isfile, [depth_i, depth_j]))

depth_i = Image.open(depth_i)
depth_j = Image.open(depth_j)


# %%

