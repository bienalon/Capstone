import os
import random
from collections import namedtuple
import csv
import geojson

root_dir = r"C:\Users\biena\Dropbox\Capstone\Results"

layer_path = os.path.join(root_dir, "assets_proc_join.geojson")

def split_geojson(layer_path, train_ration=0.33):
    with open(layer_path, "r") as layer:
        assets = geojson.load(layer)
        features = assets["features"]
        # List of random sample of 1/3 of the features in geojson
        tds_idxs = random.sample(
            range(0, len(features) - 1), int(len(features) * train_ration))
        tds_features = []
        eds_features = []

        for idx, feature in enumerate(features):
            if idx in tds_idxs:
                tds_features.append(feature)
            else:
                eds_features.append(feature)

        tds_collection = geojson.FeatureCollection(tds_features)
        eds_collection = geojson.FeatureCollection(eds_features)

    with open(os.path.join(root_dir, "assets_tds.geojson"), "w") as tds:
        geojson.dump(tds_collection, tds)
    with open(os.path.join(root_dir, "assets_eds.geojson"), "w") as eds:
        geojson.dump(eds_collection, eds)

    return (tds_collection, eds_collection)