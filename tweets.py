from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

import time
import pandas as pd
import os

options = Options()
options.add_experimental_option("detach", True)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("window_size=1280,800")
options.add_argument("--disable-popup-blocking")
options.add_argument("--disable-save-password-bubble")



driver = webdriver.Chrome(options=options)
driver.get("https://accounts.google.com/v3/signin/identifier?hl=en_GB&ifkv=AXo7B7VGP4Y_gNfwPri72zV40Ii9kmgYbvLRXoOhOeBNkeBYcMPcPOX_Aolo1vK16FetaA4URMIfUA&flowName=GlifWebSignIn&flowEntry=ServiceLogin&dsh=S-1140670556%3A1692882589574310")
#email: 
email = 'YOUR_EMAIL'
#password:
password = 'YOUR_PASSWORD'

#LOGIN
driver.find_element(By.XPATH,'//*[@id="identifierId"]').send_keys(email)
time.sleep(3)
driver.find_element(By.XPATH,'//*[@id="identifierNext"]/div/button').click()

time.sleep(5)
driver.find_element(By.XPATH,'//*[@id="password"]/div[1]/div/div[1]/input').send_keys(password)
driver.find_element(By.XPATH,'//*[@id="passwordNext"]/div/button/span').click()
time.sleep(5)

#GO TO TWITTER
driver.get("https://twitter.com/")
time.sleep(4)
input("Please complete the manual step and then press Enter here...") # the manual step invloves closing the save passwrod popup, you could go incongnito mode instead by using options.add_argument("--incognito")
driver.get("https://twitter.com/explore")
time.sleep(5)
search = driver.find_element(By.XPATH,'//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[1]/div[1]/div/div/div/div/div/div[1]/div[2]/div/div/div/form/div[1]/div/div/div/label/div[2]/div/input')
search.send_keys('@Account') # a specific account to scrap tweets from
search.send_keys(Keys.ENTER)

# Wait for the account page to load
time.sleep(5)

# Function to simulate scrolling and scraping
def scroll_page(driver):
    tweets_data = []
    new_tweets=set()

    while len(tweets_data) < 100:  # Desired number of tweets
        tweet_elements = driver.find_elements(By.XPATH, '//article[@data-testid="tweet"]')

        for tweet_element in tweet_elements:
            try:
                tweet_text = tweet_element.text
                if tweet_text and tweet_text not in new_tweets:
                    tweets_data.append(tweet_text)
                    new_tweets.add(tweet_text)
            
            except StaleElementReferenceException:
                continue #recover from stale elements
    
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//article[@data-testid="tweet"]'))
        )


    return tweets_data


all_tweets_data = scroll_page(driver)

# Convert the list to a pandas DataFrame
df_tweets = pd.DataFrame(all_tweets_data,columns=['Tweets'])
#print(df_tweets)
