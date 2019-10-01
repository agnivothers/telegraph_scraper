from selenium import webdriver
import unittest

class LoginTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_login(self):
        self.browser.get("https://epaper.timesgroup.com/TOI/TimesOfIndia/indialogin.aspx")
        self.assertIn('', self.browser.title)
        self.fail('Finish the test!')

if __name__=='__main__':
    unittest.main()
