from selenium import webdriver
from bs4 import BeautifulSoup
from urllib import request

class ArchiveParameters:
    year    = ""
    month   = ""
    day     = ""
    page_no = 1
    pophead_variable1 = ""
    pophead_variable2 = ""
    pophead_variable3 = ""

class TelegraphScraper:
    """
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
    """
    def get_maps_for_date_and_page_no(self,ap):
        year_first_date_string = ap.year + "-" + ap.month + "-" + ap.day
        url = "https://epaper.telegraphindia.com/index.php?pagedate="+year_first_date_string+"&edcode=71&subcode=71&mod=&pgnum="+str(ap.page_no)+"&type=a"
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

    def get_variable_parameters_from_tag(self,tag,ap):
        onclick_signature_for_textview = tag.attrs['onclick']
        parameters = onclick_signature_for_textview.replace('return show_pophead(','').replace(')','').replace('\'','')
        #print(parameters)
        parameters_list = parameters.split(',')
        #print(parameters_list)
        ap.pophead_variable1 = parameters_list[0]
        ap.pophead_variable2 = parameters_list[1]
        ap.pophead_variable3 = parameters_list[2]
        return ap

    def get_link_from_parameters(self,ap):
        # link = https://epaper.telegraphindia.com/textview_295380_1603269_4_1_1_01-10-2019_71_1.html
        link =  "https://epaper.telegraphindia.com/textview_{0}_{1}_{2}_1_{3}_{4}-{5}-{6}_71_1.html"\
            .format("295380",ap.pophead_variable2,ap.pophead_variable3,ap.page_no,ap.day,ap.month,ap.year)
        #print(link)
        return link

    def get_bsobject_from_parameters(self, ap):
        link = self.get_link_from_parameters(ap)
        html = request.urlopen(link)
        soup = BeautifulSoup(html, "lxml")
        return soup
    def get_title(self, ap):
        soup = self.get_bsobject_from_parameters(ap)
        title = soup.find("title")
        return title.string
    def get_news_text(self,ap):
        #self.maxDiff = None
        news_text = ''
        #print("THE LINK IS: "+link)
        soup = self.get_bsobject_from_parameters(ap)
        story_details = soup.find(class_="stry_dtl_lft")
        text_tag_collection = story_details.find_all(class_="p_txt_kj")
        #print(str(text_tag_collection[0]))
        first_tag = BeautifulSoup(str(text_tag_collection[0]),"lxml")
        first_tag.span.unwrap()
        #print("Printing first_tag:"+first_tag.text)
        news_text=news_text+first_tag.text
        for tag in text_tag_collection:
            if tag.string is not None:
                news_text = news_text + tag.string
            #print("Printing tags ...")
            #print(tag.string)
            #text = tag.
        print(news_text)
        return news_text
    def get_news_text_from_first_tag(self,first_tag):
        #text = ''
        first_tag.span.unwrap()
        text = first_tag.text
        return text
        #text = text+first_tag.span.string
        #new_tag =