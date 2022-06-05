import sys

# Twitter API
import tweepy
import csv

# Tweet Analysis
import os
import re
import pandas as pd
import tensorflow as tf
from transformers import AutoTokenizer, TFAutoModelForSequenceClassification
from transformers import InputExample, InputFeatures

# Graphing/Output
import matplotlib.pyplot as plt
import dataframe_image as dfi


# User input
url = sys.argv[1]

# Twitter API
consumer_key = "xc9jIyaEk9rdgnkuESI2dHIe1"
consumer_secret = "P5soIFD9vq7CUNba768NmPqul9jQLYs0lByseErxYrOuYBV9ub"
access_key= "1229631115205341186-vntUrsfzLCzG7PJrJu0zf83J2XSJDk"
access_secret = "K1WdSL7KYQozn50KHGizxucj6ggUd19RFFmDiSrD8MZ95"

bearer_token = "AAAAAAAAAAAAAAAAAAAAANo%2BcgEAAAAADttN1q0nUgqlR3TdwHYsXjRfMEY%3DPEIeD7oPcX6BO1ltXHgJ9VT3pWqJCYwBVlFKqLiV7KweSTR1Z8"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)

api = tweepy.API(auth,wait_on_rate_limit=True)
client = tweepy.Client(bearer_token, consumer_key, consumer_secret, access_key, access_secret)

#csvFile = open('replies.csv', 'w') # for linux
csvFile = open('replies.csv', 'w', encoding="utf-8") # for windows
csvWriter = csv.writer(csvFile)

temp = url[::-1]
id = temp[ temp.find('/') - 19 : temp.find('/')]
tweet_id = id[::-1]

status = api.get_status(tweet_id)

start_id = tweet_id
n=5

#reads a max of 100n replies
for i in range(n):
    #create filter Query
    q = 'conversation_id:'+str(tweet_id) + ' to:'+status.user.screen_name + ' is:reply' + ' -has:links' + ' lang:en'

    #Max batch size for replies is 100
    for reply in client.search_recent_tweets(query=q, max_results=100, since_id=start_id).data:
        #remove first @tag and append to csv
        csvWriter.writerow([reply.text[len(status.user.screen_name)+1:], reply.id])
        start_id = reply.id  + 1

csvFile.close()


# Tweet Analysis
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
tf.config.list_physical_devices('GPU')

#uses Hugging Face Pre-Trained Transformer Library (transformers)
with tf.device('/CPU:0'):
    model = TFAutoModelForSequenceClassification.from_pretrained("vinai/bertweet-base",num_labels=3,problem_type="multi_label_classification")
    tokenizer = AutoTokenizer.from_pretrained("vinai/bertweet-base",num_labels=3)


model.load_weights('bertweet_FullTrained.h5')
dfRaw = pd.read_csv('replies.csv')

df = pd.DataFrame()
df['DATA_COLUMN'] = dfRaw.iloc[:,0]
df['LABEL_COLUMN'] = 0

def convertToExamples(data,DATA_COLUMN,LABEL_COLUMN):
    dataOut = data.apply(lambda x: InputExample(guid=None, # Globally unique ID for bookkeeping, unused in this case
                        text_a = x[DATA_COLUMN], 
                        text_b = None,
                        label = x[LABEL_COLUMN]), axis = 1)
    return dataOut 

def convert_examples_to_tf_dataset(examples, tokenizer, max_length=128):
    features = [] # -> will hold InputFeatures to be converted later

    for e in examples:
        # Documentation is really strong for this method, so please take a look at it
        input_dict = tokenizer.encode_plus(
            e.text_a,
            add_special_tokens=True,
            max_length=max_length, # truncates if len(s) > max_length
            return_token_type_ids=True,
            return_attention_mask=True,
            pad_to_max_length=True, # pads to the right by default # CHECK THIS for pad_to_max_length
            truncation=True
        )

        input_ids, token_type_ids, attention_mask = (input_dict["input_ids"],
            input_dict["token_type_ids"], input_dict['attention_mask'])

        features.append(
            InputFeatures(
                input_ids=input_ids, attention_mask=attention_mask, token_type_ids=token_type_ids, label=e.label
            )
        )

    def gen():
        for f in features:
            yield (
                {
                    "input_ids": f.input_ids,
                    "attention_mask": f.attention_mask,
                    "token_type_ids": f.token_type_ids,
                },
                f.label,
            )

    return tf.data.Dataset.from_generator(
        gen,
        ({"input_ids": tf.int32, "attention_mask": tf.int32, "token_type_ids": tf.int32}, tf.int64),
        (
            {
                "input_ids": tf.TensorShape([None]),
                "attention_mask": tf.TensorShape([None]),
                "token_type_ids": tf.TensorShape([None]),
            },
            tf.TensorShape([]),
        ),
    )

dataInputExamples = convertToExamples(df,'DATA_COLUMN','LABEL_COLUMN')

with tf.device('/GPU:0'):
    dataTensor = convert_examples_to_tf_dataset(list(dataInputExamples), tokenizer)
    dataTensor = dataTensor.batch(1)
    
with tf.device('/CPU:0'):
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=3e-5, epsilon=1e-08, clipnorm=1.0), 
                loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True), 
                metrics=[tf.keras.metrics.SparseCategoricalAccuracy('accuracy')])
    out = model.predict(dataTensor)
    
outDF = pd.DataFrame(out['logits'])
outCat = outDF.idxmax(axis=1)
outValue = outDF.max(axis=1)
overallOut = pd.concat([df['DATA_COLUMN'], outCat, outValue],axis=1)


# Graphing/Output
plt.pie(overallOut[0].value_counts().sort_index(), labels = ['negative','neutral','positive'], colors = ["r", "c", "g"], autopct='%1.1f%%', shadow=True, startangle=90)
plt.savefig('graph.png')

overallOut[0] = overallOut[0].replace(0, "negative")
overallOut[0] = overallOut[0].replace(1, "neutral")
overallOut[0] = overallOut[0].replace(2, "positive")
overallOut.rename(columns=({ "DATA_COLUMN": "", 0: "Predicted Sentiment", 1: "Probability"}), inplace=True)

overallOut.to_csv('test2.csv')

new_df = overallOut.sample(n=10, replace=False)
new_df = new_df.drop("Probability", axis=1)
pd.set_option("display.max_column", None)
pd.set_option("display.max_colwidth", 100)
pd.set_option('display.width', -1)
pd.set_option('display.max_rows', None)

dfi.export(
    new_df,
    "sample.png",
    table_conversion="matplotlib"
)