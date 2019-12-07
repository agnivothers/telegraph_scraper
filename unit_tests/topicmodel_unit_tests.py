import unittest
from code import topic_model

class TopicmodelTest(unittest.TestCase):
    tm = topic_model.Topicmodel()
    tm.EXTRACTED_DATA_ROOT_DIRECTORY = 'test_data/extracted_data/'
    tm.NUM_TOPICS = 50
    def setUp(self):
        pass

    def test_get_lemmatized_data(self):
        lemmatized_data1 = self.get_lemmatized_data_for_june_2018_to_nov_2019()
        lemmatized_data2 = self.tm.get_lemmatized_data()
        self.assertEqual(lemmatized_data1,lemmatized_data2)

    def test_get_LDAModel(self):
        LDAModel1 = self.get_LDAModel_for_june_2018_to_nov_2019()
        LDAModel2 = self.tm.create_LDA_model()
        self.assertEqual(LDAModel1,LDAModel2)

    def get_lemmatized_data_for_june_2018_to_nov_2019(self):
        return 'Dummy test'
    def get_LDAModel_for_june_2018_to_nov_2019(self):
        return 'Dummy model'

if __name__ == '__main__':
    unittest.main()