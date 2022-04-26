import re
import string
import pandas as pd
from nltk.corpus import stopwords
# 0 - hate speech,
# 1 - offensive language,
# 2 - neither

class trainBuild:
    def __init__(self):
        self.stop = list(set(stopwords.words("english")))
        self.word = []  ##  word list all
        self.word_both = []  ##  word list

        self.benefitsReview = []  ##  hatelist
        self.offencive = []  ##  offencive
        self.neither = []  ##  neither class
        self.tweet_class = []  ##  tweets class
        self.tweets = []  ##  to store tweets
        self.data = pd.DataFrame()  ## all data

    ## get all required values
    def getValues(self):
        # nrc = pd.read_csv("input/better.csv", header = None, index_col = False)

        self.data = pd.read_csv("drugLibTest_raw.tsv",error_bad_lines=False,sep='\t', lineterminator='\r')

    ## get attribute vectors by status
    def getStatusProcessed(self, fileWriter):
        status = []  ## processed status
        ## iterate dataframe by rows
        count = 0;
        for index, row in self.data.iterrows():
            count = count + 1
            if count <= 5000:


                try:
                    s = row["benefitsReview"]
                    print(s)
                    # attr = []## attribute vectors for each status
                    ## status process
                    s = s.replace('!', '')
                    s = s.replace('.', '')
                    s = s.replace('"', '')
                    s = s.replace('rt', '')
                    s = s.replace('&amp;', '')
                    s = s.replace(':', '')
                    s = re.sub(r"(?:@\S*|#\S*|http(?=.*://)\S*)", "", s.rsplit("\n")[0].lower())
                    s = re.sub(r'^http?:\/\/.*[\r\n]*', '', s, flags=re.MULTILINE)
                    # print(s)
                    # s = s.replace("rt", "").rsplit("\n")[0]
                    for word in s.translate(string.punctuation).split():
                        # if word not in self.stop:
                        if word not in self.benefitsReview and word not in self.word:
                            # print(word)
                            if word.__len__() > 2 and not word.startswith('http'):
                                self.benefitsReview.append(word)
                                self.word.append(word)
                                effective_class = row["effectiveness"]
                                urlDrugName = row["urlDrugName"]
                                sideEffects = row["sideEffects"]
                                rating = row["rating"]
                                if effective_class in 'Considerably Effective':  # Negative
                                    effective_class=1.0
                                elif effective_class in 'Highly Effective':  # Neutral
                                    effective_class = 2.0
                                elif effective_class in 'Moderately Effective':
                                    effective_class=3.0
                                elif effective_class in 'Marginally Effective':
                                    effective_class=4.0
                                else:
                                    effective_class = 5.0

                                if sideEffects in 'Mild Side Effects':  # Negative
                                    sideEffects=1.0
                                elif sideEffects in 'Severe Side Effects':  # Neutral
                                    sideEffects = 2.0
                                elif sideEffects in 'No Side Effects':
                                    sideEffects=3.0
                                elif sideEffects in 'Moderate Side Effects':
                                    sideEffects=4.0
                                else:
                                    sideEffects = 5.0

                                filewriter.writerow(
                                    [word,  urlDrugName,effective_class,sideEffects,rating])
                except Exception as e1:
                    hello=''









x = trainBuild()
x.getValues()
import csv

with open('data2.csv', 'w') as csvFile:
    filewriter = csv.writer(csvFile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(
        ['words','urlDrugName','effectiveness','sideEffects','rating'])
    x.getStatusProcessed(filewriter)
csvFile.close()
