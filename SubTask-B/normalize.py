
# coding: utf-8


# # Import necessary dependencies
import spacy
import nltk
from nltk.tokenize.toktok import ToktokTokenizer
import re
import unicodedata
import contractions
from bs4 import BeautifulSoup
nlp = spacy.load("en", parse = False, tag=False, entity=False)
tokenizer = nltk.TweetTokenizer(strip_handles=True)
stopword_list = nltk.corpus.stopwords.words('english')
stopword_list.remove('no')
stopword_list.remove('not')
stopword_list.append('url')
pattern = re.compile(r"(.)\1{2,}")

#tokenization
def strip_html_tags(doc):
    soup = BeautifulSoup(doc,"html.parser")
    doc = soup.get_text()
    tokens=tokenizer.tokenize(doc)
    #filtered_tokens = [token for token in tokens if token not in stopword_list]
    return(" ".join(tokens))  
    
def remove_url(doc):
    doc = re.sub(r'https?:\/\/.*[\r\n]*','',doc)
    doc = doc.lower()
    return doc    

# # Removing accented characters
def remove_accented_chars(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    return text

#Remove additional characters    
def reduce_lengthening(text):
    return pattern.sub(r"\1\1", text)

# # Expanding Contractions
def replace_contractions(text):
    return(contractions.fix(text))


# # Removing Special Characters
def remove_special_characters(text):
    text = re.sub('[^a-zA-Z0-9\s]', '', text)
    return text


# # Lemmatizing text
def lemmatize_text(text):
    text = nlp(text)
    text = ' '.join([word.lemma_ if word.lemma_ != '-PRON-' else word.text for word in text])
    return text


# # Normalize text corpus - tying it all together
def normalize_corpus(corpus):
    normalized_corpus = []
    count=0
    for doc in corpus:
        doc = remove_url(doc) 
        doc = strip_html_tags(doc)
        doc = remove_accented_chars(doc)
        doc = replace_contractions(doc)
        doc = doc.lower()
        doc = reduce_lengthening(doc)
        doc = re.sub(r'[\r|\n|\r\n]+', ' ',doc)
        doc = lemmatize_text(doc)
        doc = remove_special_characters(doc)  
        doc = re.sub(' +', ' ', doc)
        count = count+1
        print(count)
        normalized_corpus.append(doc)
        
    return normalized_corpus



