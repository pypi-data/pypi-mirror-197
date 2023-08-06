# Test a matching algorithm on two images
"""
    Currently testing forward pass of feature detection algorithms
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
from LFM.matching_algos import SIFT, MNN
from PIL import Image


# %%
algo = SIFT(root_sift=True)

# %%
img_1 = Image.open("/scratch/avneesh.mishra/divloc/lc/qsmall/color/670.jpg")
img_2 = Image.open("/scratch/avneesh.mishra/divloc/lc/qsmall/color/502.jpg")

# %%
res1, res2 = algo([np.array(img_1), np.array(img_2)])

# %%
