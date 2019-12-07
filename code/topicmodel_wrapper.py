from code import topic_model
def topicmodel():
    tm  = topic_model.Topicmodel()
    tm.EXTRACTED_DATA_ROOT_DIRECTORY = 'data/extracted_data/'
    print("Topicmodel program started ...")
    tm.get_lemmatized_data()
    tm.create_LDA_model()

def main():
    topicmodel()

if __name__=="__main__":
  main()