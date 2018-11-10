from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import pymongo

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    #executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)



def scrape():
    browser = init_browser()
    listings = {}

    # NASA MARS News
    
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    news_title = soup.find('div',class_='content_title').get_text()
    news_p = soup.find('div',class_="article_teaser_body").get_text()
    listings['title'] = news_title
    listings['news'] = news_p

    # JPL Mars Space Images - Featured Image

    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)
    html2 = browser.html
    soup2 = BeautifulSoup(html2, 'html.parser')
    article_style = soup2.find('article')['style']
    start = article_style.find("('")
    end = article_style.find("')")
    image = article_style[start+len("('"):end]
    featured_image_url = "https://www.jpl.nasa.gov" + image
    listings['featured_image'] = featured_image_url

    # Mars Weather

    url3 = 'https://twitter.com/marswxreport'
    browser.visit(url3)
    html3 = browser.html
    soup3 = BeautifulSoup(html3, 'html.parser')
    mars_weather = soup3.find('p',class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").get_text()
    listings['mars_weather'] = mars_weather

    # Mars Facts

    url4 = 'https://space-facts.com/mars/'
    browser.visit(url4)
    tables = pd.read_html(url4)
    df = tables[0]
    df.columns=['description','value']
    df = df.set_index('description')
    mars_facts_table = df.to_html()
    listings['mars_facts_table'] = mars_facts_table

    # Mars Hemispheres

    url_pics = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_pics)
    marspics_html = browser.html
    soup_marspics = BeautifulSoup(marspics_html, 'html.parser')
    hmsp_img_lnk = []
    images = {}

    products = soup_marspics.find("div", class_ = "result-list" )
    links = products.find_all("div", class_="item")

    for link in links:
        endlink = link.find("a")['href']
        mlinks = 'https://astrogeology.usgs.gov/' + endlink
        browser.visit(mlinks)
        html_m = browser.html
        soup_m = BeautifulSoup(html_m, "html.parser")
        download_link = soup_m.find("div", class_="downloads").ul.li.a['href']
        images['title'] = soup_m.find("h2", class_='title').text
        images['title'] =  images['title'].replace('Enhanced','')
        images['img_url'] = download_link
        hmsp_img_lnk.append(images)
        images = {}

    listings['mars_hemispheres'] = hmsp_img_lnk

    return listings