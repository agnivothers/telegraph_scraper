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
import gensim
from gensim import models, corpora
from gensim.test.utils import datapath
stop_words = stopwords.words('english') + list(punctuation)
nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])

logging.basicConfig(filename='topic_model.log', level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')

class Topicmodel:
    TRAINING_DATA_ROOT_DIRECTORY = ''
    TEST_DATA_ROOT_DIRECTORY = ''
    NUM_TOPICS = 0
    def get_tokenized_training_data(self):
        tokenized_data = []
        lemmatized_data = []
        print("Started tokenized data ...")
        logging.debug(self.TRAINING_DATA_ROOT_DIRECTORY)
        top_directory = '/home/agniv/Desktop/data-science/telegraph_scraper/'
        top_directory = top_directory+self.TRAINING_DATA_ROOT_DIRECTORY
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
                                    #for word in words:
                                    tokenized_data.append(words)

        #logging.debug(tokenized_data)
        #logging.debug(len(tokenized_data))
        #lemmatized_data = self.lemmatize(tokenized_data, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])
        #logging.debug(lemmatized_data)
        #logging.debug(len(lemmatized_data))
        with open('tokenized_data.pkl', 'wb') as f:
            pickle.dump(tokenized_data, f)
        return 'FROM TRAINING DATA'

    def create_LDA_model(self):
        print("Started creating LDA model ...")
        tokenized_data = []
        with open('tokenized_data.pkl', 'rb') as f:
            tokenized_data = pickle.load(f)
        #print(tokenized_data)
        #self.get_old_lemmatized_data()
        try:
            id2word = corpora.Dictionary(tokenized_data)
        except TypeError as te:
            logging.exception(te)
        logging.debug('id2word done')



        corpus = [id2word.doc2bow(text) for text in tokenized_data]
        logging.debug('corpus done')
        lda_model = models.LdaModel(corpus=corpus,
                                    id2word=id2word,
                                    num_topics=self.NUM_TOPICS)

        logging.debug('LdaModel creation done')

        print("LDA Model:")

        for idx in range(self.NUM_TOPICS):
            # Print the first 50 most representative topics
            print("Topic #%s:" % idx, lda_model.print_topic(idx, 10))

        print("=" * 20)

        # datapath = /home/agniv/.local/lib/python3.6/site-packages/gensim/test/test_data
        temp_file = datapath("saved-model")
        lda_model.save(temp_file)
        return id2word

    def get_tokenized_test_data(self,id2word):
        logging.debug('STARTED GET_TOKENIZED_TEST_DATA')
        temp_file = datapath("saved-model")
        saved_lda_model = models.LdaModel.load(temp_file)
        tokenized_data = []
        #lemmatized_data = []
        print("Started tokenized data ...")
        logging.debug(self.TEST_DATA_ROOT_DIRECTORY)
        top_directory = '/home/agniv/Desktop/data-science/telegraph_scraper/'
        top_directory = top_directory+self.TEST_DATA_ROOT_DIRECTORY
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
                                        #logging.debug(words)
                                        #print(words)
                                    bow = id2word.doc2bow(words)
                                    sorted_topic_list = sorted(saved_lda_model[bow], key=lambda x: x[1],
                                                                   reverse=True)
                                    top_topic = sorted_topic_list[:1]
                                    (idx, value) = top_topic[0]
                                    top_topic_str = str(saved_lda_model.print_topic(idx, 5))
                                    top_topic_keywords = re.findall(r'"([^"]*)"', top_topic_str)
                                    top_topic_probabilities = re.findall("\d+\.\d+", top_topic_str)
                                    logging.debug('FILENAME: '+pagewise_directory+'/'+newsfile)
                                    print('FILENAME: ' + pagewise_directory + '/' + newsfile)
                                    logging.debug('TOPICS: ' + str(top_topic_keywords))
                                    print('TOPICS: ' + str(top_topic_keywords))
                                    logging.debug('TOPIC PROBABILITIES: ' + str(top_topic_probabilities))
                                    print('TOPIC PROBABILITIES: ' + str(top_topic_probabilities))
                                    #for word in words:
                                    #tokenized_data.append(words)

        #logging.debug(tokenized_data)
        #logging.debug(len(tokenized_data))
        #lemmatized_data = self.lemmatize(tokenized_data, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])
        #logging.debug(lemmatized_data)
        #logging.debug(len(lemmatized_data))
        #with open('tokenized_data.pkl', 'wb') as f:
         #   pickle.dump(tokenized_data, f)
        return 'FROM TEST DATA'

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
    def get_old_lemmatized_data(self):
        with open('lemmatized_data.pkl', 'rb') as f:
            lemmatized_data = pickle.load(f)
        logging.debug(lemmatized_data)