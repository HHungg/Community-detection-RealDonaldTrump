import tweepy
import datetime
import csv
import re
import sys
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# credentials from https://apps.twitter.com/
consumerKey = "fsuCix5k0KAwfPEspWxysiKlA"
consumerSecret = "ZBUKWbb22q4BjFtka94p7QsQvwpVaHvqtlg6yLxE8sCoqSxopu"
accessToken = "1979100115-KBsuBMN8FpyNMlNM8kgEIzldKp0V4GUj4XjBFoI"
accessTokenSecret = "Y7HJVaND4KBxXZqwl2RT76enrKC4ucyCtPlvu87tBuUsN"

auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)

api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

def check_user(username):
    try:
        api.get_user(username)
    except tweepy.TweepError as e:
            print(e, username)
            return 0 
    return 1

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

def tags_from_user(username, startDate, endDate):
    userNames = []
    tmpTweets = tweepy.Cursor(api.user_timeline, id = username).items()
    for tweet in tmpTweets:
        if "@" in tweet.text and tweet.created_at < endDate and tweet.created_at > startDate and political_sentiment(tweet.text) > 0:
            for term in tweet.text.split():
                term = re.sub('[^a-zA-Z0-9@]', '', term)
                if term.startswith('@') and len(term) > 1 and check_user(term) == 1:
                    userNames.append(term)
    # loc duplicate
    userNames = list(set(userNames))
    return userNames


def extend_by_tags(username, startDate, endDate):
    all_users = [] # mang chua tat ca user craw duoc
    level = 0
    while(1):
        if(level == 0):
            all_users.append(username)
            with open("level_%s_nodes.csv" % str(level), "w") as f:
                writer = csv.writer(f)
                writer.writerow([username])
            pass
            level = level + 1
        
        if(level != 0):
            current_level_users = [] # mang cac node cung level
            father_nodes_csv = "level_%s_nodes.csv" % str(level-1) # file chua cac node cua level truoc
            current_nodes_csv = "level_%s_nodes.csv" % str(level) # file csv chua cac node cung level
            # mo rong graph
            father_nodes = np.atleast_1d(np.loadtxt(father_nodes_csv, dtype=str, delimiter=",", usecols=(0,)))
            for node in father_nodes:
                print("Extending from user: %s (%s / %s) " % (node, np.where(father_nodes == node)[0] , len(father_nodes)))
                try:
                    tmpTag = tags_from_user(node, startDate, endDate) # voi moi node cua level truoc duoc mo rong bang tag
                except tweepy.TweepError as e:
                    print(e)
                    continue
                # ghi vao graph
                csvNames = [[node, tag] for tag in tmpTag]
                with open("graph.csv", "a") as f: # graph_csv file chua node-node
                    writer = csv.writer(f)
                    writer.writerows(csvNames)
                pass
                current_level_users.extend(tmpTag)
            # loc dulicate trong current level
            current_level_users = list(set(current_level_users))
            new_users = np.setdiff1d(current_level_users, all_users) # tim cac user moi khong co trong all_users
            # ghi lai toc do tang node cua graph
            graph = [[level, len(all_users), len(new_users), len(new_users)/len(all_users)]]
            with open("grow_speed_graph.csv", "a") as f:
                writer = csv.writer(f)
                writer.writerows(graph)
            pass
            all_users.extend(new_users)
            # ghi cac node cung level vao file
            with open(current_nodes_csv, "a") as f:
                writer = csv.writer(f)
                for user in new_users:
                    writer.writerow([user])
            pass
            level = level + 1
        if(len(new_users)/(len(all_users)-len(new_users)) < 1):
            print("Number of new users is decreased! Stop crawling!!!!!!!!!")
            break
    # ghi lai danh sach user crawl duoc
    with open("all_users.csv", "a") as f:
        writer = csv.writer(f)
        for user in all_users:
            writer.writerow([user])
    pass
    return

screen_name = "@realDonaldTrump"
startDate = datetime.datetime(2016, 9, 11, 4, 0, 0)
endDate = datetime.datetime(2018, 5, 1, 4, 0, 0)
extend_by_tags(screen_name, startDate, endDate)


            

            




                


