#!/usr/bin/env python

"""88scrape.py: Script to find racists and neo-nazis on reddit and tag them."""

__author__ = "Ayu"
__license__ = "GPL"

import praw

reddit = praw.Reddit(user_agent='88scrape')
user_dict = dict()

def main():
    with open('sublist.txt') as sublist:
        subreddit_list = sublist.readlines()
    sublist.close()
    print('Loaded subreddit list, fetching users')
    
    for sub_name in subreddit_list:
        sub_name = sub_name.rstrip()
        for submission in get_submissions(sub_name):
            user_list = get_users_from_submission(submission)
            for user_name in user_list:
                add_to_dict(user_name,sub_name)

    print('Users fetched, generating RES file.')
    create_res_file()
    print('Completed succesfully')

def get_submissions(sub_name,post_num=88):
    return reddit.get_subreddit(sub_name).get_hot(limit=post_num)

def get_users_from_submission(submission):
    users_list = []
    
    try:
        users_list = [submission.author.name.lower()]
    except Exception:
        pass

    comments = praw.helpers.flatten_tree(submission.comments)

    for comment in comments:
        try:
            users_list.append(comment.author.name.lower())
        except Exception:
            pass

    return users_list

def add_to_dict(user_name,sub_name):
    if user_name in user_dict:
        if sub_name not in user_dict[user_name]:
            user_dict[user_name] += (', ' + sub_name)
    else:
        user_dict[user_name] = sub_name

def create_res_file():
    out_file = open('res.txt','w')

    out_file.write('{')

    first = True
    for user_name, user_sublist in user_dict.items():
        if not first:
            out_file.write(',')
        else:
            first = False
        out_file.write('"'+user_name+'":{"tag":"'+user_sublist+ \
                       '","link":"","color":"black","votes":0}')

    out_file.write('}')
    out_file.close()

if __name__ == "__main__":
    main()
