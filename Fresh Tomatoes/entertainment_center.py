# Lesson 3.4: Make Classes
# Mini-Project: Movies Website

# In this file, you will define instances of the class Movie defined
# in media.py. After you follow along with Kunal, make some instances
# of your own!

# After you run this code, open the file fresh_tomatoes.html to
# see your webpage!

import media
import fresh_tomatoes

# Favorite Movies
last_mohicans = media.Movie("Last of the Mohicans",
"Three trappers protect a British Colonel's daughters in the midst of the French and Indian War.",
"https://images-na.ssl-images-amazon.com/images/M/MV5BMzU4YzI3ODItYzY3NS00ZTQ2LTg2YzUtNTdjMTVlYjVkYTE4XkEyXkFqcGdeQXVyNjUwNzk3NDc@._V1_.jpg",
"https://www.youtube.com/watch?v=yaQeVnN6pUc")

the_revenant = media.Movie("The Revenant",
"A frontiersman on a fur trading expedition in the 1820s fights for survival after being mauled by a bear and left for dead by members of his own hunting team.",
"https://images-na.ssl-images-amazon.com/images/M/MV5BY2FmODc2N2QtYmY3MS00YTMwLWI2NGYtZWRmYWVkNjFjZmI0XkEyXkFqcGdeQXVyNTMxMjgxMzA@._V1_.jpg",
"https://www.youtube.com/watch?v=LoebZZ8K5N0")

unforgiven = media.Movie("Unforgiven",
"Retired Old West gunslinger William Munny reluctantly takes on one last job, with the help of his old partner and a young man.",
"https://images-na.ssl-images-amazon.com/images/M/MV5BODM3YWY4NmQtN2Y3Ni00OTg0LWFhZGQtZWE3ZWY4MTJlOWU4XkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_SY1000_CR0,0,665,1000_AL_.jpg",
"https://www.youtube.com/watch?v=ftTX4FoBWlE")

black_robe = media.Movie("Black Robe",
"A young Jesuit priest seeks to convert the Indian tribes in Canada while also trying to survive the harsh winter.",
"https://images-na.ssl-images-amazon.com/images/M/MV5BODA5NDQ4NzQ0NF5BMl5BanBnXkFtZTYwMjU3MDM5._V1_.jpg",
"https://www.youtube.com/watch?v=hVfMsZMiSzY")

dances_wolves = media.Movie("Dances with Wolves",
"Lt. John Dunbar, exiled to a remote western Civil War outpost, befriends wolves and Indians, making him an intolerable aberration in the military.",
"https://images-na.ssl-images-amazon.com/images/M/MV5BMTY3OTI5NDczN15BMl5BanBnXkFtZTcwNDA0NDY3Mw@@._V1_SY1000_CR0,0,666,1000_AL_.jpg",
"https://www.youtube.com/watch?v=uc8NMbrW7mI")

into_west = media.Movie("Into the West",
"Tales from the American West in the 19th century, told from the perspective of two families, one of white settlers and one of Native Americans.",
"https://images-na.ssl-images-amazon.com/images/M/MV5BMTI1NTg4NTE2M15BMl5BanBnXkFtZTcwMzUwNjAzMQ@@._V1_SY1000_CR0,0,747,1000_AL_.jpg",
"https://www.youtube.com/watch?v=luNNjjsTPqg")

movies = [last_mohicans,the_revenant,unforgiven,black_robe,dances_wolves,into_west]

fresh_tomatoes.open_movies_page(movies)
