class PredictOutlier:
    anomalydetectorobject = None
    testdata = None
    scores = None
    
    def predict_anomaly_detector(self):
        cols_freq = []
        
        for c in anomalydetectorobject.cols:
            
            d = anomalydetectorobject.valuecountsdict[c]
            test_data = pd.merge(test_data,d,how='left',on=[c])
            new_prob_value = (1/1)/(1 + anomalydetectorobject.colsum.loc[df_sum_values['index'] == c+'_frequency','sum'].values[0])
            
            test_data[c+'_frequency'] = test_data[c+'_frequency'].fillna(new_prob_value)
            cols_freq.append(c+'_frequency')

        test_distance = test_data[cols_freq].apply(lambda x: (mahalanobis(df_median_values['median'].values, x, anomalydetectorobject.invcovmx)), axis=1)

        self.score = sigmoid_curve(test_distance,anomalydetectorobject.threshold)

        return self
    
    def sigmoid_curve(test_dist,threshold, k = 1):
        score = []
        for t in test_dist:
            v = 1.0/(1.0 + np.exp(-k*(np.log10(t) - np.log10(threshold))))
            score.append(v)
        return score
    
    def get_datetimefeatures(self, df):
        for d in self.datetimecols:
            
            df[d+'_weekday'] = self.data[d].apply(lambda m : m.weekday())
            df[d+'_hourofday'] = self.data[d].apply(lambda m : m.hour)
            self.cols = self.cols + [d+'_weekday',d+'_hourofday']
        return df
    
    def __init__(self,ad,td):
        if(test_data.shape[0]) == 0
            raise ValueError('There should be at least one observation to predict score')
        self.anomalydetectorobject = ad
        self.testdata = td
        
