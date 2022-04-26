from textblob import TextBlob
neg = 0.0
pos = 0.0
neg_count = 0
neutral_count = 0
pos_count = 0
for tweet in Tweets:
    # print tweet.text
    blob = TextBlob(tweet.text)
    if blob.sentiment.polarity < 0:  # Negative
        neg += blob.sentiment.polarity
        neg_count += 1
    elif blob.sentiment.polarity == 0:  # Neutral
        neutral_count += 1
    else:  # Positive
        pos += blob.sentiment.polarity
        pos_count += 1