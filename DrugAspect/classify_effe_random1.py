from sklearn.ensemble import RandomForestClassifier

import csv

train_data = []
train_data_name = []
train_labels = []
import re
import string
import pandas as pd

initial_words = []
test_real_output = []
word_indexList = []
from nltk.corpus import stopwords

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


def getRecommendation():
    correct = 0
    incorrect = 0
    data = pd.read_csv("data2.csv", error_bad_lines=False, sep=',', lineterminator='\r')
    # print(train_data)
    # print(train_labels)
    initial_words.clear()
    word_indexList.clear()
    line_count = 0;

    for index, row in data.iterrows():
                # print(row[0])
        line_count += 1
        try:
            if line_count==2:
                print(line_count)
                print(row['effectiveness'])
                print(row['sideEffects'])
                print(row['rating'])
                print(row['urlDrugName'])
                print(row['words'])

            train_data.append([float(line_count),
                               float(row['effectiveness']),
                               float(row['sideEffects']),
                               float(row['rating'])
                               ]
                              )

            train_labels.append(row['urlDrugName'])
            train_data_name.append(row['words'])

        except Exception as e:
            hello = ''
            print(e)

    clf_random_forest = RandomForestClassifier()
    clf_random_forest.fit(train_data, train_labels)

    data = pd.read_csv("drugLibTest_raw.tsv", error_bad_lines=False, sep='\t', lineterminator='\r')
    # print(train_data)
    # print(train_labels)
    initial_words.clear()
    word_indexList.clear()
    count = 0;

    for index, row in data.iterrows():
        count = count + 1
        if count <= 10:

            try:
                # for keyword

                s = row["benefitsReview"]
                s = s.replace(',', '#')
                effective_class = row["effectiveness"]
                # urlDrugName = row["urlDrugName"]
                sideEffects = row["sideEffects"]
                rating = row["rating"]
                # print('rating'+str(rating))

                if effective_class in 'Considerably Effective':  # Negative
                    effective_class = 1.0
                elif effective_class in 'Highly Effective':  # Neutral
                    effective_class = 2.0
                elif effective_class in 'Moderately Effective':
                    effective_class = 3.0
                elif effective_class in 'Marginally Effective':
                    effective_class = 4.0
                else:
                    effective_class = 5.0

                if sideEffects in 'Mild Side Effects':  # Negative
                    sideEffects = 1.0
                elif sideEffects in 'Severe Side Effects':  # Neutral
                    sideEffects = 2.0
                elif sideEffects in 'No Side Effects':
                    sideEffects = 3.0
                elif sideEffects in 'Moderate Side Effects':
                    sideEffects = 4.0
                else:
                    sideEffects = 5.0
                # print(s)
                real_output = row['urlDrugName']
                test_real_output.append(real_output)
                index = train_data_name.index(s)
                print('index' + str(index))
                print('real_output' + str(real_output))
                word_indexList.append([float(index), float(effective_class), float(sideEffects), float(rating)])


            except Exception as e:
                here = 1

    print(word_indexList)

    predict = clf_random_forest.predict(word_indexList)
    # print(predict.count('hello'))
    # output = trending(predict.tolist())
    # output =predict.tolist()
    # print(output[0])
    # print('real='+str(real_output)+":predicted"+str(output[0]))
    print(test_real_output)
    count1 = 0
    for p in predict:
        # print(p)
        count1 = count1+1
        print(p + ":" + str(test_real_output[int(count1-1)]))
        if p in test_real_output[int(count1-1)]:

            correct = correct + 1
        else:
            incorrect = incorrect + 1


    print(correct)
    print(incorrect)
    percent = correct / (correct + incorrect) * 100.0
    print(percent)


getRecommendation()
