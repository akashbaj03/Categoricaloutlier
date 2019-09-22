"""Scorer class to generate anomaly score for new observations."""
import pandas as pd
import numpy as np
import scipy as sp
import random
from scipy.spatial.distance import mahalanobis

class PredictOutlier:
    anomalydetectorobject = None
    testdata = None
    scores = None
    
    def predict_anomaly_detector(self):
        
    """Predict function to obtaina score based on categorical data points.
    
    The method in turn calls other functions to obtain the probability and
    mahalanobis distance of the new observation.
    
    Returns
    -------
    scores: array
        array of scores for all the observation(s)
    """
        cols_freq = []
        if(self.anomalydetectorobject.datetimecols != None):
            self.get_datetimefeatures()
            
        for c in self.anomalydetectorobject.cols:
            
            d = self.anomalydetectorobject.valuecountsdict[c]
            
            self.testdata = pd.merge(self.testdata,d,how='left',on=[c])
            new_prob_value = (1/1)/(1 + self.anomalydetectorobject.colsum.loc[self.anomalydetectorobject.colsum['index'] == c+'_frequency','sum'].values[0])
            
            self.testdata[c+'_frequency'] = self.testdata[c+'_frequency'].fillna(new_prob_value)
            cols_freq.append(c+'_frequency')

        test_distance = self.testdata[cols_freq].apply(lambda x: (mahalanobis(self.anomalydetectorobject.median['median'].values, x, self.anomalydetectorobject.invcovmx)), axis=1)

        self.scores = self.sigmoid_curve(test_distance,self.anomalydetectorobject.threshold)

        return self.scores
    
    def sigmoid_curve(self,test_dist, k = 1):
    """Sigmoid function is used to fit the distance distribution.
    It provides anomaly score between 0 and 100
    
    Returns
    -------
    score: value to quantify the anomaly-ness (0-100)
        
    """
        score = []
        for t in test_dist:
            v = 1.0/(1.0 + np.exp(-k*(np.log10(t) - np.log10(self.anomalydetectorobject.threshold))))
            score.append(v)
        return score
    
    def get_datetimefeatures(self):
    """Extracts the supported date time features by the model.
    Anomalous hour of the day and week day are flagged
        
    """
        for d in self.anomalydetectorobject.datetimecols:
            
            self.testdata[d+'_weekday'] = self.testdata[d].apply(lambda m : m.weekday())
            self.testdata[d+'_hourofday'] = self.testdata[d].apply(lambda m : m.hour)
            #self.cols = self.cols + [d+'_weekday',d+'_hourofday']
        
    
    def __init__(self,ad,td):
    """Constructor for the class.
    
    Keyword arguments:
        ad : Object of the training class
        
        td : dataframe of test data
    """
        if(td.shape[0]) == 0:
            raise ValueError('There should be at least one observation to predict score')
        self.anomalydetectorobject = ad
        self.testdata = td.copy()
        self.predict_anomaly_detector()
        
