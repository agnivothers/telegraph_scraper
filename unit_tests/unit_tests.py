import unittest
from selenium import webdriver
from code import telegraph_scraper
from selenium.webdriver.support.wait import WebDriverWait



class TelegraphHomePageTest(unittest.TestCase):

    def setUp(self):
        ts = telegraph_scraper.TelegraphScraper()
        self.ts = ts # Learning Python Testing, Pg. 88 How to use objects created in setUP method by other methods

    def test_telegraph_archive_page_url_load(self):
        browser = self.ts.get_browser()
        browser = self.ts.get_telegraph_archive_home_page(browser)
        self.assertIn('', browser.title)
    def test_access_a_particular_date(self):
        browser = self.ts.get_browser()
        browser = self.ts.access_archive_of_date(browser,"2019","10","01")
        self.assertEqual('Telegraph india epaper Calcutta 01 Oct 2019 | Page 1',browser.title,msg="The Title for a particular date did not match")
    def test_access_a_particular_date_and_page_no(self):
        browser = self.ts.get_browser()
        browser = self.ts.access_archive_of_date_and_page_no(browser,"2019","10","01",10)
        self.assertEqual('Telegraph india epaper Calcutta 01 Oct 2019 | Page 10',browser.title,msg="The Title or page number for a particular date and page number did not match")

if __name__ == '__main__':
    unittest.main() 
