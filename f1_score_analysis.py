import os
import random
from collections import namedtuple
import csv
import geojson
import numpy as np
import pandas as pd

root_dir = r"C:\Users\biena\Dropbox\Capstone\Results"

def analyze_results(dataset, threshold, method, name):
    features = dataset["features"]
    # Training Data Set values
    tp_num, fn_num, fp_num, tn_num = 0, 0, 0, 0
    for feature in features:
        properties=feature["properties"]
        feat_id=properties["FeatName"]
        class_id=properties["ClassID"]
        changed_condition=properties["changed_condition"]
        vb_intersect=properties["rate_pct"]
        ml_confidence=properties["ConfidScore"]

        # Set confidence value field depending on method
        if method == "VB":
            confidence=vb_intersect
        elif method == "ML":
            confidence=ml_confidence

        # Actual or intended condition change
        if changed_condition == 0:
            changed=False
        else:
            changed=True

        # Compare confidence to threshold
        if confidence < threshold:
            pred_changed=True
        else:
            pred_changed=False

        # Sort out TP, FN, FP, TN
        if changed and pred_changed:
            pos_neg='TP'  # True Positive
            tp_num += 1
        elif changed and pred_changed == False:
            pos_neg='FN'  # False Negative
            fn_num += 1
        elif changed == False and pred_changed:
            pos_neg='FP'  # False Positive
            fp_num += 1
        elif changed == False and pred_changed == False:
            pos_neg='TN'  # True Negative
            tn_num += 1
            # Field
        properties["PosNeg1"] = pos_neg
    
    with open(os.path.join(root_dir, method + "_assets_" + name + ".geojson"), "w") as wjson:
        collection = geojson.FeatureCollection(features)
        geojson.dump(collection, wjson)

    precision = tp_num / (tp_num + fp_num)
    recall = tp_num / (tp_num + fn_num)

    f1_score = 2 * (precision * recall) / (precision + recall)

    result = namedtuple("result", ["tp", "fn", "fp", "tn", "precision", "recall", "f1_score"])

    return result(tp_num, fn_num, fp_num, tn_num, precision, recall, f1_score)
    
# Test Results
with open(os.path.join(root_dir, "assets_tds.geojson"), "r") as tds:
    with open(os.path.join(root_dir, "assets_eds.geojson"), "r") as eds:
        dataset0 = geojson.load(tds)
        dataset1 = geojson.load(eds)
        thresholds = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
        vb_f1_scores = {}
        ml_f1_scores = {}
        with open(os.path.join(root_dir, "tds_scores.csv"), "w") as csv_file:
            writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["tp", "fn", "fp", "tn", "precision", "recall", "f1_score", "threshold", "method"])
            for threshold in thresholds:
                result_vb = analyze_results(dataset0, threshold, "VB", "tds")
                result_ml = analyze_results(dataset0, threshold, "ML", "tds")
                writer.writerow([result_vb.tp, result_vb.fn, result_vb.fp, result_vb.tn, result_vb.precision, result_vb.recall, result_vb.f1_score, threshold, "VB"])
                writer.writerow([result_ml.tp, result_ml.fn, result_ml.fp, result_ml.tn, result_ml.precision, result_ml.recall, result_ml.f1_score, threshold, "ML"])
                vb_f1_scores[threshold] = result_vb.f1_score
                ml_f1_scores[threshold] = result_ml.f1_score

        # Eval Results
        eds_threshold_vb = max(vb_f1_scores, key=vb_f1_scores.get)
        eds_threshold_ml = max(ml_f1_scores, key=ml_f1_scores.get)
        eds_result_vb = analyze_results(dataset1, eds_threshold_vb, "VB", "eds")
        eds_result_ml = analyze_results(dataset1, eds_threshold_ml, "ML", "eds")
        with open(os.path.join(root_dir, "eds_scores.csv"), "w") as csv_file:
            writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["tp", "fn", "fp", "tn", "precision", "recall", "f1_score", "threshold", "method"])
            writer.writerow([eds_result_vb.tp, eds_result_vb.fn, eds_result_vb.fp, eds_result_vb.tn, eds_result_vb.precision, eds_result_vb.recall, eds_result_vb.f1_score, eds_threshold_vb, "VB"])
            writer.writerow([eds_result_ml.tp, eds_result_ml.fn, eds_result_ml.fp, eds_result_ml.tn, eds_result_ml.precision, eds_result_ml.recall, eds_result_ml.f1_score, eds_threshold_ml, "ML"])

        # with open(os.path.join(root_dir, "assets_proc_join.geojson"), "w") as wjson:
        #     geojson.dump(assets, wjson)
