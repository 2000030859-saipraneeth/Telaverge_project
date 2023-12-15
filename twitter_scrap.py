from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
from pymongo import MongoClient
import re
#
# client = MongoClient('mongodb://localhost:27017/')
# db = client['Socio_sage']
# collection = db['Posts']
#
# options = Options()
# options.add_experimental_option("detach", True)
# options.add_argument("--disable-infobars")
# options.add_argument("start-maximized")
# options.add_argument("--disable-extensions")
#
# options.add_experimental_option(
#     "prefs", {"profile.default_content_setting_values.notifications": 1}
# )
#
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


def twitterscrap(driver,collection,keyword):
    url = "https://twitter.com/i/flow/login"
    username = "jjpbaje01"
    password = "Jjpbaje@123"
    driver.get(url)
    time.sleep(6)
    uname = driver.find_element("name", "text")
    uname.send_keys(username)
    uname.send_keys(Keys.RETURN)
    time.sleep(2)
    pwd = driver.find_element("name", "password")
    pwd.send_keys(password)
    pwd.send_keys(Keys.RETURN)
    time.sleep(5)
    driver.get(f"https://twitter.com/search?q={keyword}")
    time.sleep(5)

    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(3)  # Add a delay to wait for the content to load

    # Set to store unique articles
    unique_articles = set()

    # Scroll down until you have 20 unique articles
    while len(unique_articles) < 20:
        # Capture current number of unique articles
        current_unique_count = len(unique_articles)

        # Scroll down
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(6)

        # Parse the new content
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find articles on the page
        new_articles = soup.find_all('article')

        # Add new articles to the set
        unique_articles.update(new_articles)

        # Remove duplicates within the set
        unique_articles = {article for article in unique_articles if article}

        # Check if new articles were added in the last scroll
        if len(unique_articles) == current_unique_count:
            break

    # Print information for the 20 unique articles
    for article in list(unique_articles)[:20]:
        text_element = article.find('div', {'data-testid': 'tweetText'})
        text = text_element.get_text() if text_element else None

        image_element = article.find('img', {'alt': 'Image'})
        src = image_element['src'] if image_element else None

        video_element = article.find('video')
        vid_src = video_element['src'] if video_element else None

        posted_by=article.find('span',{'class':'css-1qaijid r-bcqeeo r-qvutc0 r-poiln3'})
        posted=posted_by.get_text() if posted_by else None

        liked_by = article.find('div', {'data-testid':'like'})
        likes = liked_by.text.strip() if liked_by else 0
        if likes != '':
            likes = str(likes)
            remove_text = re.sub(r'K', r'', str(likes))
            if 'K' in likes:
                likes = str(int(float(remove_text) * 1000))
        else:
            likes = 0

        shared_by = article.find('div', {'data-testid':'retweet'})
        shares = shared_by.get_text() if shared_by else None
        if 'K' in shares:
            shares = str(int(float(remove_text) * 1000))
        if shares != '':
            shares = str(shares)
            remove_text = re.sub(r'K', r'', str(shares))
            if 'K' in likes:
                likes = str(int(float(remove_text) * 1000))
        else:
           shares=0

        media_content = src if src and not vid_src else vid_src

        url_element = article.find('a', {'href': lambda x: x and 'status' in x})
        url = "https://twitter.com" + url_element['href']

        print('Posted by:',posted)
        print('Text: ', text)
        print('media_content: ', media_content)
        print('shares:',shares)
        print("-" * 50)

        data = {
            "posted_by": posted,
            "text_content":text,
            "media_content":media_content,
            "likes":int(likes),
            "Shares": int(shares),
            "url":url,
            "Source":"Twitter"
        }

        # Insert the data into MongoDB
        collection.insert_one(data)
