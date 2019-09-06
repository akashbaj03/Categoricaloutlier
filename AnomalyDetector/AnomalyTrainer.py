import pandas as pd
import numpy as np
import scipy as sp
import random
from scipy.spatial.distance import mahalanobis

class TrainOutlier:
    
    data = None
    percentilek = None
    valuecountsdict = None
    colsum = None
    median = None
    invcovmx = None
    cols = None
    threshold = None
    datetimecols = None
    
    def train(self):
        df = self.data
        
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
        for d in self.datetimecols:
            df[d+'_weekday'] = self.data[d].apply(lambda m : m.weekday())
            df[d+'_hourofday'] = self.data[d].apply(lambda m : m.hour)
            self.cols = self.cols + [d+'_weekday',d+'_hourofday']
        return df
        
        
    def get_inv_frequency_values(self,df,cols):
        cols_freq = []
        for c in cols:
            d = pd.DataFrame(df[c].value_counts()).reset_index()
            d.columns = [c,c+'_frequency']
            df = pd.merge(df,d,how='left',on=[c])
            df[c+'_frequency'] = 1/df[c+'_frequency']
            cols_freq.append(c+'_frequency')
        return(df,cols_freq)

    def get_probability_values(self,df,cols,cols_freq):
        df_sum_values = pd.DataFrame(df[cols_freq].apply(sum),columns=['sum']).reset_index()
        for c in cols_freq:
            v = df_sum_values.loc[df_sum_values['index'] == c,'sum'].values[0]
            df[c] = df[c].apply(lambda x : x/(1 + v))

        return(df,df_sum_values)

    def get_mahalanobis_distance(self,df,df_median_values,cols_freq):
        #Calculate covariance matrix
        covmx = df[cols_freq].cov()
        invcovmx = sp.linalg.inv(covmx)

        df_mahalanobis = df[cols_freq].apply(lambda x: (mahalanobis(df_median_values['median'].values, x, invcovmx)), axis=1)

        return df_mahalanobis,invcovmx

    def get_value_counts_dict(self,df,cols):
        value_counts_dict = {}

        for c in cols:
            d = df.groupby([c,c+'_frequency']).size().reset_index()

            value_counts_dict[c] = d

        return(value_counts_dict)
    
    
    def __init__(self,data,percentile_k = 99.9,cat_cols=None, datetime_cols=None):
        self.data = data
        self.percentilek = percentile_k
        self.cols = cat_cols
        self.datetimecols = datetime_cols
