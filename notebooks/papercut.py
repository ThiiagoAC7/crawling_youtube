import pandas as pd
import unicodedata
import spacy
import nltk


nltk.download(['stopwords', 'rslp'])
stopwords = nltk.corpus.stopwords.words('portuguese')
spacy_lemma = spacy.load('pt_core_news_sm')
spacy_lemma.max_length = 4178373

"""
cleaning data algorithms
credit: https://medium.com/data-hackers/intelig%C3%AAncia-competitiva-com-topic-modelling-c6ea855f97b
"""


def clean_text_data(df: pd.DataFrame) -> pd.DataFrame:
    ...


def remove_non_ascii(words):
    new_words = []
    for word in words:
        new_word = unicodedata.normalize('NFKD', word).encode(
            'ascii', 'ignore').decode('utf-8', 'ignore')
        new_words.append(new_word)
    return new_words


def remove_stopwords(texto):
    lista_palavras = texto.split()
    frase_ajustada = ''
    for palavra in lista_palavras:
        if palavra not in stopwords:
            frase_ajustada = frase_ajustada + ' ' + palavra
    return frase_ajustada.lower()


def convert_lowercase(words):
    lower = []
    for s in words:
        lower.append(s.lower())
    return lower


def lemmatizer(texto):
    doc = spacy_lemma(texto)
    doc_lematizado = [token.lemma_ for token in doc]
    return ' '.join(doc_lematizado)


def tokenize_rows(text):
    tokenized_text = nltk.word_tokenize(text)
    return tokenized_text

