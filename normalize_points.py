import os
import numpy as np
import pandas as pd
from pyntcloud import PyntCloud

BASE_DIR = r"G:\Capstone\pointnet"
ply_folder = os.listdir(os.path.join(BASE_DIR, "data", "ply_files"))

# Iterate through ply files in folder
for idx, ply_file in enumerate(ply_folder):
    ply_data = PyntCloud.from_file(os.path.join(BASE_DIR, "data", "ply_files", ply_file))
    point_cloud = ply_data.points[["x", "y", "z"]].values
    #centroid = np.mean(point_cloud, axis=0)
    point_cloud -= ply_data.centroid
    furthest_distance = np.max(np.sqrt(np.sum(abs(point_cloud)**2,axis=-1)))
    point_cloud /= furthest_distance
    dataset = pd.DataFrame({'x':point_cloud[:,0], 'y':point_cloud[:,1], 'z':point_cloud[:,2]})
    norm_point_cloud = PyntCloud(dataset)
    norm_point_cloud.to_file(os.path.join(BASE_DIR, "data", "ply_files", "norm_" + ply_file))