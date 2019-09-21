"""Trainer class to build a model using the historical data."""
import pandas as pd
import numpy as np
import scipy as sp
import random
from scipy.spatial.distance import mahalanobis

class TrainOutlier:
 
    percentilek = None
    valuecountsdict = None
    colsum = None
    median = None
    invcovmx = None
    cols = None
    threshold = None
    datetimecols = None
    
    
    def train(self,df):
        """Train method takes the entire dataframe
        along with the categorical and datetime columns
        to train on the data and generate fundamental 
        training parameters.
    Keyword arguments:
        df : Dataframe of the training data
    Returns
    -------
    self : returns a object of the class
    """
        if((self.cols != None) & (self.datetimecols != None)):
            df = df[self.cols+self.datetimecols]
        elif(self.datetimecols == None):
            df = df[self.cols]
        elif(self.cols == None):
            df = df[self.datetimecols]
        else:
            raise ValueError('At least one categorical or date time column must be supplied')

        #df_cols = pd.DataFrame((df.nunique() < 100) & (df.nunique() > 2),columns = ['values'])
        #self.cols = df_cols[df_cols.values == True].index
    
        if(self.datetimecols != None):
            df = self.get_datetimefeatures(df)
        df,cols_freq = self.get_inv_frequency_values(df,self.cols)
        df,self.colsum = self.get_probability_values(df,self.cols,cols_freq)

        self.median = pd.DataFrame(df[cols_freq].apply(np.median),columns=['median']).reset_index()
        df_mahalanobis,self.invcovmx = self.get_mahalanobis_distance(df,self.median,cols_freq)

        self.threshold = np.percentile(df_mahalanobis,self.percentilek)

        self.valuecountsdict = self.get_value_counts_dict(df,self.cols)

        return self #value_counts_dict, df_sum_values, df_median_values, invcovmx, cols, threshold
    
    def get_datetimefeatures(self, df):
      """Currently, the model supports 2 ways of datetime features
      Weekday - extracts day of the week from the datetime
      Hourofday - extracts hour of the day from the datetime.
    Keyword arguments:
        df : Dataframe of the training data
        
    Returns
    -------
        df : Dataframe with added weekday and hourofday
     """
        for d in self.datetimecols:
            df[d+'_weekday'] = df[d].apply(lambda m : m.weekday())
            df[d+'_hourofday'] = df[d].apply(lambda m : m.hour)
            self.cols = self.cols + [d+'_weekday',d+'_hourofday']
        return df
        
        
    def get_inv_frequency_values(self,df,cols):
     """ Performs an inverse of the frequency values for categorical data
    Keyword arguments:
        df : Dataframe of the training data
        cols : Column names for categorical and datetime features
    Returns
    -------
        df : Dataframe with added frequency values
        cols_freq : Columns for which frequency values are derived
     """
        cols_freq = []
        for c in cols:
            d = pd.DataFrame(df[c].value_counts()).reset_index()
            d.columns = [c,c+'_frequency']
            df = pd.merge(df,d,how='left',on=[c])
            df[c+'_frequency'] = 1/df[c+'_frequency']
            cols_freq.append(c+'_frequency')
        return(df,cols_freq)

    def get_probability_values(self,df,cols,cols_freq):
     """ Obtains the probability values from the inverse frequency
     P(xi) = (1/xi)/sum(1/x1,1/x2...1/xi...1/xn)
    Keyword arguments:
        df : Dataframe of the training data
        cols : Column names for categorical and datetime features
        cols_freq : column names for which frequency is obtained
    Returns
    -------
        df : Dataframe with added weekday and hourofday
        df_sum_values : Sum values for frequency columns
     """
        df_sum_values = pd.DataFrame(df[cols_freq].apply(sum),columns=['sum']).reset_index()
        for c in cols_freq:
            v = df_sum_values.loc[df_sum_values['index'] == c,'sum'].values[0]
            df[c] = df[c].apply(lambda x : x/(1 + v))

        return(df,df_sum_values)

    def get_mahalanobis_distance(self,df,df_median_values,cols_freq):
     """ Mahalanobis distance is the metric used for quantifying the 
     anomalous-ness of a new observation. Advantage of using MD is it
     calculates the distance of an observation from the cluster and takes 
     into account the direction of the observation.
    Keyword arguments:
        df : Dataframe of the training data
        df_median_values : Median values for each categrical columns
        cols_freq : column names for which frequency is obtained
    Returns
    -------
        df_mahalanobis : Dataframe with Mahalanobis distance
        invcovmx : Inverse Covariance Matrix
     """
        #Calculate covariance matrix
        covmx = df[cols_freq].cov()
        invcovmx = sp.linalg.inv(covmx)

        df_mahalanobis = df[cols_freq].apply(lambda x: (mahalanobis(df_median_values['median'].values, x, invcovmx)), axis=1)

        return df_mahalanobis,invcovmx

    def get_value_counts_dict(self,df,cols):
     """ Value counts for all the levels of the categorical columns are
     obtained and stored to be used for prediction.
    Keyword arguments:
        df : Dataframe of the training data
        cols : Column names for categorical and datetime features
    Returns
    -------
        value_counts_dict : Dataframe of value counts for all categorical columns
     """
        value_counts_dict = {}

        for c in cols:
            d = df.groupby([c,c+'_frequency']).size().reset_index()

            value_counts_dict[c] = d

        return(value_counts_dict)
    
    
    def __init__(self,percentile_k = 99.9,cat_cols=None, datetime_cols=None):
    """ Constructor for the class.
    Keyword arguments:
        percentile_k : Threshold percentile for defining anomaly
        cat_cols : Categorical Column Names
        datetime_cols : Datetime Column Names
     """    
        self.percentilek = percentile_k
        self.cols = cat_cols
        self.datetimecols = datetime_cols
        
