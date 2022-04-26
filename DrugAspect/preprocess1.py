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
                    s=s.replace(',','#')
                    # attr = []## attribute vectors for each status
                    ## status process


                        # if word not in self.stop:
                    if s not in self.benefitsReview:
                        # print(word)
                        if s.__len__() > 2 :
                            self.benefitsReview.append(s)
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
                                [str(s),  urlDrugName,effective_class,sideEffects,rating])
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
