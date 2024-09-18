import pandas as pd
import unicodedata

import os
import json

from sklearn.datasets import fetch_20newsgroups


"""
data cleaning algorithms
credits : https://medium.com/leti-pires/modelagem-de-t%C3%B3picos-em-python-utilizando-o-modelo-de-aloca%C3%A7%C3%A3o-latente-de-dirichlet-lda-3276a469f421
"""

def clean_text_data(df: pd.DataFrame) -> pd.DataFrame:
    ...


def remove_non_ascii(words):
    new_words = []
    for word in words:
       new_word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore')
       new_words.append(new_word)
    return new_words



def parsing_test_ignore():
    df = pd.DataFrame()
    youtuber = 'felipeneto'

    c_dir = f'./data/{youtuber}/comments/'
    r_dir = f'./data/{youtuber}/replies/'
    

    comm = [os.path.join(c_dir, f) for f in os.listdir(c_dir)]
    repl = [os.path.join(r_dir, f) for f in os.listdir(r_dir)]
    for c in comm:
        data = {}
        with open(c,'r') as f:
            data = json.load(f)

        cd = {}
        for d in data["comments"]:
            cd['youtuber'] = youtuber
            cd['video_id'] = data['video_id']
            cd['video_title'] = data['video_title']
            cd['comment_id'] = d['comment_id']
            cd['comment_text'] = d['comment_text']
            cd['comment_like_count'] = d['comment_like_count']
            cd['is_reply'] = False
            cd['parent_comment_id'] = ''
            df = pd.concat([df, pd.DataFrame([cd])], ignore_index=True)

    for c in repl:
        data = {}
        with open(c,'r') as f:
            data = json.load(f)

        cr = {}
        for d in data["replies"]:
            cr['youtuber'] = youtuber 
            cr['video_id'] = df[df['comment_id'] == d['reply_parent_comment_id']]['video_id'].values[0]
            cr['video_title'] = df[df['comment_id'] == d['reply_parent_comment_id']]['video_title'].values[0]
            cr['comment_id'] = d['reply_id']
            cr['comment_text'] = d['reply_text']
            cr['comment_like_count'] = d['reply_like_count']
            cr['is_reply'] = True
            cr['parent_comment_id'] = d['reply_parent_comment_id']
            df = pd.concat([df, pd.DataFrame([cr])], ignore_index=True)

    df.to_csv(f"./data/{youtuber}/comments.csv")
