from code import times_scraper

def main():
    print("Wrapper program started ...")
    ts = times_scraper.TimesScraper()
    a = ts.get_browser()
    a = ts.get_times_archive_home_page(a)
    print("Wrapper program completed.")
if __name__=="__main__":
  main()


