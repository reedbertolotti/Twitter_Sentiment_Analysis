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
### JS libraries:
install node js <br>
npm install express <br>
npm install python-shell (rooted from child-process library) <br>

### Python libraries:
pip install tweepy <br>
pip install csv <br>
pip install os <br>
pip install re <br>
pip install pandas <br>
pip install tensorflow <br>
pip install transformers <br>
pip install matplotlib <br>
pip install dataframe_image <br>

## Running:
on command prompt/terminal: <br>
cd file_directory <br>
node index.js <br>

### Limitations of usable tweets:
- Tweet must be less than 7 days old
