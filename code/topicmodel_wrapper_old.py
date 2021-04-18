from code import topic_model
def topicmodel():
    tm  = topic_model.Topicmodel()
    tm.TRAINING_DATA_ROOT_DIRECTORY = 'data/covid-paper-data/training-data/'
    tm.TEST_DATA_ROOT_DIRECTORY = 'data/covid-paper-data/2020/April/'
    tm.NUM_TOPICS = 50
    print("Topicmodel program started ...")
    tm.get_tokenized_training_data()
    id2word = tm.create_LDA_model()
    tm.get_tokenized_test_data(id2word)

def main():
    topicmodel()

if __name__=="__main__":
  main()
