from code import telegraph_scraper

def main():
    print("Wrapper program started ...")
    ap = telegraph_scraper.ArchiveParameters()
    ap.year = "2019"
    ap.month = "10"
    ap.day = "01"
    ap.page_no=1
    ts = telegraph_scraper.TelegraphScraper()
    """
    a = ts.get_browser()
    a = ts.get_telegraph_archive_home_page(a)
    """
    maps = ts.get_maps_for_date_and_page_no(ap)
    map_collection = ts.get_map_collection(maps)
    for tag in map_collection:
        ap = ts.get_variable_parameters_from_tag(tag,ap)
        link = ts.get_link_from_parameters(ap)
        print(link)
        """
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


