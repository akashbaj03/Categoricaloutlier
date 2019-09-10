from distutils.core import setup
setup(
  name = 'categoricaloutlier',         # Name of the package
  packages = ['categoricaloutlier'],   
  version = '0.5',      
  license='MIT',        # MIT License
  description = 'Trains on categorical and date time features of the data and predicts an anomaly score for new data',   
  author = 'AKASH BAJPAI',                   
  author_email = 'akash.baj03@gmail.com',      
  url = 'https://github.com/akashbaj03',   # Provide either the link to your github or to your website
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
