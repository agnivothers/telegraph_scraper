from code import telegraph_scraper
from datetime import date
from datetime import timedelta
import os
import logging
"""
    ap.year = "2019"
    ap.month = "08"
    ap.day = "21"
    ap.page_no=8
"""

def download_and_save_data_for_particular_date(ts, ap, fsp, download_date):
    ap = ts.populate_archive_parameters_from_download_date(ap,download_date)
    total_number_of_pages = ts.get_total_number_of_pages(ap)
    for page_no in range(1,total_number_of_pages):
    #for page_no in range(4,6):
        ap.page_no = page_no
        download_and_save_data_for_particular_date_and_page_number(ts, ap, fsp)

def download_and_save_data_for_particular_date_and_page_number(ts, ap, fsp):
    logging.debug('day: '+ap.day)
    logging.debug('month: '+ap.month)
    logging.debug('year: '+ ap.year)
    logging.debug('page number: ' + str(ap.page_no))
    maps = ts.get_maps_for_date_and_page_no(ap)
    map_collection = ts.get_map_collection(maps)
    if map_collection is None:
        logging.debug("NO NEWS ON " + ap.day + "-" + ap.month + "-" + ap.year + " FOR PAGE NO: " + str(ap.page_no))
        return

    #ap = ts.get_variable_parameters_from_tag(map_collection[0], ap, function_name_to_replace)
    ap = ts.get_variable_parameters_from_tag(map_collection[0], ap)
    #logging.debug('pophead_variable1: '+ap.pophead_variable1)
    #logging.debug('pophead_variable2: '+ap.pophead_variable2)
    #logging.debug('pophead_variable3: '+ ap.pophead_variable1)
    file_name = ts.download_and_get_saved_web_page_path(ap, fsp)
    print(file_name)
    """
    all_div_ids = ts.get_div_ids_from_downloaded_file(file_name)

    for div_id in all_div_ids:
        print("-------------------------------------------------------------")
        title = ts.get_news_title(div_id)
        print(title)
        print("-------------------------------------------------------------")
        text = ts.get_news_text(div_id)
        print(text)
        ts.save_extracted_data(title, text, ap, fsp)
    """
def main():

    print("Wrapper program started ...")
    """
    if os.path.isfile('telegraph_scraper.log'):
      os.remove('telegraph_scraper.log')
    else:    ## Show an error ##
      print("Error: %s file not found - " % 'telegraph_scraper.log')
    """
    ts = telegraph_scraper.TelegraphScraper()

    fsp = telegraph_scraper.FileStorageParameters()
    fsp.DOWNLOADED_DATA_ROOT_DIRECTORY = 'data/downloaded_data/'
    fsp.EXTRACTED_DATA_ROOT_DIRECTORY = 'data/extracted_data/'

    ap = telegraph_scraper.ArchiveParameters()


    start_date = date(2018,6,3)
    download_date = start_date
    end_date = date(2018,6,8)

    while(download_date!=end_date):
        """
        try:
            download_and_save_data_for_particular_date(ts, ap, fsp, download_date)
        except IndexError as er:
            logging.debug(er)
            logging.debug(er.args)
        """

        download_and_save_data_for_particular_date(ts, ap, fsp, download_date)

        download_date = download_date+timedelta(days=1)

    download_and_save_data_for_particular_date(ts, ap, fsp, download_date)
    print("Data for all dates downloaded.")

    print("Wrapper program completed.")

if __name__=="__main__":
  main()


