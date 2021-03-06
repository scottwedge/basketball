import mysql.connector
import pca_step1_modelworkflow
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import Ridge
import sklearn
from sklearn.preprocessing import scale
import numpy as np
from sklearn.metrics import mean_squared_error, make_scorer, explained_variance_score, mean_absolute_error
import pandas as pd
import models
import pickle
from sklearn.decomposition import PCA
from sklearn.preprocessing import normalize
from scipy.stats import norm

def train_model():
    '''trains a Ridge Regressor model on PCA-reduced data and tunes the hyperparameters. Returns the model'''
    cnx = mysql.connector.connect(user="wsa",
                                  host="34.68.250.121",
                                  database="basketball",
                                  password="LeBron>MJ!")
    cursor = cnx.cursor(buffered=True)

    # extract features from database
    features = pca_step1_modelworkflow.get_features_matrix(cnx, cursor, 0, 900)

    std_dev = []

    # get player ids and std dev of fanduel points for each player
    for player in features[14000:] :
        playerid = player[1]
        get_fanduel = "SELECT fanduelPts from performance WHERE fanduelPts is not null AND playerID = " + str(playerid)
        cursor.execute(get_fanduel)
        fanduel = cursor.fetchall()
        std_dev.append(np.nanstd(fanduel));

    # get features and response variable
    features, response = pca_step1_modelworkflow.split_features(features, np.linspace(
        0, 450, dtype=int, num=451))  # 456 relevant features after removal of fanduel and draftkings

    # run pca to get sparse representation of data
    features_train = features[:14000]
    response_train = response[:14000]
    features_test = features[14000:]
    response_test = response[14000:]
    
    
    features_train_pca, features_test_pca = pca_step1_modelworkflow.run_pca(features_train, features_test)
    mses = []

    model = MLPRegressor(alpha = 100.0, activation = 'relu', learning_rate = 'adaptive', solver = 'sgd', max_iter = 600)
    model.fit(features_train_pca, response_train)

    filename = 'MLP_model_confidence.sav'
    pickle.dump(model, open(filename, 'wb'))
        
    
    y_pred1 = model.predict(features_test_pca)# test prediction
    lowerbound = [];
    upperbound = [];
    prediction = [];
    triples = [];
    for i in range(len(features_test)):
        prediction.append(y_pred1[i])
        lowerbound.append(y_pred1[i] - norm.ppf(0.95)*std_dev[i])
        upperbound.append(y_pred1[i] + norm.ppf(0.95)*std_dev[i])
        triples.append([lowerbound[i], prediction[i], upperbound[i]])
        
    
    mses.append(mean_squared_error(y_pred1, response_test))

    print triples

    

def main():
    train_model()


if __name__ == "__main__":

    main()
