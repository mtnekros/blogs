# Scraping all vetshops within a country from Google Maps

Recently, I was trying to scrape some basic informations about all agrovets
in Nepal. In this article, we are going to go over how I did it.

Our requirements.
1. Download following informations of all agrovets in Nepal with google maps.
    * Name
    * Shop type
    * Coordinates(latitude, longitude)
    * Location address
    * Shop's phone number

Let's get over the steps to setup the programming environment.
1. Install [python](https://www.python.org/downloads/)
2. Install the selenium package with `pip install selenium`
3. Download the [chromedriver](https://sites.google.com/a/chromium.org/chromedriver/downloads).

# The hurdles
1. Including the whole country for the search.
    -> Searching different locations

