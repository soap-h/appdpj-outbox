# This module will do all the database things
# Advantage: 1. Much cleaner 2. Easy to change

import shelve

from Question import Question
from News import News

def get_key(my_dict):  # Find latest key > key is the largest number
    # commonly used function to pass key from a dictionary
    if len(my_dict) == 0:
        my_key = 1
    else:
        print(my_dict.keys())
        my_key = max(my_dict.keys()) + 1

    return my_key



def add_question(qn:Question):
    question_dict = {}

    db = shelve.open('database.db', 'c')
    try:
        question_dict = db['Question']
    except:
        print("Error in retrieving questions from database.db.")

    k= get_key(question_dict)
    qn.set_question_id(k)
    print(qn)
    question_dict[k] = qn
    db['Question'] = question_dict  # update database

    db.close()

def add_news(n: News):
    news_dict = {}

    db = shelve.open('database.db', 'c')
    try:
        news_dict = db['News']
    except:
        print("Error in retrieving news from database.db.")

    k = get_key(news_dict)
    n.set_nid(k)
    print(n)
    news_dict[k] = n
    db['News'] = news_dict  # update database
    db.close()




# see if adding user is successful
def display_all_question():  # for testing purposes
    question_dict = {}
    db = shelve.open('database.db', 'c')  # open db
    try:
        question_dict = db['Question']  # retrieve data
        for k, v in question_dict.items():
            print(f"{k}:{v}")  # display data
    except:
        print("Error in retrieving Questions from database.db.")






