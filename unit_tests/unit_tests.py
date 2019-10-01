import unittest
from selenium import webdriver
from code import times_scraper
from selenium.webdriver.support.wait import WebDriverWait



class TimesHomePageTest(unittest.TestCase):

    def setUp(self):
        ts = times_scraper.TimesScraper()
        self.ts = ts # Learning Python Testing, Pg. 88 How to use objects created in setUP method by other methods

    def test_times_archive_page_url_load(self):
        browser = self.ts.get_browser()
        browser = self.ts.get_times_archive_home_page(browser)
        self.assertIn('', browser.title)
    """
    def test_login_credentials(self):
        (username,password) = self.ts.get_login_credentials()
        self.assertEqual(username,"Username","The username did not match")
        self.assertEqual(password, "Password", "The password did not match")
    """
    def test_navigate_to_login_page(self):
        browser = self.ts.get_browser()
        browser = self.ts.get_times_archive_home_page(browser)
        #a = browser.find_element_by_partial_link_text("Log")
        a = browser.find_elements_by_class_name("btn.btn-primary")

        for element in a:
            element.click()

        #a = browser.find_elements_by_class_name("col-md-12")
        #a = browser.find_element_by_link_text("Log in here")
        #a = browser.find_elements_by_xpath("//div")
        print(a)
        print(browser.window_handles)
        WebDriverWait(browser, 10).until(lambda d: len(d.window_handles) == 2)
        for handle in browser.window_handles:
            print("Printing handles")
            print(handle)
            browser.switch_to.window(handle)
            print(browser.title)
            WebDriverWait(browser, 10).until(lambda d: d.title != "")
            self.assertIn('Log In', browser.title)
            """
            b = browser.switch_to.window(handle)
            print('Switched window')
            print(b)
            """

if __name__ == '__main__': 
    unittest.main() 
