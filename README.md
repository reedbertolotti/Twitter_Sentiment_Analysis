# Twitter Sentiment Analysis
Determine tweet sentiment using machine learning.

Front end allows user to input a tweet.
Twitter API used to get that tweet's replies.
Sentiment analysis applied to replies to gauge sentiment toward original tweet.

# Contents
## demo
- the interactive front-end of our project
## notebooks
- code that trains the model for the back-end of the demo (bertweet_train_final_model.ipynb)
- exploration and other code not part of the demo

# Demo
## Environment
#### JS libraries:
conda install nodejs (version 17.9.0) <br>
change current directory to demo directory <br>
npm install express (version 4.18.1) <br>
npm install python-shell (version 3.0.1) <br>
*note: conda has npm by default

#### Python libraries:
conda install lxml (version 4.9.0) <br>
conda install tweepy (version 4.10.0) <br>
conda install pandas (version 1.4.2) <br>
conda install tensorflow (version 2.8.1) <br>
conda install transformers (version 4.19.2) <br>
conda install matplotlib (version 3.5.2) <br>
conda install dataframe_image (version 0.1.1) <br>

#### Model weights
- model weights (bertweet_FullTrained.h5) must be downloaded and placed into the demo folder
  - https://drive.google.com/file/d/12qIwJfklEVOAK6pmCGgQKmHJ2SzKFCek/view?usp=sharing

## Running:
- on command prompt/terminal, run: node index.js <br>
- in browser, open: http://localhost:3000/ <br>

#### Notes on running:
- tweets must be in form: https://twitter.com/userName/status/tweetID
  - example: https://twitter.com/SportsCenter/status/1533286249393528833
- tweets must be less than 7 days old
