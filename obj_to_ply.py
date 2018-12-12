import os
import numpy as np
import pandas as pd
from pyntcloud import PyntCloud

BASE_DIR = r"G:\Capstone\data\assets\objs"
obj_folder = os.listdir(BASE_DIR)

# for ply_file_path in os.listdir(ply_directory):
#     plyFile = PyntCloud.from_file(os.path.join(ply_directory, ply_file_path))
#     # Reverse Z values in point cloud dataframe
#     plyFile.points["z"] *= -1
#     pointsList.append(plyFile.points)
# Iterate through ply files in folder
for idx, obj_file in enumerate(obj_folder):
    obj = os.path.splitext(obj_file)
    if obj[1] == ".obj":
        mesh = PyntCloud.from_file(os.path.join(BASE_DIR, obj_file))
        for i in range(8):
            cloud = mesh.get_sample("mesh_random", n=8192, as_PyntCloud=True)
            cloud.to_file(os.path.join(BASE_DIR, "8192", obj[0] + str(i+1) + ".ply"))
        #new_cloud = cloud.get_sample("voxelgrid_nearest", voxelgrid=mesh_random, as_PyntCloud=True)