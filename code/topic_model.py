from __future__ import with_statement
from grizzled.os import working_directory
import logging
import os

logging.basicConfig(filename='topic_model.log', level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')

class Topicmodel:
    EXTRACTED_DATA_ROOT_DIRECTORY = ''
    def get_lemmatized_data(self):
        print("Started lemmatizing data ...")
        print(self.EXTRACTED_DATA_ROOT_DIRECTORY)
        top_directory = '/home/agniv/Desktop/data-science/telegraph_scraper/'
        top_directory = top_directory+self.EXTRACTED_DATA_ROOT_DIRECTORY
        with working_directory(top_directory):
            datewise_directories = sorted(os.listdir(top_directory))
            for datewise_directory in datewise_directories:
                datewise_directory = top_directory + datewise_directory
                print(datewise_directory)
                with working_directory(datewise_directory):
                    pagewise_directories = sorted(os.listdir(datewise_directory))
                    for pagewise_directory in pagewise_directories:
                        pagewise_directory = datewise_directory + '/' + pagewise_directory
                        print(pagewise_directory)
                        with working_directory(pagewise_directory):
                            newsfiles = sorted(os.listdir(pagewise_directory))
                            for newsfile in newsfiles:
                                print(newsfile)



        return ''

    def create_LDA_model(self):
        print("Started creating LDA model ...")

