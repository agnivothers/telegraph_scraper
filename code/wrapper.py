from code import telegraph_scraper
from datetime import date
from datetime import timedelta
import os
import logging


def main():
    wrapper()
    #download_data_from_exception()

def download_and_save_data_for_particular_date(ts, ap, fsp, download_date):
    ap = ts.populate_archive_parameters_from_download_date(ap,download_date)
    total_number_of_pages = ts.get_total_number_of_pages(ap)
    #for page_no in range(2,3):
    for page_no in range(1,total_number_of_pages+1):
        ap.page_no = page_no
        download_and_save_data_for_particular_date_and_page_number(ts, ap, fsp)

def download_and_save_data_for_particular_date_and_page_number(ts, ap, fsp):
    logging.debug('day: '+ap.day)
    logging.debug('month: '+ap.month)
    logging.debug('year: '+ ap.year)
    logging.debug('page number: ' + str(ap.page_no))
    maps = ts.get_maps_for_date_and_page_no(ap)
    if maps is None:
        logging.debug("NO MAPS AND HENCE NO NEWS ON " + ap.day + "-" + ap.month + "-" + ap.year + " FOR PAGE NO: " + str(ap.page_no))
        return
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

def extract_and_save_data_for_particular_date(ts, ap, fsp, download_date):
    ap = ts.populate_archive_parameters_from_download_date(ap, download_date)
    folder_name = ts.get_folder_name_to_store_downloaded_data(ap, fsp)
    print(folder_name)
    files = os.listdir(folder_name)
    for file in files:
        file_name = folder_name+file
        logging.debug("FILE NAME FOR EXTRACTING NEWS: "+file_name)
        all_div_ids = ts.get_div_ids_from_downloaded_file(file_name)
        if all_div_ids is None:
            continue
        for div_id in all_div_ids:
            print("-------------------------------------------------------------")
            try:
                title = ts.get_news_title(div_id)
                print(title)
                print("-------------------------------------------------------------")
                text = ts.get_news_text(div_id)
                #print(text)
                ts.save_extracted_data(title, text, ap, fsp, file)
            except IndexError as ie:
                #logging.exception(ie)
                logging.debug("FILE NAME WHERE INDEXERROR OCCURRED: "+file_name)
                logging.debug("TITLE: "+title)
                logging.debug("NO BODY TEXT FOR NEWS: ")
                #logging.debug("TEXT: " +text)
            except Exception as ex:
                logging.debug("SPECIFIC ERROR NOT CAUGHT. HENCE LOGGING GENERIC ERROR.")
                logging.exception(ex)


def download_data(ts, ap, fsp, download_date, end_date):
    while (download_date != end_date):
        download_and_save_data_for_particular_date(ts, ap, fsp, download_date)
        download_date = download_date + timedelta(days=1)
    download_and_save_data_for_particular_date(ts, ap, fsp, download_date)

def extract_data(ts, ap, fsp, download_date, end_date):
    while (download_date != end_date):
        extract_and_save_data_for_particular_date(ts, ap, fsp, download_date)
        download_date = download_date + timedelta(days=1)
    extract_and_save_data_for_particular_date(ts, ap, fsp, download_date)

def wrapper():
    print("Wrapper program started ...")
    ts = telegraph_scraper.TelegraphScraper()
    fsp = telegraph_scraper.FileStorageParameters()
    fsp.DOWNLOADED_DATA_ROOT_DIRECTORY = 'data/downloaded_data/'
    fsp.EXTRACTED_DATA_ROOT_DIRECTORY = 'data/extracted_data/'

    ap = telegraph_scraper.ArchiveParameters()

    start_date = date(2020,4,8)
    print("START DATE: "+str(start_date))
    download_date = start_date
    end_date = date(2020,4,8)
    print("END DATE: " + str(end_date))


    # Loop to download data from the Internet
    print("Running download_data ...")
    download_data(ts, ap, fsp, download_date, end_date)
    print("Data for all dates downloaded.")
    # Loop to parse the data locally
    print("Running extract_data ...")
    #extract_data(ts, ap, fsp, download_date, end_date)
    print("Data for all dates extracted.")
    print("Wrapper program completed.")

def download_data_from_exception():
    print("download_data_from_exception program started ...")
    ts = telegraph_scraper.TelegraphScraper()
    ts.download_data_that_raised_exception_in_first_pass()
    print("download_data_from_exception program completed.")
if __name__=="__main__":
  main()


