
from sklearn import svm
import csv
train_data = []
train_data_name = []
train_labels = []
import re
import string
import pandas as pd
initial_words = []
word_indexList = []
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
stop = list(set(stopwords.words("english")))

def trending(slst):
    count = {}
    items = []

    for item in set(slst):
        # print(item)
        count[item] = slst.count(item)

    for k, v in count.items():
        if v == max(count.values()):
            items.append(k)

    return items
from textblob import TextBlob

def getRecommendation(test_number):
    neg_count = 0;
    pos_count = 0;
    neu_count = 0;
    lstoutput=[]

    data = pd.read_csv("drugLibTest_raw.tsv",error_bad_lines=False,sep='\t', lineterminator='\r')
    #print(train_data)
    #print(train_labels)

    count = 0;
    for index, row in data.iterrows():

        count = count + 1
        if count <= 5000:


            try:
                if row["urlDrugName"] in test_number:
                    # for keyword

                    s = row["benefitsReview"] + str(row["effectiveness"]) + str(row["sideEffects"]) + str(row["rating"])

                    print(word_indexList)
                    output=''
                    blob = TextBlob(s)
                    if blob.sentiment.polarity < 0:  # Negative
                        output='Negative'
                        neg_count += 1
                    elif blob.sentiment.polarity == 0:  # Neutral
                        output = 'Neutral'
                        neu_count += 1
                    else:  # Positive
                        pos_count += 1
                        output = 'Positive'
                    lstoutput.append(output)
            except Exception as e:
                here=1

    print(pos_count)
    print(neg_count)
    print(neu_count)
    print(lstoutput)
    slices_hours = [pos_count, neg_count,neu_count]
    activities = ['Positive', 'Negative','Neutral']
    colors = ['r', 'g','y']
    plt.pie(slices_hours, labels=activities, colors=colors, startangle=90, autopct='%.1f%%')
    plt.show()


test_text = input ("Enter a Drug Name: ")

# Converts the string into a integer. If you need
# to convert the user input into decimal format,
# the float() function is used instead of int()
test_number = str(test_text)

# Prints in the console the variable as requested
print ("Drug Name: ", test_number)
if len(test_number)>0:
    getRecommendation(test_number)