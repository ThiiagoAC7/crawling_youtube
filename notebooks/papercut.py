import pandas as pd
import unicodedata
import nltk
import re
import string

nltk.download(['stopwords', 'rslp'])
stopwords = nltk.corpus.stopwords.words('portuguese')

"""
cleaning data algorithms
credit: https://medium.com/data-hackers/intelig%C3%AAncia-competitiva-com-topic-modelling-c6ea855f97b
"""


def clean_text_data(df: pd.DataFrame) -> pd.DataFrame:
    df["comment_text"] = df["comment_text"].str.replace("<br>", " ")
    df["comment_text"] = convert_lowercase(df["comment_text"])
    df["comment_text"] = remove_a_links(df["comment_text"])
    df["comment_text"] = remove_punctuation(df["comment_text"])
    df["comment_text"] = remove_non_ascii(df["comment_text"])
    df["comment_text"] = remove_stopwords(df["comment_text"])
    return df


def remove_non_ascii(words):
    new_words = []
    for word in words:
        new_word = unicodedata.normalize('NFKD', word).encode(
            'ascii', 'ignore').decode('utf-8', 'ignore')
        new_words.append(new_word)
    return new_words


def remove_stopwords(words):
    result = []
    for word in words:
        processed_text = ''
        list_words = word.split()
        for w in list_words:
            if w not in stopwords:
                processed_text = processed_text + ' ' + w  
        result.append(processed_text)
    return result


def convert_lowercase(words):
    lower = []
    for s in words:
        lower.append(s.lower())
    return lower



def remove_a_links(words):
    cleaned_words = []
    for word in words:
        cleaned_words.append(re.sub(r'<a\s+href="[^"]*">[^<]*<\/a>', '', word))
    return cleaned_words


def remove_punctuation(words):
    result = []
    for word in words: 
        word = _replace_html_codes(word)
        result.append(''.join(c for c in word if c not in string.punctuation))
    return result

def _replace_html_codes(text):
    html_escape_table = {
        "&amp;": "&",
        "&quot;": '"',
        "&apos;": "'",
        "&gt;": ">", 
        "&lt;": "<", 
    }
    
    for code, value in html_escape_table.items():
        text = text.replace(code, value)
    
    return text

