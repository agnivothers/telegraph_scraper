import unittest
from selenium import webdriver
from code import telegraph_scraper
from selenium.webdriver.support.wait import WebDriverWait
from datetime import date
from datetime import timedelta


class TelegraphHomePageTest(unittest.TestCase):
    def setUp(self):
        ts = telegraph_scraper.TelegraphScraper()
        self.ts = ts # Learning Python Testing, Pg. 88 How to use objects created in setUP method by other methods
        ap = telegraph_scraper.ArchiveParameters()
        ap.year = "2019"
        ap.month = "10"
        ap.day = "01"
        ap.page_no = 1
        self.ap = ap
        fsp = telegraph_scraper.FileStorageParameters()
        fsp.DOWNLOADED_DATA_ROOT_DIRECTORY = 'test_data/downloaded_data/'
        fsp.EXTRACTED_DATA_ROOT_DIRECTORY = 'test_data/extracted_data/'
        self.fsp = fsp

    def test_get_variable_parameters_from_tag(self):
        maps = self.ts.get_maps_for_date_and_page_no(self.ap)
        map_collection1 = self.ts.get_map_collection(maps)
        self.ap = self.ts.get_variable_parameters_from_tag(map_collection1[0],self.ap)
        self.assertEqual(self.ap.pophead_variable1,"295380","First pophead variable did not match.")
        self.assertEqual(self.ap.pophead_variable2, "1603269", "Second pophead variable did not match.")
        self.assertEqual(self.ap.pophead_variable3, "4", "Third pophead variable did not match.")

    def test_populate_archive_parameters_from_download_date(self):
        ap1 = telegraph_scraper.ArchiveParameters()
        download_date = date(2019,10,1)
        ap1 = self.ts.populate_archive_parameters_from_download_date(ap1,download_date)
        ap2 = self.get_filled_up_ap()
        self.assertEqual(ap1.year,ap2.year)
        self.assertEqual(ap1.month, ap2.month)
        self.assertEqual(ap1.day, ap2.day)

    def test_get_link_from_parameters(self):
        ap = self.get_filled_up_ap()
        link1 = self.ts.get_link_from_parameters(ap)
        link2 = self.get_first_link_from_tag_for_2019_10_01()
        self.assertEqual(link1,link2,"The links did not match.")

    def test_download_and_get_saved_web_page_path(self):
        ap = self.get_filled_up_ap()
        fsp = self.fsp
        #link = self.ts.get_link_from_parameters(ap)
        path1 = self.ts.download_and_get_saved_web_page_path(ap, fsp)
        path2 = self.get_saved_web_page_file_name_for_2019_01_01_page_01()
        self.assertEqual(path1,path2,"The downloaded texts did not match.")

    def test_get_bsobject_from_downloaded_file(self):
        all_div_ids = self.get_div_ids()
        self.assertEqual(9,len(all_div_ids),"The number of div ids do not match.")

    def test_get_news_title(self):
        all_div_ids = self.get_div_ids()
        title1 = self.ts.get_news_title(all_div_ids[0])
        title2 = self.get_news_title_for_2019_10_01()
        self.assertEqual(title1, title2, "The titles did not match.")

    def get_news_title_for_2019_10_01(self):
        return 'Riot relief delay rap on Gujarat'

    def test_get_news_text(self):
        self.maxDiff = None
        all_div_ids = self.get_div_ids()
        text1 = self.ts.get_news_text(all_div_ids[0])
        text2 = self.get_news_text_for_2019_10_01()
        self.assertEqual(text1,text2,"The news texts did not match.")

    def test_get_folder_name_to_store_downloaded_data(self):
        ap = self.get_filled_up_ap()
        fsp = self.fsp
        folder_name1 = self.ts.get_folder_name_to_store_downloaded_data(ap, fsp)
        folder_name2 = fsp.DOWNLOADED_DATA_ROOT_DIRECTORY+"2019-10-01/"
        self.assertEqual(folder_name1,folder_name2,"The folder names do not match.")

    def test_get_folder_name_to_store_extracted_data(self):
        ap = self.get_filled_up_ap()
        fsp = self.fsp
        folder_name1 = self.ts.get_folder_name_to_store_extracted_data(ap, fsp)
        folder_name2 = fsp.EXTRACTED_DATA_ROOT_DIRECTORY+"2019-10-01/1/"
        self.assertEqual(folder_name1,folder_name2,"The folder names do not match.")

    def test_save_extracted_data(self):
        ap = self.get_filled_up_ap()
        fsp = self.fsp
        title = self.get_news_title_for_2019_10_01()
        text = self.get_news_text_for_2019_10_01()
        file_path1 = self.ts.save_extracted_data(title,text, ap, fsp)
        file_path2 = self.get_extracted_data_file_name()
        #text1 = self.get_extracted_data_file_text()
        #text2 = self.get_test_data_extracted_data_file_text()
        self.assertEqual(file_path1,file_path2)

    def test_get_full_page_url(self):
        ap = self.get_filled_up_ap()
        link1 = self.ts.get_full_page_url(ap)
        link2 = self.get_first_page_url_for_2019_01_01()
        self.assertEqual(link1,link2)
    def test_get_total_pages(self):
        ap = self.get_filled_up_ap()
        no_of_pages1 = self.ts.get_total_number_of_pages(ap)
        no_of_pages2 = self.get_number_of_pages_for_2019_01_01()
        self.assertEqual(no_of_pages1,no_of_pages2)

    def get_number_of_pages_for_2019_01_01(self):
        return 22
    def get_extracted_data_file_name(self):
        return self.fsp.EXTRACTED_DATA_ROOT_DIRECTORY+'2019-10-01/1/Riot relief delay rap on Gujarat'

    def get_first_page_url_for_2019_01_01(self):
        return "https://epaper.telegraphindia.com/index.php?pagedate=2019-10-01&edcode=71&subcode=71&mod=&pgnum=1&type=a"
    def get_extracted_data_file_text(self):
        file_name = self.get_extracted_data_file_name()
        with open(file_name, "r") as content_file:
            text = content_file.read()
        print(text)
        return text

    def get_test_data_extracted_data_file_name(self):
        return self.fsp.EXTRACTED_DATA_ROOT_DIRECTORY+'2019-10-01/1/Riot relief delay rap on Gujarat'

    def get_test_data_extracted_data_file_text(self):
        file_name = self.get_test_data_extracted_data_file_name()
        with open(file_name, "r") as content_file:
            text = content_file.read()
        print(text)
        return text
    def get_div_ids(self):
        file_name = self.get_saved_web_page_file_name_for_2019_01_01_page_01()
        all_div_ids = self.ts.get_div_ids_from_downloaded_file(file_name)
        return all_div_ids

    def get_filled_up_ap(self):
        maps = self.ts.get_maps_for_date_and_page_no(self.ap)
        map_collection1 = self.ts.get_map_collection(maps)
        ap = self.ts.get_variable_parameters_from_tag(map_collection1[0],self.ap)
        return ap

    def get_saved_web_page_file_name_for_2019_01_01_page_01(self):
        return self.fsp.DOWNLOADED_DATA_ROOT_DIRECTORY+'2019-10-01/1'

    def get_news_text_for_2019_10_01(self):
        return 'New Delhi: The Supreme Court on Monday got the Gujarat government to undertake to pay Rs 50 lakh to a ' \
               'gang-rape victim of the 2002 riots and give her a job "within two weeks", rapping the state for sitting' \
               ' on its April 22 order granting the same compensation. "Why haven\'t you paid the compensation so far in' \
               ' terms of our order?" Chief Justice Ranjan Gogoi asked solicitorgeneral Tushar Mehta, who appeared for ' \
               'the Gujarat government. Mehta said the state wanted to seek a review of the April 22 order, and had ' \
               'therefore delayed its execution. He sought at least another four weeks. But the chief justice said: ' \
               '"Even two weeks is more than enoughWhile recording the state\'s undertaking, the bench added at Mehta\'s' \
               ' request that the directive was being issued in the "peculiar facts and circumstances" of the case, lest' \
               ' the Rs 50-lakh award become a precedent for all rape cases. The bench, which included Justices S.A. ' \
               'Bobde and Abdul Nazeer, was hearing a contempt petition from the victim. The woman was aged 21 and five' \
               ' months pregnant when she was gang-raped by a mob that killed seven of her relatives. After Monday\'s ' \
               'court order, her husband accused the Gujarat government of "not providing any assistance" all these ' \
               'years, PTI reported. "The Supreme Court in April ordered compensation within 15 days. It\'s been more ' \
               'than five months but the state government did not contact us even once," he said..'

    def get_map_collection_for_2019_10_01(self):
        return []
    def get_first_link_from_tag_for_2019_10_01(self):
        return 'https://epaper.telegraphindia.com/textview_295380_1603269_4_1_1_01-10-2019_71_1.html'

    def get_maps_for_2019_10_01(self):
        maps = ""
        """
        <map name="Maps"><area shape="rect" class="borderimage" coords="373,589,729,1144" href="#" onclick="return show_pop('295380','16016245','4')" onmouseover="borderit(this,'black','')" onmouseout="borderit(this,'white')" data-tooltip=""> 
<area shape="rect" class="borderimage" coords="285,685,367,742" href="#" onclick="return show_pophead('295380','1603269','4')" onmouseover="borderit(this,'black',' Riot relief delay rap on Gujarat <br /><p>New Delhi: The Supreme Cour.....')" onmouseout="borderit(this,'white')" data-tooltip="<b> Riot relief delay rap on Gujarat </b><br /><p>New Delhi: The Supreme Cour....."> 
<area shape="rect" class="borderimage" coords="281,680,372,1144" href="#" onclick="return show_pop('295380','1603269','4')" onmouseover="borderit(this,'black',' Riot relief delay rap on Gujarat <br /><p>New Delhi: The Supreme Cour.....')" onmouseout="borderit(this,'white')" data-tooltip="<b> Riot relief delay rap on Gujarat </b><br /><p>New Delhi: The Supreme Cour....."> 
<area shape="rect" class="borderimage" coords="104,250,185,350" href="#" onclick="return show_pophead('295380','16010406','4')" onmouseover="borderit(this,'black',' India s worst-kept secrets, told by Rajan <br /><p>Mumbai: Former Reserve Bank.....')" onmouseout="borderit(this,'white')" data-tooltip="<b> India s worst-kept secrets, told by Rajan </b><br /><p>Mumbai: Former Reserve Bank....."> 
<area shape="rect" class="borderimage" coords="98,246,731,358" href="#" onclick="return show_pop('295380','16010406','4')" onmouseover="borderit(this,'black',' India s worst-kept secrets, told by Rajan <br /><p>Mumbai: Former Reserve Bank.....')" onmouseout="borderit(this,'white')" data-tooltip="<b> India s worst-kept secrets, told by Rajan </b><br /><p>Mumbai: Former Reserve Bank....."> 
<area shape="rect" class="borderimage" coords="105,685,276,739" href="#" onclick="return show_pophead('295380','16050366','4')" onmouseover="borderit(this,'black',' Kashmir thrust Shah missed <br /><p>New Delhi: Malaysian Prime .....')" onmouseout="borderit(this,'white')" data-tooltip="<b> Kashmir thrust Shah missed </b><br /><p>New Delhi: Malaysian Prime ....."> 
<area shape="rect" class="borderimage" coords="98,680,281,919" href="#" onclick="return show_pop('295380','16050366','4')" onmouseover="borderit(this,'black',' Kashmir thrust Shah missed <br /><p>New Delhi: Malaysian Prime .....')" onmouseout="borderit(this,'white')" data-tooltip="<b> Kashmir thrust Shah missed </b><br /><p>New Delhi: Malaysian Prime ....."> 
<area shape="rect" class="borderimage" coords="102,387,281,505" href="#" onclick="return show_pophead('295380','1621585','4')" onmouseover="borderit(this,'black',' Questions on transfer of judges <br /><p>New Delhi: The separate dec.....')" onmouseout="borderit(this,'white')" data-tooltip="<b> Questions on transfer of judges </b><br /><p>New Delhi: The separate dec....."> 
<area shape="rect" class="borderimage" coords="98,358,731,680" href="#" onclick="return show_pop('295380','1621585','4')" onmouseover="borderit(this,'black',' Questions on transfer of judges <br /><p>New Delhi: The separate dec.....')" onmouseout="borderit(this,'white')" data-tooltip="<b> Questions on transfer of judges </b><br /><p>New Delhi: The separate dec....."> 
<area shape="rect" class="borderimage" coords="14,815,98,913" href="#" onclick="return show_pop('295380','16336469','4')" onmouseover="borderit(this,'black','')" onmouseout="borderit(this,'white')" data-tooltip=""> 
<area shape="rect" class="borderimage" coords="10,524,97,626" href="#" onclick="return show_pop('295380','16332149','4')" onmouseover="borderit(this,'black','')" onmouseout="borderit(this,'white')" data-tooltip=""> 
<area shape="rect" class="borderimage" coords="18,279,96,336" href="#" onclick="return show_pophead('295380','1635637','4')" onmouseover="borderit(this,'black',' Core industries shrink <br /><p>¡ NEW DELHI: The eight cor.....')" onmouseout="borderit(this,'white')" data-tooltip="<b> Core industries shrink </b><br /><p>¡ NEW DELHI: The eight cor....."> 
<area shape="rect" class="borderimage" coords="10,252,96,425" href="#" onclick="return show_pop('295380','1635637','4')" onmouseover="borderit(this,'black',' Core industries shrink <br /><p>¡ NEW DELHI: The eight cor.....')" onmouseout="borderit(this,'white')" data-tooltip="<b> Core industries shrink </b><br /><p>¡ NEW DELHI: The eight cor....."> 
<area shape="rect" class="borderimage" coords="13,731,90,743" href="#" onclick="return show_pophead('295380','16347293','4')" onmouseover="borderit(this,'black',' 21 die in accident <br /><p>AHMEDABAD: At least 21 peop.....')" onmouseout="borderit(this,'white')" data-tooltip="<b> 21 die in accident </b><br /><p>AHMEDABAD: At least 21 peop....."> 
<area shape="rect" class="borderimage" coords="9,725,98,815" href="#" onclick="return show_pop('295380','16347293','4')" onmouseover="borderit(this,'black',' 21 die in accident <br /><p>AHMEDABAD: At least 21 peop.....')" onmouseout="borderit(this,'white')" data-tooltip="<b> 21 die in accident </b><br /><p>AHMEDABAD: At least 21 peop....."> 
<area shape="rect" class="borderimage" coords="9,19,732,243" href="#" onclick="return show_pop('295380','15591945','4')" onmouseover="borderit(this,'black','')" onmouseout="borderit(this,'white')" data-tooltip=""> 
<area shape="rect" class="borderimage" coords="15,430,83,445" href="#" onclick="return show_pophead('295380','16326797','4')" onmouseover="borderit(this,'black',' Electoral bonds <br /><p>NEW DELHI: The government o.....')" onmouseout="borderit(this,'white')" data-tooltip="<b> Electoral bonds </b><br /><p>NEW DELHI: The government o....."> 
<area shape="rect" class="borderimage" coords="7,427,97,521" href="#" onclick="return show_pop('295380','16326797','4')" onmouseover="borderit(this,'black',' Electoral bonds <br /><p>NEW DELHI: The government o.....')" onmouseout="borderit(this,'white')" data-tooltip="<b> Electoral bonds </b><br /><p>NEW DELHI: The government o....."> 
<area shape="rect" class="borderimage" coords="15,633,94,646" href="#" onclick="return show_pophead('295380','16432637','4')" onmouseover="borderit(this,'black',' Kashmir hearings <br /><p>NEW DELHI: The Supreme Cour.....')" onmouseout="borderit(this,'white')" data-tooltip="<b> Kashmir hearings </b><br /><p>NEW DELHI: The Supreme Cour....."> 
<area shape="rect" class="borderimage" coords="7,629,96,723" href="#" onclick="return show_pop('295380','16432637','4')" onmouseover="borderit(this,'black',' Kashmir hearings <br /><p>NEW DELHI: The Supreme Cour.....')" onmouseout="borderit(this,'white')" data-tooltip="<b> Kashmir hearings </b><br /><p>NEW DELHI: The Supreme Cour....."> 
<area shape="rect" class="borderimage" coords="9,940,278,969" href="#" onclick="return show_pophead('295380','16125109','4')" onmouseover="borderit(this,'black',' Tenzing II, Everest rescuer <br /><p>Darjeeling: When " everest"="" .....')"="" onmouseout="borderit(this,'white')" data-tooltip="<b> Tenzing II, Everest rescuer </b><br /><p>Darjeeling: When " ....."=""> 
<area shape="rect" class="borderimage" coords="7,920,281,1136" href="#" onclick="return show_pop('295380','16125109','4')" onmouseover="borderit(this,'black',' Tenzing II, Everest rescuer <br /><p>Darjeeling: When " everest"="" .....')"="" onmouseout="borderit(this,'white')" data-tooltip="<b> Tenzing II, Everest rescuer </b><br /><p>Darjeeling: When " ....."=""> 
</map>
        """
        return maps


if __name__ == '__main__':
    unittest.main()

    """
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

    def test_get_maps(self):
        #browser = self.ts.get_browser()
        #browser = self.ts.access_archive_of_date_and_page_no(browser, "2019", "10", "01", 1)
        maps1 = self.ts.get_maps_for_date_and_page_no("2019", "10", "01", 1)
        #print((type(map1)))
        maps2 = self.get_maps_for_2019_10_01()

        self.assertEqual(maps1,maps2,"The maps did not match.")

    def test_get_map(self):
        maps = self.ts.get_maps_for_date_and_page_no("2019", "10", "01", 1)
        map_collection1 = self.ts.get_map_collection(maps)
        map_collection2 = self.get_map_collection_for_2019_10_01()
        self.assertEqual(map_collection1, map_collection2,"The map collections did not match.")

    def test_get_link_from_tag(self):
        maps = self.ts.get_maps_for_date_and_page_no(self.ap)
        map_collection1 = self.ts.get_map_collection(maps)
        link1 = self.ts.get_link_from_tag(map_collection1[0],self.ap)
        link2 = self.get_first_link_from_tag_for_2019_10_01()
        self.assertEqual(link1, link2,"The links did not match.")

    def test_get_title(self):
        file_name = self.get_saved_web_page_file_name_for_2019_01_01_page_01()
        title1 = self.ts.get_news_title(file_name)
        title2 = 'Riot relief delay rap on Gujarat '
        self.assertEqual(title1, title2,"The titles did not match.")


    def test_get_news_text(self):
        self.maxDiff = None
        link = self.get_first_link_from_tag_for_2019_10_01()
        text1 = self.ts.get_news_text(self.ap)
        text2 = self.get_news_text_for_2019_10_01()
        self.assertEqual(text1,text2,"The news texts did not match.")

    def test_get_news_text_from_first_tag(self):
        first_tag = self.get_first_tag_2019_10_01()
        text1 = self.ts.get_news_text_from_first_tag(first_tag)
        text2 = ' Former Reserve Bank of India governor Raghuram Rajan has said that people in authority have to tolerate criticism and that any move to suppress it "is a sure fire recipe for policy mistakes'
        self.assertEqual(text1,text2)
    def get_first_tag_2019_10_01(self):
        return '<p class="p_txt_kj"><span style="font-weight:bold">Mumbai:</span> Former Reserve Bank of India governor Raghuram Rajan has said that people in authority have to tolerate criticism and that any move to suppress it "is a sure fire recipe for policy mistakes".</p>'
    """
