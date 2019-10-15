from code import telegraph_scraper

def main():
    print("Wrapper program started ...")
    ap = telegraph_scraper.ArchiveParameters()
    ap.year = "2019"
    ap.month = "10"
    ap.day = "01"
    ap.page_no=4
    fsp = telegraph_scraper.FileStorageParameters()
    fsp.DOWNLOADED_DATA_ROOT_DIRECTORY = 'data/downloaded_data/'
    fsp.EXTRACTED_DATA_ROOT_DIRECTORY = 'data/extracted_data/'
    ts = telegraph_scraper.TelegraphScraper()
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
        ts.save_extracted_data(title,text,ap,fsp)

    print("Wrapper program completed.")
if __name__=="__main__":
  main()


