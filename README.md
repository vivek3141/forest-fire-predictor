<center>

![Logo](https://raw.githubusercontent.com/vivek3141/forest-fire-predictor/master/img/logo.png)

</center>

# Forest Fire Predictor
This webapp can be used to predict the amount of area burnt by a fire by selecting a point on a map.
## Built Using
* Flask API - hosted on Heroku
* Keras with a Tensorflow backend for predicting - computed on the cloud and sklearn for pre-processing
* JS and HTML for the websites
* Openweathermap API for the weather data
* Pandas, Numpy, Dill for csv reading, linear algebra and saving objects, respectively.
* Integrated and hosted on GitHub Pages
## How it works
* When the user clicks the button on the web page, the Heroku API is sent the latitude and longitude
of the place selected on the map.
* The python script then fetches weather data from the openweathermap API.
* This data is used to calculate the various Fire Weather Indices.
* The FWIs and the raw data from the API are fed into the Deep Regression model which 
outputs  
## Requirements
* `keras`, `tensorflow`, `sklearn` for machine learning
* `flask`, `flask-cors` for the API
* `numpy` for linear algebra
* `dill` for object saving
* `pandas` for reading the training data in the form of `*.csv`
