from selenium import webdriver
from bs4 import BeautifulSoup
from urllib import request
from urllib import error
import os
import wget
import re
from datetime import date
from datetime import timedelta
import random
import logging
logging.basicConfig(filename='telegraph_scraper.log', level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')

class ArchiveParameters:
    year    = ""
    month   = ""
    day     = ""
    page_no = 0
    pophead_variable1 = ""
    pophead_variable2 = ""
    pophead_variable3 = ""

class FileStorageParameters:
    DOWNLOADED_DATA_ROOT_DIRECTORY = ''
    EXTRACTED_DATA_ROOT_DIRECTORY = ''

class TelegraphScraper:

    def populate_archive_parameters_from_download_date(self,ap,download_date):
        ap.year = str(download_date.year)
        if(download_date.month) < 10:
            ap.month="0"+str(download_date.month)
        else:
            ap.month = str(download_date.month)
        if(download_date.day) < 10:
            ap.day="0"+str(download_date.day)
        else:
            ap.day = str(download_date.day)
        return ap

    def get_random_integer(self):
        return random.randint(1,10000000)
    def get_full_page_url(self, ap):
        year_first_date_string = ap.year + "-" + ap.month + "-" + ap.day
        url = "https://epaper.telegraphindia.com/index.php?pagedate="+year_first_date_string+"&edcode=71&subcode=71&mod=&pgnum="+str(ap.page_no)+"&type=a"
        return url

    def get_total_number_of_pages(self, ap):
        url = self.get_full_page_url(ap)
        html = request.urlopen(url)
        soup = BeautifulSoup(html,"lxml")
        totalpages = soup.find('input', {'id': 'totalpages'}).get('value')
        logging.debug('total number of pages: ' + totalpages)
        return int(totalpages)

    def get_maps_for_date_and_page_no(self,ap):
        url = self.get_full_page_url(ap)
        logging.debug("full page url: "+url)
        html = request.urlopen(url)
        soup = BeautifulSoup(html,"lxml")
        maps = soup.find(attrs={'name':'Maps'})
        #logging.debug(maps)
        return maps
    def get_map_collection(self,maps):
        map_collection_all = maps.find_all_next("area")
        map_collection = []
        function_name_to_replace = ''
        #logging.debug('map_collection_all: '+str(map_collection_all))
        for tag in map_collection_all:
            if "show_pophead" in str(tag):
                #function_name_to_replace = 'show_pophead'
                map_collection.append(tag)
            """
            else:
                if "show_pop" in str(tag):
                    function_name_to_replace = 'show_pop'
                    map_collection.append(tag)
            """
        if len(map_collection)==0:
            return None
        else:
            return map_collection

    #def get_variable_parameters_from_tag(self,tag,ap,function_name_to_replace):
    def get_variable_parameters_from_tag(self, tag, ap):
        try:
            onclick_signature_for_textview = tag.attrs['onclick']
            parameters = onclick_signature_for_textview.replace('return show_pophead(','').replace(')','').replace('\'','')
            parameters_list = parameters.split(',')
            ap.pophead_variable1 = parameters_list[0]
            ap.pophead_variable2 = parameters_list[1]
            ap.pophead_variable3 = parameters_list[2]
            #logging.debug('pophead_variable1: '+ap.pophead_variable1)
            #logging.debug('pophead_variable2: ' + ap.pophead_variable2)
            #logging.debug('pophead_variable3: ' + ap.pophead_variable3)
        except Exception as e:
            logging.debug(e)

        """
        onclick_signature_for_textview = tag.attrs['onclick']
        logging.debug('onclick_signature_for_textview: '+onclick_signature_for_textview)
        logging.debug('function_name_to_replace: '+function_name_to_replace)
        #parameters = onclick_signature_for_textview.replace('return '+ function_name_to_replace+'(', '').replace(')', '').replace('\'','')
        function_name_replaced = onclick_signature_for_textview.replace('return '+ function_name_to_replace+'(', '')
        logging.debug('function_name_replaced: '+function_name_replaced)
        parameters = onclick_signature_for_textview.replace('return '+ function_name_to_replace+'(', '').replace(')', '').replace('\'','')

        logging.debug('PARAMETERS: '+parameters)
        parameters_list = parameters.split(',')
        ap.pophead_variable1 = parameters_list[0]
        ap.pophead_variable2 = parameters_list[1]
        ap.pophead_variable3 = parameters_list[2]
        """
        return ap

    def get_link_from_parameters(self,ap):
        # link = https://epaper.telegraphindia.com/textview_295380_1603269_4_1_1_01-10-2019_71_1.html
        link =  "https://epaper.telegraphindia.com/textview_{0}_{1}_{2}_1_{3}_{4}-{5}-{6}_71_1.html"\
            .format(ap.pophead_variable1,ap.pophead_variable2,ap.pophead_variable3,ap.page_no,ap.day,ap.month,ap.year)
        logging.debug('link: '+link)
        return link

    def get_folder_name_to_store_downloaded_data(self, ap, fsp):
        return fsp.DOWNLOADED_DATA_ROOT_DIRECTORY+ap.year+"-"+ap.month+"-"+ap.day+"/"

    def get_folder_name_to_store_extracted_data(self, ap, fsp, file):
        return fsp.EXTRACTED_DATA_ROOT_DIRECTORY+ap.year+"-"+ap.month+"-"+ap.day+"/"+file+"/"

    def download_and_get_saved_web_page_path(self, ap, fsp):
        folder_name = self.get_folder_name_to_store_downloaded_data(ap, fsp)
        link = self.get_link_from_parameters(ap)
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        file_name = folder_name+str(ap.page_no)
        if os.path.exists(file_name):
            os.remove(file_name)
        try:
            wget.download(link, file_name)
        except error.HTTPError as he:
            logging.debug("PROBLEM WITH LINK: "+link)
            logging.debug("CANNOT DOWNLOAD FOR " + ap.day + "-" + ap.month + "-" + ap.year + " FOR PAGE NO: " + str(ap.page_no))
            #logging.exception(he)
        return file_name

    def get_div_ids_from_downloaded_file(self, file_name):
        soup = ''
        try:
            with open(file_name, "r") as downloaded_file:
                soup = BeautifulSoup(downloaded_file, "lxml")
        except UnicodeDecodeError as ude:
            #logging.exception(ude)
            logging.debug("FILE NAME WHERE UNICODEDECODEERROR OCCURRED: " + file_name)
            return

        id_regex = re.compile("id-\d+")
        all_div_ids = soup.find_all(id=id_regex)
        return all_div_ids

    def get_news_title(self, div_id):
        title = div_id.find(class_="sub_head haedlinesstory1")
        if title == None:
            title = div_id.find(class_="books_text haedlinesstory1")
        return title.string.strip()

    def get_news_text(self,div_id):
        #logging.debug('div_id: ')
        #logging.debug(div_id)
        news_text = ''
        text_tag_collection = div_id.find_all(class_="p_txt_kj")
        #logging.debug('text_tag_collection: ')
        #logging.debug(text_tag_collection)

        first_tag = BeautifulSoup(str(text_tag_collection[0]),"lxml")

        first_tag.span.unwrap()
        news_text=news_text+first_tag.text
        for tag in text_tag_collection:
            if tag.string is not None:
                news_text = news_text + tag.string
        return news_text

    def get_news_text_from_first_tag(self,first_tag):
        first_tag.span.unwrap()
        text = first_tag.text
        return text

    def save_extracted_data(self,title,text,ap, fsp, file):

        folder_name = self.get_folder_name_to_store_extracted_data(ap, fsp, file)
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        if title == '':
            title = text[:250]
            logging.debug("NO TITLE PRESENT, HENCE TAKING FROM TEXT: "+title)
        if '/' in title:
            title = title.replace('/','-')
            logging.debug("TITLE CONTAINED / WHICH IS REPLACED BY - : "+title)
        if len(title)>250:
            title = title[:250]
            logging.debug("HUGE TITLE STRING, HENCE TAKING ONLY FIRST 250 CHARACTERS: " + title)
        file_path = folder_name + title
        with open(file_path, 'w') as f:
            f.write(text)
        return file_path

    def download_data_that_raised_exception_in_first_pass(self):
        not_downloaded_links_file = "not.downloaded.links"
        with open(not_downloaded_links_file,'r') as file_name:
            ROOT_FOLDER_NAME = 'data/downloaded_data/'
            for line_no,line in enumerate(file_name):
                line = line.strip()
                split_line = line.split("PROBLEM WITH LINK: ")
                link = split_line[1]
                parameters = link.split('_')
                download_missed_page_no = parameters[5]
                download_missed_date = parameters[6]
                #print(download_missed_date)
                date_components = download_missed_date.split('-')
                download_missed_date = date_components[2]+'-'+date_components[1]+'-'+date_components[0]
                print(download_missed_date)
                print(download_missed_page_no)
                folder_name = ROOT_FOLDER_NAME+download_missed_date+'/'
                if not os.path.exists(folder_name):
                    logging.debug("FOLDER NAME: "+folder_name+" NOT PRESENT")
                file_name = folder_name+download_missed_page_no
                logging.debug(file_name)
                print()
                if os.path.exists(file_name):
                    os.remove(file_name)
                try:
                    wget.download(link, file_name)
                except error.HTTPError as he:
                    logging.debug("PROBLEM WITH LINK: "+link)
                    logging.debug("CANNOT DOWNLOAD FOR " + download_missed_date + " FOR PAGE NO: " + download_missed_page_no)


        """
        try:
            folder_name = self.get_folder_name_to_store_extracted_data(ap, fsp)
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)
            if title=='':
                title = text.split(':')[0]
            file_path = folder_name+title
            with open(file_path, 'w') as f:
                f.write(text)
            return file_path
        except Exception as e:
            logging.debug(e)
        """
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
