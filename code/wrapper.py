from code import telegraph_scraper

def main():
    print("Wrapper program started ...")
    ap = telegraph_scraper.ArchiveParameters()
    ap.year = "2019"
    ap.month = "09"
    ap.day = "20"
    ap.page_no=1
    ts = telegraph_scraper.TelegraphScraper()
    """
    a = ts.get_browser()
    a = ts.get_telegraph_archive_home_page(a)
    """
    maps = ts.get_maps_for_date_and_page_no(ap)
    map_collection = ts.get_map_collection(maps)
    ap = ts.get_variable_parameters_from_tag(map_collection[0], ap)
    file_name = ts.download_and_get_saved_web_page_path(ap)
    all_div_ids = ts.get_div_ids_from_downloaded_file(file_name)

    for div_id in all_div_ids:
        print("-------------------------------------------------------------")
        ts.get_news_text(div_id)
        """
        link = ts.get_link_from_parameters(ap)
        print(link)
        
        print("-------------------------------------------------------------")
        title = ts.get_title(ap)
        print(title)
        print("-------------------------------------------------------------")
        text = ts.get_news_text(ap)
        print(text)
        """
    print("Wrapper program completed.")
if __name__=="__main__":
  main()


