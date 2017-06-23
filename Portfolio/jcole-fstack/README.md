# Multi-User Blog Project

This project is a working blog application written in Python and hosted on Google
App Engine.

To view a working example, click [here.][3b7474d4]


To Setup and run locally.


Install [Python 2.7 ][f7403f8d]and [Google Appengine SDK][d7b372f6]


1. Clone Repository.
2. From the Command line in the local folder enter the command:
    ```
  dev_appserver.py app.yaml

    ```
3. Open browser to localhost:8080.

## Files

**app.yaml** - Configures how URL paths correspond to handlers/static files for Google App Engine.
**blog.py** - This file contains all of the Python code to create the data models and perform the functions to create the blog.

## Folders

**static** - Contains the Javascript, Images, CSS, and Font folders. This blog uses standard Bootstrap CSS, Javascript, JQuery librarires. In addition, the blog uses  **main.css** to add custom styling. This blog also uses the Freely distributed Glyphicon image files. These are found in the **font** folder.

**templates** - This blog uses [Jinja 2 ][ab1da425]and all HTML files are stored in the **templates** folder. 






[3b7474d4]: https://jcole-fstack.appspot.com/blog "Full-Stack Blog"
[d7b372f6]: https://cloud.google.com/appengine/docs/standard/python/download "Google App Engine"
[f7403f8d]: https://www.python.org/downloads/ "Python"
[ab1da425]: http://jinja.pocoo.org/ "Jinja 2"
