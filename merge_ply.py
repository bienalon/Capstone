import os
import geojson
import numpy as np
import pandas as pd
from pyntcloud import PyntCloud

ply_directory = r"G:\Capstone\data"

# Merge ply files exported by CARLA Simulator
pointsList = []
# Can be limited to batches of 100, otherwise too large
i = 0
for ply_file_path in os.listdir(ply_directory):
    if ply_file_path.endswith(".ply"):
        i += 1
        plyFile = PyntCloud.from_file(os.path.join(ply_directory, ply_file_path))
        plyFile.points["z"] *= -1
        pointsList.append(plyFile.points)
    # if i % 100 == 0:
points = pd.concat(pointsList)
mergedPly = PyntCloud(points)
mergedPly.to_file(os.path.join(ply_directory, "out", str(i) + ".ply"))
        # pointsList.clear()
    # Reverse Z values in point cloud dataframe
    #plyFile.points["z"] *= -1
    #pointsList.append(plyFile.points)

points = pd.concat(pointsList)
mergedPly = PyntCloud(points)
mergedPly.to_file(os.path.join(ply_directory, "vMerged.ply"))