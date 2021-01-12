from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

class Platform():
    def __init__(self, name):
        self.tv = {}
        self.movies = {}
        self.name = name

def data_scraping(platform, source, platform_class):

    page_exists = True
    offset = 0
    ratings = []
    names = []

    while page_exists:

        base_link = "https://reelgood.com/" + source + "/source/" + platform + "?offset=" + str(offset)

        page_request = Request(base_link, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            page_open = urlopen(page_request)
        except:
            break

        # Check if we see the Error 404 page
        error = BeautifulSoup(page_open.read(), features="html.parser")
        error_message = error.find_all("h1", { "class":"css-7fo8ar e1oyx0om3"})
        print(base_link, len(error_message))

        if len(error_message) != 0:
            break

        else:
            platform_req = Request(base_link, headers={'User-Agent': 'Mozilla/5.0'})
            platform_html = urlopen(platform_req)
            platformObj = BeautifulSoup(platform_html.read(), features="html.parser")


            unfiltered_names = platformObj.find_all("td", { "class":"css-1u7zfla e126mwsw1"})

            unfiltered_ratings = platformObj.findAll("b", {"class":"css-1px39yc"})


            for rating in unfiltered_ratings:
                if "/10" not in rating.get_text():
                    ratings.append(rating.get_text())

            for name in unfiltered_names:
                names.append(name.get_text())

            offset += 50

    ratings = [v for i, v in enumerate(ratings) if i % 2 == 1]

    iterations = len(names)

    for i in range(0,iterations):
        if source == "movies":
            platform_class.movies[names[i]] = ratings[i]
        elif source == "tv":
            platform_class.tv [names[i]] = ratings[i]

    if source == "movies":
        print(list(platform_class.movies.keys()))
        print(list(platform_class.movies.values()))
    elif source == "tv":
        print(list(platform_class.tv.keys()))
        print(list(platform_class.tv.values()))

    return platform_class

