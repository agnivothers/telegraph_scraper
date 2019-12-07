from __future__ import with_statement

import logging
import os
import re
from string import punctuation
import pickle
from grizzled.os import working_directory
from nltk.corpus import stopwords
from nltk import word_tokenize
import spacy
stop_words = stopwords.words('english') + list(punctuation)
nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])

logging.basicConfig(filename='topic_model.log', level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')

class Topicmodel:
    EXTRACTED_DATA_ROOT_DIRECTORY = ''
    def get_lemmatized_data(self):
        tokenized_data = []
        lemmatized_data = []
        print("Started lemmatizing data ...")
        logging.debug(self.EXTRACTED_DATA_ROOT_DIRECTORY)
        top_directory = '/home/agniv/Desktop/data-science/telegraph_scraper/'
        top_directory = top_directory+self.EXTRACTED_DATA_ROOT_DIRECTORY
        with working_directory(top_directory):
            datewise_directories = sorted(os.listdir(top_directory))
            for datewise_directory in datewise_directories:
                datewise_directory = top_directory + datewise_directory
                #logging.debug('DATE: '+datewise_directory)
                with working_directory(datewise_directory):
                    pagewise_directories = sorted(os.listdir(datewise_directory))
                    for pagewise_directory in pagewise_directories:
                        pagewise_directory = datewise_directory + '/' + pagewise_directory
                        #logging.debug('PAGE: '+pagewise_directory)
                        with working_directory(pagewise_directory):
                            newsfiles = sorted(os.listdir(pagewise_directory))
                            for newsfile in newsfiles:
                                #logging.debug('HEADING: '+newsfile)
                                with open(newsfile, "r") as content_file:
                                    file_content = content_file.read()
                                    text = re.sub(r'\W+', ' ', file_content)
                                    all_words = self.tokenize(text, stop_words)
                                    words = []
                                    for word in all_words:
                                        if len(word) < 3:# logging.debug("Small words not added: "+word)
                                            continue
                                        if re.match(r'^[0-9]', word):# logging.debug("Words staring with number not added: "+word)
                                            continue
                                        words.append(word)
                                    for word in words:
                                        tokenized_data.append(word)

        logging.debug(tokenized_data)
        logging.debug(len(tokenized_data))
        #lemmatized_data = self.lemmatize(tokenized_data, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])
        #logging.debug(lemmatized_data)
        #logging.debug(len(lemmatized_data))
        with open('tokenized_data.pkl', 'wb') as f:
            pickle.dump(tokenized_data, f)
        return ''

    def create_LDA_model(self):
        print("Started creating LDA model ...")

    def tokenize(self, text, stop_words):
        words = word_tokenize(text)
        words = [w.lower() for w in words]
        return [w for w in words if w not in stop_words and not w.isdigit()]

    def lemmatize(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
        i = 0
        """https://spacy.io/api/annotation"""
        texts_out = []
        # print 'In lemmatization'
        # print texts
        for word in texts:
            doc = nlp(word)
            # print 'Docs'
            # print doc
            texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
        i += 1
        logging.debug(str(i))
        return texts_out