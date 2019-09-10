class PredictOutlier:
    anomalydetectorobject = None
    testdata = None
    scores = None
    
    def predict_anomaly_detector(self):
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

        return self
    
    def sigmoid_curve(self,test_dist, k = 1):
        score = []
        for t in test_dist:
            v = 1.0/(1.0 + np.exp(-k*(np.log10(t) - np.log10(self.anomalydetectorobject.threshold))))
            score.append(v)
        return score
    
    def get_datetimefeatures(self):
        for d in self.anomalydetectorobject.datetimecols:
            
            self.testdata[d+'_weekday'] = self.testdata[d].apply(lambda m : m.weekday())
            self.testdata[d+'_hourofday'] = self.testdata[d].apply(lambda m : m.hour)
            #self.cols = self.cols + [d+'_weekday',d+'_hourofday']
        
    
    def __init__(self,ad,td):
        if(test_data.shape[0]) == 0:
            raise ValueError('There should be at least one observation to predict score')
        self.anomalydetectorobject = ad
        self.testdata = td
        self.predict_anomaly_detector()
        
