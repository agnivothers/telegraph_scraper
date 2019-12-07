from code import topicmodel
def topicmodel(self):
    tm  = topicmodel.Topicmodel()
    print("Topicmodel program started ...")
    tm.get_lemmatized_data()
    tm.create_LDA_model()

def main():
    topicmodel()

if __name__=="__main__":
  main()