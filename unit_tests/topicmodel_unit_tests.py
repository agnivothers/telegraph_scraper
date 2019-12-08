import unittest
from code import topic_model

class TopicmodelTest(unittest.TestCase):
    tm = topic_model.Topicmodel()
    tm.TRAINING_DATA_ROOT_DIRECTORY = 'test_data/extracted_data/training_data/'
    tm.TEST_DATA_ROOT_DIRECTORY = 'test_data/extracted_data/test_data/'
    tm.NUM_TOPICS = 50
    def setUp(self):
        pass

    def test_get_tokenized_training_data(self):
        tokenized_training_data1 = self.get_tokenized_training_data_for_june_2018_to_aug_2019()
        tokenized_training_data2 = self.tm.get_tokenized_training_data()
        self.assertEqual(tokenized_training_data1,tokenized_training_data2)

    def test_get_LDAModel(self):
        LDAModel1 = self.get_LDAModel_for_june_2018_to_aug_2019()
        LDAModel2 = self.tm.create_LDA_model()
        self.assertEqual(LDAModel1,LDAModel2)
    def test_get_tokenized_test_data(self):
        tokenized_test_data1 = self.get_tokenized_test_data_for_sep_2019_to_nov_2019()
        id2word = self.tm.create_LDA_model()
        tokenized_test_data2 = self.tm.get_tokenized_test_data(id2word)
        self.assertEqual(tokenized_test_data1,tokenized_test_data2)

    def get_tokenized_training_data_for_june_2018_to_aug_2019(self):
        return 'Dummy training data'
    def get_tokenized_test_data_for_sep_2019_to_nov_2019(self):
        return 'Dummy test data'
    def get_LDAModel_for_june_2018_to_aug_2019(self):
        return 'Dummy model'

if __name__ == '__main__':
    unittest.main()