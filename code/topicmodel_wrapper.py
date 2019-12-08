from code import topic_model
def topicmodel():
    tm  = topic_model.Topicmodel()
    tm.TRAINING_DATA_ROOT_DIRECTORY = 'data/extracted_data/training_data/'
    tm.TEST_DATA_ROOT_DIRECTORY = 'data/extracted_data/test_data/'
    tm.NUM_TOPICS = 50
    print("Topicmodel program started ...")
    tm.get_tokenized_training_data()
    tm.create_LDA_model()

def main():
    topicmodel()

if __name__=="__main__":
  main()