from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import json
import time
import re
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

def fbscrap(driver,collection,keyword):
    url = "https://www.facebook.com"
    username = "6301360621"
    password = "Jjpbaje@123"
    driver.get(url)
    time.sleep(2)
    email = driver.find_element("name", "email")
    pswrd = driver.find_element("name", "pass")
    email.send_keys(username)
    time.sleep(1)
    pswrd.send_keys(password)
    time.sleep(3)
    email.submit()
    driver.maximize_window()
    time.sleep(2)
    driver.get(f"https://www.facebook.com/search/posts/?q={keyword}&filters=eyJycF9hdXRob3I6MjAsInJwX2F1dG9fYXV0aG9yOiwyMCwid2ViX2F1dG9fYXV0aG9yOiwyMCwiZW1haWwiOiJ0ZWxlbmdhbmFAZ21haWwuY29tIn0%3D")
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)  # Adjust the sleep time according to the time it takes to load more posts

    for _ in range(6):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(6)  # Adjust the sleep time according to the time it takes to load more posts

    # Get the HTML content of the current page
    html_content = driver.page_source

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract information using BeautifulSoup
    article_elements = soup.find_all('div', {'role': 'article'})
    article_elements = [article for article in article_elements if 'reel' not in article.find('a', href=True)['href'].lower()]

    print(len(article_elements))
    for article in article_elements[:20]:
        text_element = article.find('div', {'data-ad-comet-preview': 'message'}) or \
                       article.find('div', {'data-ad-preview': 'message'}) or \
                       article.find('div', {'style': 'text-align: start;'})


        text = text_element.text if text_element else None

        strong_element = article.find('span', attrs=lambda x: x is None)
        posted_by = strong_element.get_text() if strong_element else 'Group'

        span_element = article.find('span', {'class': 'xt0b8zv x1e558r4'})
        reaction_text = span_element.get_text() if span_element else 0

        if reaction_text != 0:
            reaction_text = str(reaction_text)
            remove_text = re.sub(r'K', r'', str(reaction_text))
            if 'K' in reaction_text:
                reaction_text = str(int(float(remove_text) * 1000))
        # reaction_count_match = re.search(r'(\d+(\.\d+)?[kKmMbB]|\d+)', reaction_text)
        # reaction_count = reaction_count_match.text if reaction_count_match else None
        span_element = article.find_all('div', {'class': 'x9f619 x1n2onr6 x1ja2u2z x78zum5 xdt5ytf x2lah0s x193iq5w xeuugli xsyo7zv x16hj40l x10b6aqq x1yrsyyn'})
        # Extract the number of shares using a regular expression
        share_count=0
        for spaned_element in span_element:
            if spaned_element.text:
                print(spaned_element.text)
                parts = spaned_element.text.split(' ')
                share_count = parts[0]         # Stop searching once a matching element is found
                break;

        if share_count != 0:
            share_count = str(share_count)
            remove_text = re.sub(r'K', r'', str(share_count))
            if 'K' in share_count:
                share_count = str(int(float(remove_text) * 1000))

        image_element = article.find('img', {'referrerpolicy': 'origin-when-cross-origin', 'src': lambda x: x and 'emoji' not in x})
        src = image_element['src'] if image_element else None

        url_element=article.find('a',{'href':lambda x: x and 'posts' not in x})
        url=url_element['href'] if url_element else None

        print("Posted by:", posted_by)
        print("Text:", text)
        print("Image Source:", src)
        print("Reaction Count:", reaction_text)
        print("Shared count:",share_count)
        print("-" * 50)

        data = {
            "posted_by": posted_by,
            "text_content": text,
            "media_content": src,
            "likes": int(reaction_text),
            "Shares": int(share_count),
            "url":url,
            "Source": "Facebook"
        }

        # Insert the data into MongoDB
        collection.insert_one(data)

