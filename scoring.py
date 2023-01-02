"""
Author: Minh Vu
Date: December 30, 2022
This script used for scoring the model
"""
from flask import Flask, session, jsonify, request
import pandas as pd
import numpy as np
import pickle
import logging
from sklearn.metrics import f1_score
import os
import sys
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import json

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


#################Load config.json and get path variables
with open('config.json','r') as f:
    config = json.load(f) 

dataset_csv_path = os.path.join(config['output_folder_path']) 
test_data_path = os.path.join(config['test_data_path']) 

def score_model():
    """
    Loads a trained model and the test data, and calculate an F1 score
    for the model on the test data and saves the result to tje latest_score.txt file
    """
    test_df = pd.read_csv(test_data_path)
    

#################Function for model scoring
def score_model():
    #this function should take a trained model, load test data, and calculate an F1 score for the model relative to the test data
    #it should write the result to the latestscore.txt file

