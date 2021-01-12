from scraper import *
from datatocsv import *

# We will store all of the Platform objects into a list
platformsList = []

def main():

    platforms = ["peacock", "disney_plus", "showtime", "netflix", "hulu", "amazon", "hbo_max"]

    for platform in platforms:

        platform_class = Platform(platform)

        data_scraping(platform, "tv", platform_class)
        data_scraping(platform, "movies", platform_class)

        platformsList.append(platform_class)

    datatocsv(platformsList)

    return 0


if __name__ == '__main__':
    main()


