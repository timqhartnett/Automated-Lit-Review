#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 16:53:49 2021



@author: timothy
"""
import pandas as pd
import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
import re
import unicodedata
import random
os.chdir('/home/timothy/NLP')

import Lit_review_AI as litai

archive_driver = litai.archive_scrapper(driver_path='/home/timothy/chromedriver')

'''
find training datasets for BERT training
randomly sample 10 papers from each properties class
'''
random.seed(42)
training_materials_properties = ['magnetic materials','structural materials','superconducting materials',
                                  'ferroelectric materials','thermoelectric materials']


def title_and_abstract_search(keywords):
    papers = {}
    for i in range(len(training_materials_properties)):
        mined_papers = archive_driver.find_all_abstracts(training_materials_properties[i])
        papers.update({training_materials_properties[i]:mined_papers})
    return papers

def create_training_validation(number_papers_per_keyword,paper_dict):
    training_df = None
    for key in paper_dict.keys():
        sample_df = paper_dict[key].sample(n=number_papers_per_keyword)
        if training_df is None:
            training_df = sample_df.iloc[:int(number_papers_per_keyword*0.8),:]
            validation_df = sample_df.iloc[int(number_papers_per_keyword*0.8):,:]
        else:
            training_df = pd.concat(training_df,sample_df.iloc[:int(number_papers_per_keyword*0.8),:],axis=0)
            validation_df = pd.concat(validation_df,sample_df.iloc[int(number_papers_per_keyword*0.8):,:],axis=0)
    return training_df, validation_df

def clean_text_tokenize(dataframe):
    '''
    takes dataframe from selenium scrapped data and cleans the text for NLP
    cleaning steps are:
    1 sentence tokenization 
    2 unique character and punctuation elimination in conjuction with case lowering
    3 word tokenization by sentence because BERT in tensor flow goes sentence by sentence
    4 removal of stop words from word tokens
    5 combine in dataframe word tokens with sentence identifier
    '''
    dataframe.index = range(len(dataframe.index))
    sentences = []
    for row in dataframe.index:
        sents = sent_tokenize(dataframe.loc[row,'Title'])
        for sent in sents:
            sent = re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", sent)
            sentences.append(sent.lower())
        sents = sent_tokenize(dataframe.loc[row,'Abstract'])
        for sent in sents:
            sent = re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", sent)
            sentences.append(sent.lower())
    word_tokens = [word_tokenize(text) for text in sentences]
    #nltk for stop words 
    nltk.download('stopwords')
    from nltk.corpus import stopwords
    stop = stopwords.words('english')
    #combine into dataframe, labels must be added manually to training and test set for new NER model creation
    cleaned_training = []
    sentence_labels = []
    for c,text_li in enumerate(word_tokens):
        words = [word for word in text_li if word not in stop]
        cleaned_training.extend(words)
        sentence_labels.extend([c]*len(words))
    cleaned_word_tokens = pd.DataFrame({'sentence':sentence_labels,'word':cleaned_training})

    return(cleaned_word_tokens)

corpus_papers = title_and_abstract_search(training_materials_properties)
training_df, validation_df = create_training_validation(10,corpus_papers)
cleaned_training = clean_text_tokenize(training_df)
cleaned_validation = clean_text_tokenize(validation_df)
cleaned_training.to_csv('/home/timothy/NLP/cleaned_training_tokens.csv')
cleaned_validation.to_csv('/home/timothy/NLP/cleaned_val_tokens.csv')
