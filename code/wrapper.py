from code import telegraph_scraper
from datetime import date
from datetime import timedelta

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
        ap.page_no = page_no
        download_and_save_data_for_particular_date_and_page_number(ts, ap, fsp)

def download_and_save_data_for_particular_date_and_page_number(ts, ap, fsp):
    maps = ts.get_maps_for_date_and_page_no(ap)
    map_collection = ts.get_map_collection(maps)
    ap = ts.get_variable_parameters_from_tag(map_collection[0], ap)
    file_name = ts.download_and_get_saved_web_page_path(ap, fsp)
    all_div_ids = ts.get_div_ids_from_downloaded_file(file_name)

    for div_id in all_div_ids:
        print("-------------------------------------------------------------")
        title = ts.get_news_title(div_id)
        print(title)
        print("-------------------------------------------------------------")
        text = ts.get_news_text(div_id)
        print(text)
        ts.save_extracted_data(title, text, ap, fsp)

def main():
    print("Wrapper program started ...")
    ts = telegraph_scraper.TelegraphScraper()

    fsp = telegraph_scraper.FileStorageParameters()
    fsp.DOWNLOADED_DATA_ROOT_DIRECTORY = 'data/downloaded_data/'
    fsp.EXTRACTED_DATA_ROOT_DIRECTORY = 'data/extracted_data/'

    ap = telegraph_scraper.ArchiveParameters()


    start_date = date(2018,6,1)
    download_date = start_date
    end_date = date(2018,6,2)

    while(download_date!=end_date):
        download_and_save_data_for_particular_date(ts, ap, fsp, download_date)
        download_date = download_date+timedelta(days=1)

    download_and_save_data_for_particular_date(ts, ap, fsp, download_date)
    print("Data for all dates downloaded.")

    print("Wrapper program completed.")

if __name__=="__main__":
  main()


