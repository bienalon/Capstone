import os
import geojson
import numpy as np
import pandas as pd
from pyntcloud import PyntCloud

ply_directory = r"G:\Capstone\data"

ref_pnt_cld = PyntCloud.from_file(os.path.join(ply_directory, "TestFinalFilter.ply"))
df = ref_pnt_cld.points

with open(os.path.join(ply_directory, "assets.json")) as data:
    assets = geojson.load(data)
    for feature in assets["features"]:
        xMaxCrop = df["x"] < feature.properties["max_x"]
        yMaxCrop = df["y"] < feature.properties["max_y"]
        zMaxCrop = df["z"] < feature.properties["max_z"]
        xMinCrop = df["x"] > feature.properties["min_x"]
        yMinCrop = df["y"] > feature.properties["min_y"]
        zMinCrop = df["z"] > feature.properties["min_z"]

        cropped = df.loc[
            xMaxCrop & yMaxCrop & zMaxCrop & xMinCrop & yMinCrop & zMinCrop
            ]
        name = feature.properties["FeatName"]
        name = name.replace(" ", "")
        croppedZPly = PyntCloud(cropped)
        croppedZPly.to_file(os.path.join(ply_directory, "assets", "test", name + ".ply"))