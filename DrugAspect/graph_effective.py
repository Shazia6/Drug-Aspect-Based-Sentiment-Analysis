
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
    output = '';
    output1 = 0;
    output2 = 0;
    output3 = 0;
    output4 = 0;
    output5 = 0;

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

                    s = row["effectiveness"]
                    print(s)


                    if s in 'Considerably Effective':  # Negative
                        output = 'Considerably Effective'
                        output1 += 1
                    elif s in 'Highly Effective':  # Neutral
                        output = 'Highly Effective'
                        output2 += 1
                    elif s in 'Moderately Effective':
                        output3 += 1
                        output = 'Moderately Effective'
                    elif s in 'Marginally Effective':
                        output4 += 1
                        output = 'Marginally Effective'
                    else:
                        output5 += 1
                        output = 'OTHERS'
                    lstoutput.append(output)
            except Exception as e:
                here=1




    slices_hours = [output1, output2,output3,output4,output5]
    print(slices_hours)
    activities = ['Considerably', 'Highly','Moderately','Marginally','Others']
    # colors = ['r', 'g','y']
    plt.pie(slices_hours, labels=activities,  startangle=90, autopct='%.1f%%')
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