from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
import time
from pymongo import MongoClient
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

def linkedinscrap(driver,collection,keyword):

    url = "https://www.linkedin.com/home"
    username = "9700306613"
    password = "Jjpbaje@123"
    driver.get(url)
    time.sleep(6)
    uname = driver.find_element("name", "session_key")
    uname.send_keys(username)
    time.sleep(5)
    pwd = driver.find_element("name", "session_password")
    pwd.send_keys(password)
    time.sleep(5)
    pwd.send_keys(Keys.RETURN)
    time.sleep(5)
    articles_list = []

    # Define the base URL for the LinkedIn search
    page_url = f"https://www.linkedin.com/search/results/content/?keywords={keyword}"
    driver.get(page_url)


    # for page_number in range(1, 4):  # Assuming you want to scrape 2 pages
    #     page_url = base_url + str(page_number)
    #     print(page_url)
    #     driver.get(page_url)
    #     time.sleep(3)
    #     html_content = driver.page_source
    #     soup = BeautifulSoup(html_content, 'html.parser')
    #     new_articles = soup.find_all('div', {'data-chameleon-result-urn': True})
    #     articles_list.extend(new_articles)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)  # Adjust the sleep time according to the time it takes to load more posts

    for _ in range(3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # Adj

    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    new_articles = soup.find_all('div', {'data-urn': True})
    articles_list.extend(new_articles)


    print(len(articles_list))

    for article in articles_list[:20]:

        text_element = article.find('div', {'class': lambda x: x and 'feed-shared-update-v2__description-wrapper mr2' in x})
        text = text_element.text.strip() if text_element else None

        posted_by=article.find('span',{'class':lambda x: x and 'update-components-actor__name' in x})
        posted=posted_by.text.strip() if posted_by else None

        liked_by=article.find('span',{'class':lambda x: x and 'social-details-social-counts__reactions-count' in x})
        likes=liked_by.text.strip() if liked_by else 0
        if likes != '':
            likes = str(likes)
            remove_text = re.sub(r'K', r'', str(likes))
            if 'K' in likes:
                likes = str(int(float(remove_text) * 1000))
        else:
            likes=0

        Images=article.find('img',{'alt':''})
        img_src= Images['src'] if Images else None

        retweets=article.find('button',{'aria-label':lambda x: x and 'repost' in x})
        retweet=retweets['aria-label'].split(" ") if retweets else 0
        if retweet != 0:
            retweet = str(retweet[0])
            remove_text = re.sub(r'K', r'', str(retweet))
            if 'K' in retweet:
                retweet = str(int(float(remove_text) * 1000))

        url_element=article['data-urn']
        print(url_element)
        url="https://www.linkedin.com/feed/update/"+url_element


        print("likes: ",likes)
        if posted:
            posted = posted.split("View")
            print("Posted by:", posted[0].strip())
        if text:
            print("Text:", text)
        print("Image : ", img_src)
        if retweet:
            print('shares: ',retweet)
        else:
            print('shares: ', 0)
        print("-" * 50)


        data = {
            "posted_by": posted[0].strip() if posted else None,
            "text_content":text,
            "media_content":img_src,
            "likes":int(likes),
            "Shares": int(retweet) ,
            "url":url,
            "Source":"Linkedin"
        }

        # Insert the data into MongoDB
        collection.insert_one(data)
