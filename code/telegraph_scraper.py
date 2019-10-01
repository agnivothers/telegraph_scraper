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
        browser.get("https://epaper.telegraphgroup.com/TOI/TelegraphOfIndia/indialogin.aspx")
        return(browser)
