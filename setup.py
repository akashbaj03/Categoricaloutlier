from distutils.core import setup
setup(
  name = 'categoricaloutlier',         # Name of the package
  packages = ['categoricaloutlier'],   
  version = '0.6',      
  license='MIT',        # MIT License
  description = 'Trains on categorical and date time features of the data and predicts an anomaly score for new data',   
  long_description='Categorical Outlier is tool to detect anomalous observations in categorical and datetime features. Most of the techniques that we already have focusses mostly on numeric features. There is no library available which can detect a outlier within categories. This package builds a profile of the categorical using the past observations and gives an outlier score to a new observation on the basis of this profile. A scenario where this library can be very useful will be a predicting unusual driving behaviour. A driver who drives the same route(s) to drive to may be office will show an anomalous behaviour if he takes altogether different route on particular day. He will get a high outlier for thie behaviour. On the contrary, an uber driver drives to new location everytime and hence, a new destination will not be an anomalous behaviour and hence will get a low score. The package also takes combination of categorical features as input.'
  author = 'AKASH BAJPAI',                   
  author_email = 'akash.baj03@gmail.com',      
  url = 'https://github.com/akashbaj03/categoricaloutlier',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/akashbaj03/categoricaloutlier/archive/categoricaloutlier_v0.1.tar.gz',    # Download link
  keywords = ['categorical', 'outlier', 'anomaly', 'unsupervised','datetime','frequency','probability'],   # Keywords that define your package best
  install_requires=['pandas','numpy','scipy'],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',      #Supported python versions
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
