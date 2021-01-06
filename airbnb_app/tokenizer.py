import re
import pickle
import unicodedata
import numpy as np
import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from bs4 import BeautifulSoup
import spacy

nlp = spacy.load('en_core_web_md')
stopword_list = pickle.load(open('stopwords.pickle', 'rb'))