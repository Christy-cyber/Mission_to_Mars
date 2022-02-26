#!/usr/bin/env python
# coding: utf-8

# Import Splinter and BeautifulSoup and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt
import time

def scrape_all():
    # Initiate headless driver for deployment--set-up splinter/executable path
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    
    # Set news_title and paragraph variables; tells Python to use mars_news function to pull data
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": mars_hemispheres(browser)
}

    # End session--stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


# ### Featured Images from JPL

def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Include try/except to handle errors
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

# ## Mars Facts Website

def mars_facts():

    # Include try/except block to handle errors
    try:
        # use 'read_html" to scrape the facts table into a dataframe
        # Harvest table from website using pandas, set column titles, set index
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None
    
    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert df back to HTML ready code, include bootstrap
    return df.to_html(classes = "table table-striped")


# ## Mars Hemispheres Website

def mars_hemispheres(browser):
    
    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # Find and click thumbnail to navigate to next page
    thumb_image_elem = browser.find_by_css('a.product-item img')


    # Create for loop to loop through images
    for image in range(len(thumb_image_elem)):
    
        # Navigate to the image
        browser.find_by_css('a.product-item img')[image].click()
    
        # Parse the resulting html with soup
        html = browser.html
        img_soup = soup(html, 'html.parser')

    
        # Add try/except for error handling
        try:

            # Get url and title
            img_url_rel= browser.find_by_text('Sample')
            title = browser.find_by_css('h2.title').text
        
        except BaseException:
            return None

        # Complete full url
        img_url = img_url_rel['href']
    
        # Create dictionary
        hemispheres = {} 

        # Add url and title to dictionary
        hemispheres['img_url'] = img_url
        hemispheres['title'] = title

        # Append url and title dictionary to list
        hemisphere_image_urls.append(hemispheres)
    
        # Return to browser and include wait time to allow browser to load
        browser.back()
        time.sleep(1)



    # 4. Print the list that holds the dictionary of each image url and title.
    return hemisphere_image_urls

    # 5. Quit the browser
    #browser.quit()


if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())







