import pandas as pd
import numpy as np
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.preprocessing import LabelEncoder
from collections import defaultdict
from nltk.corpus import wordnet as wn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import model_selection, naive_bayes, svm
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier

#Set Random seed
np.random.seed(500)

# Add the Data using pandas
Corpus = pd.read_csv(r"drugLibTest_raw.tsv",error_bad_lines=False,sep='\t')

# Step - 1: Data Pre-processing - This will help in getting better results through the classification algorithms

# Step - 1a : Remove blank rows if any.
Corpus['benefitsReview'].dropna(inplace=True)
Corpus['rating'].dropna(inplace=True)


# Step - 1b : Change all the text to lower case. This is required as python interprets 'dog' and 'DOG' differently
Corpus['benefitsReview'] = [entry.lower() for entry in Corpus['benefitsReview']]
# Corpus['benefitsReview'] = [entry.lower() for entry in Corpus['benefitsReview']+' '+Corpus['effectiveness']+' '+Corpus['sideEffects']+' '+Corpus['condition']+' '+Corpus['sideEffectsReview']+' ' +Corpus['commentsReview']]
print(Corpus['benefitsReview'][0])
# Corpus['rating'] = [entry.lower() for entry in Corpus['rating']]

# Step - 1c : Tokenization : In this each entry in the corpus will be broken into set of words
Corpus['benefitsReview']= [word_tokenize(entry) for entry in Corpus['benefitsReview']]
# Corpus['rating']= [word_tokenize(entry) for entry in Corpus['rating']]
# print(Corpus.head())
# Step - 1d : Remove Stop words, Non-Numeric and perfom Word Stemming/Lemmenting.

# WordNetLemmatizer requires Pos tags to understand if the word is noun or verb or adjective etc. By default it is set to Noun
tag_map = defaultdict(lambda : wn.NOUN)
tag_map['J'] = wn.ADJ
tag_map['V'] = wn.VERB
tag_map['R'] = wn.ADV


for index,entry in enumerate(Corpus['benefitsReview']):
    # Declaring Empty List to store the words that follow the rules for this step
    Final_words = []

    # Initializing WordNetLemmatizer()
    word_Lemmatized = WordNetLemmatizer()
    # pos_tag function below will provide the 'tag' i.e if the word is Noun(N) or Verb(V) or something else.
    for word, tag in pos_tag(entry):
        # Below condition is to check for Stop words and consider only alphabets
        if word not in stopwords.words('english') and word.isalpha():
            word_Final = word_Lemmatized.lemmatize(word,tag_map[tag[0]])
            Final_words.append(word_Final)
    # print(Final_words)
    # The final processed set of words for each iteration will be stored in 'text_final'
    Final_words.append(str(Corpus['effectiveness'][index]))
    Final_words.append(str(Corpus['rating'][index]))
    Final_words.append(str(Corpus['sideEffects'][index]))
    Corpus.loc[index,'text_final'] = str(Final_words)



print(Corpus['text_final'][0])

# Step - 2: Split the model into Train and Test Data set
Train_X, Test_X, Train_Y, Test_Y = model_selection.train_test_split(Corpus['text_final'],Corpus['urlDrugName'],test_size=0.2,random_state=False)
# print(len(Train_X))
# print(len(Test_X))
# Step - 3: Label encode the target variable  - This is done to transform Categorical data of string type in the data set into numerical values
Encoder = LabelEncoder()
Train_Y = Encoder.fit_transform(Train_Y)
Test_Y = Encoder.fit_transform(Test_Y)

# Step - 4: Vectorize the words by using TF-IDF Vectorizer - This is done to find how important a word in document is in comaprison to the corpus
Tfidf_vect = TfidfVectorizer(max_features=5000)
Tfidf_vect.fit(Corpus['text_final'])

Train_X_Tfidf = Tfidf_vect.transform(Train_X)
Test_X_Tfidf = Tfidf_vect.transform(Test_X)
# columns = ['text','effectiveness', 'rating','sideEffects']
# df_ = pd.DataFrame(columns=columns)

#
# appendFile = open('sample.csv','w')
#
# for index,entry in enumerate(Train_X_Tfidf):
#     appendFile.write(str(list(entry)))
#     appendFile.write("\n")
# appendFile.close()


# print(df_.head())
# Step - 5: Now we can run different algorithms to classify out data check for accuracy

# Classifier - Algorithm - Naive Bayes
# fit the training dataset on the classifier
Naive = naive_bayes.MultinomialNB()
Naive.fit(Train_X_Tfidf,Train_Y)

# predict the labels on validation dataset
predictions_NB = Naive.predict(Train_X_Tfidf)

# Use accuracy_score function to get the accuracy
print("Naive Bayes Accuracy Score -> ",accuracy_score(predictions_NB, Train_Y)*100)


# Classifier - Algorithm - SVM
# fit the training dataset on the classifier
SVM = svm.SVC(C=1.0, kernel='linear', degree=5, gamma='auto')
SVM.fit(Train_X_Tfidf,Train_Y)

# predict the labels on validation dataset
predictions_SVM = SVM.predict(Train_X_Tfidf)

# Use accuracy_score function to get the accuracy
print("SVM Accuracy Score -> ",accuracy_score(predictions_SVM, Train_Y)*100)

clf_random_forest = RandomForestClassifier()
clf_random_forest.fit(Train_X_Tfidf, Train_Y)
# predict the labels on validation dataset
predictions_Random= clf_random_forest.predict(Train_X_Tfidf)

# Use accuracy_score function to get the accuracy
print("Random Accuracy Score -> ",accuracy_score(predictions_Random, Train_Y)*100)