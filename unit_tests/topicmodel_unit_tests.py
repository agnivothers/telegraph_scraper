import unittest
from code import topicmodel

class TopicmodelTest(unittest.TestCase):
    tm = topicmodel.Topicmodel()
    def setUp(self):
        pass

    def test_get_lemmatized_data(self):
        lemmatized_data1 = self.get_lemmatized_data_for_june_2018_to_nov_2019()
        lemmatized_data2 = self.tm.get_lemmatized_data()
        self.assertEqual(lemmatized_data1,lemmatized_data2)

    def get_lemmatized_data_for_june_2018_to_nov_2019(self):
        return 'Dummy test'

if __name__ == '__main__':
    unittest.main()