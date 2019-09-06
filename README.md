# CategoricalOutlier - Detect anomalies in categorical and temporal data

Categorical Outlier package was specially designed to detect outliers in categorical data. The project was built as there is no ready-to-use packages available to detect unusual patterns in categorical data. ALmost everything focuses on numerical features.

# Overview
The categoricaloutlier was built to provide a score for the outlier-ness of the categorical features. It supports following key features -

  - Determines outlier score for categorical feature based on historical distribution
  - Supports date feature and converts it to 'day of the week', thereby, flagging an unusual weekday
  - Supports time feature and converts it to 'time of the day', thereby, flagging an unusual time in a day
  - Supports 2-dimensional categorical features, flagging unusual combinations

## Uniqueness
It learns from the historical data to quantify the anomalous nature of a new observation. A feature high variance will get a low score for an unseen observation as compared to a feature with low or zero variance. 

This is the first package that targets outliers amongst categorical features as opposed to innumerable libraries for numerical features.

## Usage

In the following paragraphs, I am going to describe how you can get and use categoricaloutlier for your own projects.

###  Getting it

To download categoricaloutlier, either fork this github repo or simply use Pypi via pip.
```sh
$ pip install categoricaloutlier
```

### Using it

Categorical Outlier can be used by simple commands to get a score for outlier-ness

```Python
from categoricaloutlier import TrainOutlier, PredictOutlier
```

And you are ready to go! At this point, I want to clearly distinct between a AnomalyTrainer and a AnomalyScorer.  

## AnomalyTrainer
AnomalyTrainer class is used to train the categorical and date time features on the historical data. It build a fundamental profile from the data for the categorical features.

### Parameters
It expects 4 parameters to train a model -
  - data - dataframe with all the rows and columns on which the model is to be trained on
  - percentile_k - This is the threshold defined for outlier-ness. Default value is 99.9%. However, user can overwrite it based on data suitability
  - cat_cols - This is the list of names of categorical columns. It has been left on the user to determine which columns needs to be included to determine outlier-ness
  - datetime_cols - This is the name(s) of the datetime column within the data. 

The current version supports day of the week and time of the day to determine anomalies. In future versions, the support may be extended to include other temporal features.

The categorical columns can be 2-dimensional feature as well. 2-dimensional features are derive features by combining 2 categorical columns into one. This is imperative as in certain cases the combination might be unusual as opposed to independent features.

Training the a new model is just two lines of code

### Initalize the train object
Let's create a new Anomaly trainer object with required parameters
```Python
at = AnomalyTrainer(data,95,cat_cols,datetime_cols)
```
Make a call to train function to train the model on the data
```Python
at.train()
```
This trains the model on the data and gives an object of AnomalyTrainer Class. This object needs to passed to the scorer to generate scores for a new observation.

## AnomalyScorer
AnomalyScorer class is built to obtain the score of outlier-ness for a new observation of the same data. It uses a sigmoid function to provide a score between 1 to 100. 1 representing most similar to existing data and 100 representing most dissimilar to existing data.

### Parameters
It expects 2 parameters to provide a score -
  - at - AnomalyTrainer object is the train object created above for training the model
  - test_data - It is a dataframe of test data which needs to be scored using the model
 
The AnomalyScorer obtains the categorical and date time columns that was used at the time of training to predict a score. The test data should have at least one observation.

Predicting a score is a one line code
```Python
score = PredictOutlier(at,test_data)
```
The result is an array of score(s) between 1 to 100 determining the outlier-ness of the data.




License
----

MIT License

Copyright (c) 2018 Joel Barmettler

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

