import numpy as np

tune = {
        "mfcc":
        {
             "learning_rate" : [0.1]
            , "n_estimators" : [100]
            ,"max_depth" : [7]
            , "min_child_weight" : [1]
            , "gamma" : [0.0]
            , "subsample" : [0.8]
            , "colsample_bytree" : [0.8]
            , "scale_pos_weight" : [1]
        },
        "hmfcc":
        {
            "max_depth" : [3,5]
            , "min_child_weight" : [1]
            , "gamma" : [0]
            , "subsample" : [0.6]
            , "learning_rate" : [0.1]
        },
        "pmfcc":
        {
            "max_depth" : [3]
            , "min_child_weight" : [1]
            , "gamma" : [0]
            , "subsample" : [0.58]
            , "learning_rate" : [0.13]
            , "colsample_bytree" : [1.0]
        },
        "tfidf_1gram":
        {
            "max_depth" : [7]
            , "min_child_weight" : [0]
            , "gamma" : [1]
            , "subsample" : [0.5]
            , "colsample_bytree" : [0.9]
            , "learning_rate" : [0.20]
            , "n_estimators" : [100]
        },
        "tfidf_2gram":
        {
            "max_depth" : [8]
            , "min_child_weight" : [0]
            , "gamma" : [0.0]
            , "subsample" : [0.78]
            , "colsample_bytree" : [0.8]
            , "learning_rate" : [0.18]
            , "n_estimators" : [130]
        },
        "tfidf_3gram":
        {
            "max_depth" : [7]
            , "min_child_weight" : [0]
            , "gamma" : [0.0]
            , "subsample" : [0.78]
            , "colsample_bytree" : [0.8]
            , "learning_rate" : [0.18]
            , "n_estimators" : [130]
        },
        "tfidf_4gram":
        {
            "max_depth" : [7]
            , "min_child_weight" : [0]
            , "gamma" : [1]
            , "subsample" : [0.575]
            , "colsample_bytree" : [0.90]
            , "learning_rate" : [0.105]
        },
        "ssd":
        {
            "max_depth" : [6]
            , "min_child_weight" : [1]
            , "gamma" : [0.40]
            , "subsample" : [0.81]
            , "colsample_bytree" : [0.80]
            , "learning_rate" : [0.50]
            , "n_estimators" : [50]
        },
        "rp":
        {
            "max_depth" : [6,]
            , "min_child_weight" : [1,]
            , "gamma" : [0,]
            , "subsample" : [0.95,]
            , "colsample_bytree" : [0.85,]
            , "learning_rate" : [0.125]
        },
        "rh":
        {
            "max_depth" : [6,]
            , "min_child_weight" : [1,]
            , "gamma" : [0,]
            , "subsample" : [0.95,]
            , "colsample_bytree" : [0.85,]
            , "learning_rate" : [0.1,0.125,0.15]
        },
    }
