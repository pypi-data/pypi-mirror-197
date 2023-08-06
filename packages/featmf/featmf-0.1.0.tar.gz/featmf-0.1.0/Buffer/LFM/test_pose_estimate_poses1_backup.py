# Given a image pairs (loop closures), estimate R & t
"""
    Takes the loop_pairs file, data source, and algorithm pipeline
    as arguments and saves the transformations in a single file.

    NOTE: Backup made for storing the working pose knowledge (verifies
        that the ground truth is correct)
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
frame_freq = data["frame_freq"]

# %%
img_i = f"{largs.ds_dir}/{largs.ds_name}/color/{frame_freq * i + 1}.jpg"
img_j = f"{largs.ds_dir}/{largs.ds_name}/color/{frame_freq * j + 1}.jpg"

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
# Testing something else
d = np.load(f"{largs.ds_dir}/{largs.ds_name}/all_feat.npy")


# %%
# TODO: Read the depths (and return as point clouds)
depth_i = f"{largs.ds_dir}/{largs.ds_name}/depth/{frame_freq * i + 1}.png"
depth_j = f"{largs.ds_dir}/{largs.ds_name}/depth/{frame_freq * j + 1}.png"
assert all(map(os.path.isfile, [depth_i, depth_j]))

depth_i = Image.open(depth_i)
depth_j = Image.open(depth_j)

# %%
# 65535 is not 100 m, but 10 m
pts_i = get_pcd_from_dimg(np.array(depth_i), 65535/10)    # [H, W, XYZ]
pts_j = get_pcd_from_dimg(np.array(depth_j), 65535/10)
pcd_i = pts_img_to_o3dpc(pts_i, np.array(img_i))
pcd_j = pts_img_to_o3dpc(pts_j, np.array(img_j))

# %%
# Agent axis (frames)
ax_i = o3d.geometry.TriangleMesh.create_coordinate_frame(0.25, 
        np.array([0. ,0. ,0.]))
ax_j = o3d.geometry.TriangleMesh.create_coordinate_frame(1, 
        np.array([0. ,0. ,0.]))
# Uncomment one fo
ax_j.transform(tf_i_j)  # Agent {j} in {i}
# ax_i.transform(np.linalg.inv(tf_i_j))   # {i} in {j}
# # Convert agent to image (camera) frames
# ax_i.transform(np.linalg.inv(tf_agent_camera))
# ax_j.transform(np.linalg.inv(tf_agent_camera))
# # Display results for camera transformation frames (WORKING)
# o3d.visualization.draw_geometries([ax_i, ax_j, pcd_j])

# %%
"""
    Visualize everything in {agent_i} frame
"""
agent_pcd_i = pcd_i.transform(tf_agent_camera)  # pcd_i in {agent_i}
agent_pcd_j = pcd_j.transform(tf_agent_camera)  # pcd_j in {agent_j}
# pcd_j in {agent_i} (where agent was when {i} was taken)
agent_pcd_j.transform(tf_i_j)
o3d.visualization.draw_geometries([ax_i, ax_j, agent_pcd_i, 
    agent_pcd_j], width=1080, height=720, lookat=[0, 0, 0], 
    up=[0, 1, 0], front=[0, 0, 1], zoom=0.1)
