import os
import geojson
import numpy as np
import pandas as pd
from pyntcloud import PyntCloud

ply_directory = r"G:\Capstone\data"

# Reference
with open(os.path.join(ply_directory, "assets.json"), "r") as json:
    ref_folder = os.listdir(os.path.join(ply_directory, "assets", "ref"))
    assets = geojson.load(json)
    for feature in assets["features"]:
        properties = feature["properties"]
        if properties["FeatName"] + ".ply" in ref_folder:
            ply_file_path = properties["FeatName"] + ".ply"
            ref_ply_file = PyntCloud.from_file(os.path.join(ply_directory, "assets", "ref", ply_file_path))
            test_ply_file = PyntCloud.from_file(os.path.join(ply_directory, "assets", "test", ply_file_path))

            # Merge reference and test point clouds as pandas dataframes
            frames = pd.concat([ref_ply_file.points, test_ply_file.points])
            merged_pcd = PyntCloud(frames)

            # Add voxel grid to merged file
            voxelgrid_id = merged_pcd.add_structure("voxelgrid", n_x=64, n_y=64, n_z=64)
            voxelgrid = merged_pcd.structures[voxelgrid_id]

            # Query voxel grid for those containing points
            ref_voxel_match = np.unique(voxelgrid.query(ref_ply_file.points[["x", "y", "z"]].values))
            test_voxel_match = np.unique(voxelgrid.query(test_ply_file.points[["x", "y", "z"]].values))

            # Intersect populated voxel grids
            intersected_voxels = np.intersect1d(ref_voxel_match, test_voxel_match, assume_unique=True)

            ref_only = np.setdiff1d(ref_voxel_match, test_voxel_match)
            test_only = np.setdiff1d(test_voxel_match, ref_voxel_match)

            properties["vox_intersect"] = intersected_voxels.size
            properties["vox_ref"] = ref_only.size
            properties["vox_test"] = test_only.size

            y = test_voxel_match[np.in1d(test_voxel_match, ref_voxel_match)]

    with open(os.path.join(ply_directory, "assets_proc.geojson"), "w") as wjson:
        geojson.dump(assets, wjson)
