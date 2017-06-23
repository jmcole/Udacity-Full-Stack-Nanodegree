# Lesson 3.4: Make Classes
# Mini-Project: Movies Website

# In this file, you will define the class Movie. You could do this
# directly in entertainment_center.py but many developers keep their
# class definitions separate from the rest of their code. This also
# gives you practice importing Python files.

import webbrowser

class Movie():
    # This class provides a way to store movie related information

    def __init__(self,movie_title,movie_storyline,poster_image,trailer_youtube):
        # initialize instance of class Movie
        # Based on https://classroom.udacity.com/nanodegrees/nd000/parts/7697496f-b17f-4ddd-81e1-afc2b001c80c/modules/a15df0cc-d40e-4ac9-92f8-fad5182b78e6/lessons/4e9680db-757d-4dfa-a1ca-46222ef78ac6/concepts/10136290610923#
        self.title = movie_title
        self.storyline = movie_storyline
        self.poster_image_url = poster_image
        self.trailer_youtube_url= trailer_youtube

    def show_trailer(self):
        webbrowser.open(self.trailer_youtube_url)
