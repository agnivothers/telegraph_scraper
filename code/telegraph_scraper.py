from selenium import webdriver
from code import login_credentials


class TimesScraper:

    def greeting(self,name):
        print("Hello! ",name)

    def get_browser(self):
        browser = webdriver.Chrome()
        browser.set_window_size(1024, 600)
        browser.maximize_window()
        return(browser)
    def get_times_archive_home_page(self,browser):
        browser.get("https://epaper.timesgroup.com/TOI/TimesOfIndia/indialogin.aspx")
        #print(login_credentials.username,login_credentials.password)
        return(browser)
    """
    def get_login_credentials(self):
        return(login_credentials.username,login_credentials.password)
    """
