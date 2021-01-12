import os
import csv

prices = {"disney_plus": "7", "hulu": "6", "showtime": "11", "netflix": "9",
          "peacock": "5", "amazon": "9", "hbo_max": "15"}

def datatocsv(platformsList):

    with open('Output/Output.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow(["Platform", "Source", "Cost", "Name", "Rating"])

        for platform in platformsList:

            name = platform.name

            # {"Breaking Bad": "97", ....}
            movies = platform.movies
            tv = platform.tv

            for key, value in movies.items():
                writer.writerow([name, "Movie", prices[platform.name], key, value])

            for key, value in tv.items():
                writer.writerow([name, "TV", prices[platform.name], key, value])
