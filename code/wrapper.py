from code import telegraph_scraper

def main():
    print("Wrapper program started ...")
    ts = telegraph_scraper.TelegraphScraper()
    a = ts.get_browser()
    a = ts.get_telegraph_archive_home_page(a)
    print("Wrapper program completed.")
if __name__=="__main__":
  main()


