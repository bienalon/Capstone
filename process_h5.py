import os
import re
import h5py
import math
import numpy as np
import pandas as pd
from pyntcloud import PyntCloud

BASE_DIR = r"G:\Capstone"

# Load ply files with asset reference models
ply_folder = os.listdir(os.path.join(BASE_DIR, "data", "assets", "test"))

# Output h5 file containing ply files
h5_filename = os.path.join(BASE_DIR, "data", "assets", "test", "ply_data_test_dirty_test.h5")
# f = h5py.File(h5_filename)

NUM_POINT = 8192

# Natural Sorting
def atoi(text):
    return int(text) if text.isdigit() else text

def jitter_point_cloud(batch_data, sigma=0.01, clip=0.05):
    """ Randomly jitter points. jittering is per point.
        Input:
          BxNx3 array, original batch of point clouds
        Return:
          BxNx3 array, jittered batch of point clouds
    """
    B, N = batch_data.shape
    assert(clip > 0)
    jittered_data = np.clip(sigma * np.random.randn(B, N).astype('f4'), -1*clip, clip)
    jittered_data += batch_data
    return jittered_data

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [ atoi(c) for c in re.split('(\d+)', text) ]

# Create arrays with labels from 'shape_names.txt' file
# lbl_mexican_palm = np.array([0], dtype="uint8")
# lbl_speed_limit = np.array([1], dtype="uint8")
# lbl_street_lamp = np.array([2], dtype="uint8")
# lbl_traffic_light = np.array([3], dtype="uint8")
shape_names = {
    "AcerifoliaTree": 0, 
    "ArbustoPineTree": 1, 
    "BareAcerifoliaTree": 2, 
    "BareSassafrasTree": 3,
    "Bench": 4,
    "BusStop": 5, 
    "CypressTree": 6, 
    "DatePalm": 7, 
    "ElectricPole": 8,
    "FanPalm": 9,
    "FireHydrant": 10, 
    "Lamp": 11, 
    "MailBox": 12, 
    "MapleTree": 13,
    "ParkingMeter": 14,
    "PedestrianLamp": 15, 
    "QuercusTree": 16, 
    "SaccharumTree": 17, 
    "SassafrasTree": 18,
    "SpeedLimit": 19,
    "StopSign": 20, 
    "TotaiPalm": 21, 
    "TrafficLight": 22, 
    "TrashCan": 23,
    "WhiteFirTree": 24
    }
# List of point cloud objects from .ply files in folder
data_list = []
label_list = []

# Iterate through ply files in folder
for idx, ply_file in enumerate(ply_folder):
    # Get shape name from file name and dict
    shape = ply_file.split(".")[0]
    shape = "".join([i for i in shape if not i.isdigit()])
    # Create arrays with labels from 'shape_names.txt' file
    label = np.array([shape_names[shape]], dtype="uint8")
    label_list.append(label)
    # Read point cloud
    ply_data = PyntCloud.from_file(os.path.join(BASE_DIR, "data", "assets", "test", ply_file))
    # Resample point cloud
    #sampled_cloud = ply_data.get_sample("points_random", n=8192, as_PyntCloud=True)
    # Get points
    #points = sampled_cloud.points[["x", "y", "z"]].values
    points = ply_data.points[["x", "y", "z"]].values
    if len(points) < NUM_POINT:
        pcd_list = [points]
        mult = math.ceil((NUM_POINT / len(points)))
        for m in range(mult - 1):
            jittered = jitter_point_cloud(points)
            pcd_list.append(jittered)
        points = np.concatenate((pcd_list), axis=0)
    # Normalize coordinates
    centroid = np.mean(points, axis=0)
    points -= centroid
    furthest_distance = np.max(np.sqrt(np.sum(abs(points)**2,axis=-1)))
    points /= furthest_distance
    # Recreate pandas points from normalized points
    dataset = pd.DataFrame({'x':points[:,0], 'y':points[:,1], 'z':points[:,2]})
    norm_point_cloud = PyntCloud(dataset)
    sampled_cloud = norm_point_cloud.get_sample("points_random", n=NUM_POINT, as_PyntCloud=True)
    points = sampled_cloud.points[["x", "y", "z"]].values
    sampled_cloud.to_file(os.path.join(BASE_DIR, "data", "assets", "test", "norm_" + ply_file))
    #point_cloud = ply_data["vertex"].data
    point_cloud_list = [[row[0], row[1], row[2]] for row in points]
    #result_array[idx] = point_cloud_list
    data_list.append(point_cloud_list)

# top = max([len(sublist) for sublist in data_list])

# Indexes from 'shape_names.txt'
labels_array = np.array(label_list, dtype="uint8")
# for L in data_list:
#     for coords in L:
#         for val in coords:
#             if type(val) != np.float32:
#                 print(val)
# Create data array
data_array = np.array(data_list, dtype='f4').reshape((labels_array.size, NUM_POINT, 3))

# Write
with h5py.File(h5_filename, "w") as ply_data_train:
    ply_data_train.create_dataset("label", data=labels_array)
    ply_data_train.create_dataset("data", data=data_array)