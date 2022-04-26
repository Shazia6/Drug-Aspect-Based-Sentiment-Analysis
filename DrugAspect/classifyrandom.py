
from sklearn.ensemble import RandomForestClassifier
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

    with open('data2.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0

        for row in csv_reader:
            if line_count == 0:
                # print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                # print(row[0])
                line_count += 1
                try:
                    # print(row[1])
                    # print(row[2])
                    train_data.append([float(line_count),
                                       float(row['effectiveness']),
                                       float(row['sideEffects']),
                                       float(row['rating'])
                                       ]
                                      )

                    train_labels.append(row['urlDrugName'])
                    train_data_name.append(row['words'])

                except Exception as e:
                    print(e)

    clf_random_forest = RandomForestClassifier()
    clf_random_forest.fit(train_data, train_labels)

    data = pd.read_csv("test.tsv", error_bad_lines=False, sep='\t', lineterminator='\r')
    # print(train_data)
    # print(train_labels)
    count = 0;
    for index, row in data.iterrows():
        count = count + 1
        if count <= 10:


            try:
                # for keyword

                s = row["benefitsReview"]
                # print(s)
                effective_class = row["effectiveness"]
                # urlDrugName = row["urlDrugName"]
                sideEffects = row["sideEffects"]
                rating = row["rating"]
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

                print('rating'+str(rating))
                initial_words.clear()
                word_indexList.clear()
                # remove http and other stop words
                s = s.replace('!', '')
                s = s.replace('.', '')
                s = s.replace('"', '')
                s = s.replace('rt', '')
                s = s.replace('&amp;', '')
                s = s.replace(':', '')
                s = re.sub(r"(?:@\S*|#\S*|http(?=.*://)\S*)", "", s.rsplit("\n")[0].lower())
                s = re.sub(r'^http?:\/\/.*[\r\n]*', '', s, flags=re.MULTILINE)
                print(s)
                # print (s)
                # attr = []  ## attribute vectors for each status
                # ## status process
                # s = re.sub(r"(?:@\S*|#\S*|http(?=.*://)\S*)", "", s.rsplit("\n")[0].lower())
                s = s.replace("rt", "").rsplit("\n")[0]

                for word in s.translate(string.punctuation).split():
                    if (word not in initial_words and word not in stop):
                        initial_words.append(word)

                for words in initial_words:
                    try:
                        index = train_data_name.index(words)
                        word_indexList.append([float(index), float(effective_class),float(sideEffects),float(rating)])
                    except Exception as e1:
                        help=1
                        # print(e1)

                print(word_indexList)
            except Exception as e:
                here=1

            try:

                predict = clf_random_forest.predict(word_indexList)
                # print(predict)
                output = trending(predict.tolist())
                print(output)
            except Exception as e:
                print(e)



getRecommendation()