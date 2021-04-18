from code import topic_model
def topicmodel():
    tm  = topic_model.Topicmodel()
    tm.TRAINING_DATA_ROOT_DIRECTORY = 'data/covid-paper-data/training-data/'
    tm.TEST_DATA_ROOT_DIRECTORY = 'data/covid-paper-data/2020/April/'
    tm.NUM_TOPICS = 50
    print("Topicmodel program started ...")
    #tm.get_tokenized_training_data()
    tokenized_data = tm.get_tokenized_data()
    id2word = tm.get_id2word(tokenized_data)
    #tm.create_LDA_model(id2word, tokenized_data)    
    topic_news_article_dict = tm.get_topic_news_article_dict(id2word)
    tm.plot_histogram(topic_news_article_dict)

def main():
    topicmodel()

if __name__=="__main__":
  main()
