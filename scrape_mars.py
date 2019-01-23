# ## Step 2 - MongoDB and Flask Application

# Use MongoDB with Flask templating to create a new HTML page that displays all of the 
# information that was scraped from the URLs above.

# * Start by converting your Jupyter notebook into a Python script called `scrape_mars.py` 
# with a function called `scrape` that will execute all of your scraping code from above 
# and return one Python dictionary containing all of the scraped data.

# * Next, create a route called `/scrape` that will import your `scrape_mars.py` script 
# and call your `scrape` function.

#   * Store the return value in Mongo as a Python dictionary.

# * Create a root route `/` that will query your Mongo database and pass the mars data into an 
# HTML template to display the data.

# * Create a template HTML file called `index.html` that will take the mars data dictionary and
#  display all of the data in the appropriate HTML elements. Use the following as a guide for 
# what the final product should look like, but feel free to create your own design.


# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pymongo
import pandas as pd



# from datetime import datetime
# import time

# define scrape
def scrape():
    
    #--------------NASA MARS NEWS------------------------
    executable_path = {"executable_path": "chromedriver.exe"}
    browser = Browser("chrome", **executable_path, headless=False)

    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Scrape page into soup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")


    results = soup.find("li", class_='slide')
    # print(results)


    title = results.find("div", class_='content_title').a.text

    paragraph = results.find("div", class_="article_teaser_body").Text


    #--------------JPL MARS SPACE IMAGES------------------------
    # Visit the page
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    # Scrape page into soup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # featured_image_url
    featured_image_url = "https://www.jpl.nasa.gov"+soup.find("article")['style'].split("('", 1)[1].split("')")[0]
    
    #--------------NASA MARS WEATHER------------------------
    # Visit the url
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)

    # Scrape page into soup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # mars_weather
    mars_weather = soup.find("p",class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    # print(mars_weather)


    #--------------NASA MARS FACTS------------------------
    # Visit the url
    url = "http://space-facts.com/mars/"
    
    table = pd.read_html(url)[0]
    table.columns = ["Description", "Value"]
    table1 = table.set_index("Description")
    html_table = table1.to_html(na_rep = "",index=False)


    #--------------Mars Hemispheres------------------------
    # Visit the url
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    # Scrape page into soup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # hemisphere_image_url_1

    results = soup.find_all("div", class_='description')

    mars_data = []
    mars_dict = {}

    for result in results:

    # * You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.

        image_url_loc="https://astrogeology.usgs.gov"+result.find("a", href=True)["href"]
    #     print(image_url_loc)

        # Visit the url
        browser.visit(image_url_loc)

        # Scrape page into soup
        html = browser.html
        soup1 = BeautifulSoup(html, "html.parser")

        image_url ="https://astrogeology.usgs.gov" + soup1.find("img", class_='wide-image')['src']
    #     print(image_url)

        title=result.find("h3").text
    #     print(title)

        mars_dict = {
            "title": title,
            "img_url" : image_url
        }

        mars_data.append(mars_dict)

    mars_scrape_results={
        "newstitle":title,
        "newsparagraph":paragraph,
        "featuredimage":featured_image_url,
        "marsfacts":html_table,
        "marsweather":mars_weather,
        "marsdata":mars_data,
    }
    
    return mars_scrape_results
