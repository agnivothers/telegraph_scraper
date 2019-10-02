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
    def access_archive_of_date(self,browser,year,month,day):
        year_first_date_string = year+"-"+month+"-"+day
        browser.get("https://epaper.telegraphindia.com/index.php?pagedate="+year_first_date_string+"&edcode=71&subcode=71&mod=&pgnum=1&type=a")
        return(browser)
    def access_archive_of_date_and_page_no(self,browser,year,month,day,page_no):
        year_first_date_string = year + "-" + month + "-" + day
        browser.get("https://epaper.telegraphindia.com/index.php?pagedate="+year_first_date_string+"&edcode=71&subcode=71&mod=&pgnum="+str(page_no)+"&type=a")
        return(browser)