from selenium import webdriver
from bs4 import BeautifulSoup
from urllib import request


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
    def get_maps_for_date_and_page_no(self,year,month,day,page_no):
        year_first_date_string = year + "-" + month + "-" + day
        url = "https://epaper.telegraphindia.com/index.php?pagedate="+year_first_date_string+"&edcode=71&subcode=71&mod=&pgnum="+str(page_no)+"&type=a"
        html = request.urlopen(url)
        soup = BeautifulSoup(html,"lxml")
        #maps = soup.find("map",name="enewspaper1")
        maps = soup.find(attrs={'name':'Maps'})
        return maps
    def get_map_collection(self,maps):
        map_collection_all = maps.find_all_next("area")
        map_collection = []
        for tag in map_collection_all:
            if "show_pophead" in str(tag):
                map_collection.append(tag)
        return map_collection
    def get_link_from_tag(self,tag,year,month,day,page_no):
        onclick_signature_for_textview = tag.attrs['onclick']
        parameters = onclick_signature_for_textview.replace('return show_pophead(','').replace(')','').replace('\'','')
        #print(parameters)
        parameters_list = parameters.split(',')
        #print(parameters_list)
        #link = https://epaper.telegraphindia.com/textview_295380_1603269_4_1_1_01-10-2019_71_1.html
        link =  "https://epaper.telegraphindia.com/textview_{0}_{1}_{2}_1_{3}_{4}-{5}-{6}_71_1.html"\
            .format(parameters_list[0],parameters_list[1],parameters_list[2],page_no,day,month,year)
        #print(link)
        return link
    def get_bsobject_from_link(self,link):
        html = request.urlopen(link)
        soup = BeautifulSoup(html, "lxml")
        return soup
    def get_title_from_html(self,link):
        soup = self.get_bsobject_from_link(link)
        title = soup.find("title")
        return title.string
    def get_news_text(self,link):
        news_text = ''
        soup = self.get_bsobject_from_link(link)
        story_details = soup.find(class_="stry_dtl_lft")
        text_tag_collection = story_details.find_all(class_="p_txt_kj")
        for tag in text_tag_collection:
            print(tag.string)
            #text = tag.

        return news_text