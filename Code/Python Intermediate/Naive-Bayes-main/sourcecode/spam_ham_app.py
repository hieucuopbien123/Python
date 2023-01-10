import streamlit as st
import json
import pandas as pd
import string as str
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import re
def pre_process(text):
    #lower case all the text
    text_lower=text.lower()
    #remove all the url in the text
    text_no_link=re.sub(r"http\S+", "", text_lower)
    #remove all digit,punctuation,... and only keep the alphabetic words
    text_clean=re.sub(r'[^a-z]', ' ', text_no_link)
    text_clean=" ".join(text_clean.split())
    #use wordnet lemmatizer to lemmatize the text
    wnl = WordNetLemmatizer()
    #tokenize to make array of words
    words = word_tokenize(text_clean)
    #remove all stop word such as a,he,she,many,...
    word_no_stop=[word for word in words if word not in stopwords.words('english')]
    #lemmatize all the text
    word_lemmatize=[wnl.lemmatize(word) for word in word_no_stop]
    return word_lemmatize
with open("vocab") as f:
        vocab = json.loads(f.read())
#----------intitialize all the necessary parameter and write Naive Bayes classifier----------------
#sum of the length of all document whose label is spam
num_of_spam=147684 #result from training

#sum of the length of all document whose label is ham
num_of_ham=261405 #result from training

#probality of spam email in the training set
p_spam =  1211/4137

#probality of ham email in the training set
p_ham =  2926/4137

#size of the vocabulary 
num_of_voc=len(vocab)

#function to caculate P(word[i]|spam)
def p_spam_word_MNB(word):
    if word in vocab:
      return (vocab[word][1]+1)/(num_of_spam+num_of_voc)
    else:
      return 1/(num_of_spam+num_of_voc)

#function to caculate P(word[i]|hpam)
def p_ham_word_MNB(word):
  if word in vocab:
      return (vocab[word][0]+1)/(num_of_ham+num_of_voc)
  else:
      return 1/(num_of_ham+num_of_voc)

#Multinomial Naive Bayes classifier: 
def MNB_classifier(message):
    p_spam_messge = np.log10(p_spam)
    p_ham_messge = np.log10(p_ham)
    for word in message:
        p_spam_messge += np.log10(p_spam_word_MNB(word))
        p_ham_messge += np.log10(p_ham_word_MNB(word))
    if p_ham_messge >= p_spam_messge:
        return 'ham'
    elif p_ham_messge < p_spam_messge:
        return 'spam'  
def main():
	st.title("Email Filtering App")

	text=st.text_input("Enter the content of the email")
	if st.button("Classify"):
		text=pre_process(text)
		predict=MNB_classifier(text)
		if predict=="ham":
			st.success("This is a ham email!")
		else:
			st.error("This is a spam Email")
main()