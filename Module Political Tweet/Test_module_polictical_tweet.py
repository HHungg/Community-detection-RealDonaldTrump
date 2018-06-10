import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def political_sentiment(tweet):
    polictical_dic = np.atleast_1d(np.loadtxt("SPD.csv", dtype=str, delimiter=",", skiprows=1 , usecols=(0,)))
    words = word_tokenize(tweet)
    words = [word for word in words if word.isalpha()]
    useful_words = [word for word in words if word not in stopwords.words('english')]
    
    # print(useful_words)
    score = 0 
    for word in useful_words:
        if(word.lower().startswith(tuple(polictical_dic))):
            score = score + 1
            # print(word)
        else:
            score = score - 1

    return score

tweets = np.atleast_1d(np.loadtxt("100-tweets.csv", dtype=str, delimiter=",", usecols=(0,)))
print(len(tweets))
scores = []
for tweet in tweets:
    score = political_sentiment(tweet)
    scores.append(score)

result = []
for score in scores:
    if(score > 0):
        result.append(1)
    else:
        result.append(0)

print(len(result))
print(result)


