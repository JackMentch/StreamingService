import os
import csv
from scraper import *
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import math

# Dictionary of objects
platformsList = {}

data_directory = r'./Output'

for filename in os.listdir(data_directory):
    if filename.endswith(".csv"):

        with open(os.path.join(data_directory, filename), mode='r') as current_season:
            csv_reader = csv.reader(current_season)

            # Create an object if not found already
            for line in csv_reader:
                if line[0] not in platformsList.keys() and line[0] != "Platform":
                    platformsList[line[0]] = Platform(line[0])

                if line[0] in platformsList.keys():

                    if line[1] == "Movie":
                        platformsList[line[0]].movies[line[3]] = line[4]

                    elif line[1] == "TV":
                        platformsList[line[0]].tv[line[3]] = line[4]


# Plotting Number of Movies and Tv shows
barWidth = 0.2
tv_shows = []
movies = []
total = []
platforms = []

for platform in platformsList.values():
    print(f"Number of movies for {platform.name}: {len(platform.movies.keys())}")
    movies.append(len(platform.movies.keys()))
    platforms.append(platform.name)

print("-----------------------")

for platform in platformsList.values():
    print(f"Number of tv shows for {platform.name}: {len(platform.tv.keys())}")
    tv_shows.append(len(platform.tv.keys()))

total = [movie + tv_show for movie, tv_show in zip(movies, tv_shows)]

def plot_total():
    bar1 = np.arange(len(platforms))
    bar2 = [i+barWidth for i in bar1]
    bar3 = [i+barWidth for i in bar2]

    plt.bar(bar1,tv_shows,barWidth,label="TV Shows")
    plt.bar(bar2,movies,barWidth,label="Movies")
    plt.bar(bar3,total,barWidth,label="Total")

    plt.xlabel("Streaming Platforms")
    plt.ylabel("Amount of Shows/Movies")
    plt.title("Total Number of Movies/Shows on Platforms")
    plt.xticks(bar2,platforms)
    plt.legend()
    plt.show()

def plot_shows():
    bar1 = np.arange(len(platforms))

    plt.bar(bar1,tv_shows,barWidth,color=(0.8, 0.0, 0.0),label="TV Shows")

    plt.xlabel("Streaming Platforms")
    plt.ylabel("Number of TV Shows")
    plt.title("Total Number of TV Shows on Platforms")
    plt.xticks(bar1,platforms)
    plt.legend()
    plt.show()

def plot_movies():
    bar1 = np.arange(len(platforms))

    plt.bar(bar1,movies,barWidth,color=(0.0, 0.6, 0.0),label="Movies")

    plt.xlabel("Streaming Platforms")
    plt.ylabel("Number of Movies")
    plt.title("Total Number of Movies on Platforms")
    plt.xticks(bar1,platforms)
    plt.legend()
    plt.show()

def calc_show_average():

    list_of_scores = []
    sum_of_scores = 0
    shows_not_scored = 0

    for platform in platformsList.values():
        list_of_scores.extend(platform.tv.values())

    counter = 0
    for score in list_of_scores:

        if score != "N/A":
            sum_of_scores += int(score)
        else:
            shows_not_scored += 1

    return int(round(sum_of_scores/(len(list_of_scores)-shows_not_scored),0))

def calc_movie_average():

    list_of_scores = []
    sum_of_scores = 0
    movies_not_scored = 0

    for platform in platformsList.values():
        list_of_scores.extend(platform.movies.values())

    counter = 0
    for score in list_of_scores:

        if score != "N/A":
            sum_of_scores += int(score)
        else:
            movies_not_scored += 1

    return int(round(sum_of_scores/(len(list_of_scores)-movies_not_scored),0))

def calc_value_score():

    value_movie_scores = {}
    value_tv_scores = {}

    for platformObj in platformsList.values():

        platform_name = platformObj.name

        list_of_movie_scores = list(platformObj.movies.values())
        num_of_movies = len(list_of_movie_scores)

        list_of_tv_scores = list(platformObj.tv.values())
        num_of_tv_shows = len(list_of_tv_scores)

        movie_rating_coefficient = 0
        tv_rating_coefficient = 0

        for movie_score in list_of_movie_scores:

            if movie_score != "N/A":
                score = int(movie_score) - calc_movie_average()
                movie_rating_coefficient += score

        for tv_score in list_of_tv_scores:

            if tv_score != "N/A":
                score = int(tv_score) - calc_show_average()
                tv_rating_coefficient += score

        movie_value = math.log(num_of_movies,1.02)*(movie_rating_coefficient/num_of_movies)
        tv_show_value = math.log(num_of_tv_shows,1.02)*(tv_rating_coefficient/num_of_tv_shows)

        value_tv_scores[platform_name] = int(tv_show_value/100)
        value_movie_scores[platform_name] = int(movie_value/100)

        # print(platform_name)
        # print(movie_rating_coefficient)
        # print(tv_rating_coefficient)
        # print(f"Average Show Coeff: {tv_rating_coefficient/num_of_tv_shows}")
        # print(f"Average Movie Coeff: {movie_rating_coefficient/num_of_movies}")



    return value_movie_scores, value_tv_scores


plot_shows()