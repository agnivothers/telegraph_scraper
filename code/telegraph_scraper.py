from selenium import webdriver


class TelegraphScraper:

    def greeting(self,name):
        print("Hello! ",name)

    def get_browser(self):
        browser = webdriver.Chrome()
        browser.set_window_size(1024, 600)
        browser.maximize_window()
        return(browser)
    def get_telegraph_archive_home_page(self,browser):
        browser.get("https://epaper.telegraphindia.com/archives.php")
        return(browser)
    def access_archive_of_date(self,browser,date_string):
        browser.get("https://epaper.telegraphindia.com/index.php?pagedate="+date_string+"&edcode=71&subcode=71&mod=&pgnum=1&type=a")
        return(browser)