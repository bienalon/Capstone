import os
import csv
import geojson
import numpy as np
import pandas as pd
from sklearn.metrics import precision_score

root_dir = r"G:\Capstone"

pred_label_path = os.path.join(root_dir, "pred_label.csv")
layer_path = os.path.join(root_dir, "assets_proc.geojson")

csv_dict = {}
with open(pred_label_path, "r") as pred_label:
    csv_reader = csv.reader(pred_label)
    # 'pred_conf_score', ' conf_score', ' prediction', ' label', 'id'
    headers = next(csv_reader, None)
    for row in csv_reader:
        feat_id = row[4]
        prediction = int(row[2])
        conf_score = float(row[1])
        pred_conf_score = float(row[0])
        csv_dict[feat_id] = [pred_conf_score, conf_score, prediction]

with open(os.path.join(root_dir, "assets_proc_join.geojson"), "w") as wjson:
    geojson.dump(assets, wjson)