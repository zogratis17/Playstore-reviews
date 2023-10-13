from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')

def analyze_sentiment(text):
    sia = SentimentIntensityAnalyzer()
    sentiment_scores = sia.polarity_scores(text)
    compound_score = sentiment_scores['compound']

    if compound_score >= 0.05:
        return 'Positive'
    elif compound_score <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'

# Set up the appropriate web driver based on user input
driver = None
user_choice = input("Are you an iOS or Android user? ")
if user_choice.lower() == "ios":
    app_name = input("Enter the name of the app or game (Please give the correct name for better results): ")
    # Use appropriate web driver for iOS (e.g., Safari)
elif user_choice.lower() == "android":
    app_name = input("Enter the name of the app or game (Please give the correct name for better results): ")
    # Use appropriate web driver for Android (e.g., Chrome)
else:
    print("Invalid choice. Please select either 'iOS' or 'Android'.")
    exit()

# Prompt the user to enter the name of the app or game
driver = webdriver.Chrome()

# Navigate to the respective app store and search for the app/game
if user_choice.lower() == "ios":
    driver.get("https://www.apple.com/app-store/")
    # Write code to search for the app/game using the provided name on the iOS app store
    # Use appropriate Selenium commands to interact with the web page elements
else:
    driver.get("https://play.google.com/store")

    # Click on the search icon
    search_icon = driver.find_element(By.CSS_SELECTOR, '#kO001e > header > nav > div > div:nth-child(1) > button > i')
    search_icon.click()
    sleep(3)

    # Enter the app name in the search box
    search_box = driver.find_element(By.CSS_SELECTOR, '#kO001e > header > nav > c-wiz > div > div > label > input')
    search_box.send_keys(app_name)
    search_box.send_keys(Keys.RETURN)  # Press Enter key to trigger search
    sleep(8)

    # Wait for the search results to load
    # WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//div[@data-uitype="500"]')))

    # Click on the first search result
    search_results = driver.find_elements(By.XPATH, '//*[@id="yDmH0d"]/c-wiz[3]/div/div/c-wiz/c-wiz[1]/c-wiz/section/div/div/a')
    if search_results:
        search_results[0].click()
        sleep(20)
        # Wait for the app page to load
        # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "UD7Dzf")))

        See_all_reviews = driver.find_element(By.XPATH, "//span[contains(text(),'See all reviews')]")

        # Scroll to the button element using JavaScript
        driver.execute_script("window.scrollTo(0, arguments[0].getBoundingClientRect().top - window.innerHeight/2);",See_all_reviews)
        sleep(10)
        # Click the button
        See_all_reviews.click()
        sleep(20)


    else:
        print("App not found in the Google Play Store.")
        driver.quit()
        exit()


# Extract and print the reviews and the names of the reviewers
reviews = driver.find_elements(By.CLASS_NAME, 'h3YV2d')
reviewers = driver.find_elements(By.CLASS_NAME, 'X5PpBb')

# Initialize empty lists for each sentiment category
positive_reviews = []
negative_reviews = []
neutral_reviews = []

# Check if reviews and reviewers are found
if reviews and reviewers:
    # Process the reviews and categorize them
    for review, reviewer in zip(reviews, reviewers):
        sentiment = analyze_sentiment(review.text)
        if sentiment == 'Positive':
            positive_reviews.append((reviewer.text, review.text))
        elif sentiment == 'Negative':
            negative_reviews.append((reviewer.text, review.text))
        else:
            neutral_reviews.append((reviewer.text, review.text))

    # Print the positive reviews
    print("Positive Reviews:")
    for reviewer, review in positive_reviews:
        print(f"{reviewer}: {review}")
    print()

    # Print the negative reviews
    print("Negative Reviews:")
    for reviewer, review in negative_reviews:
        print(f"{reviewer}: {review}")
    print()

    # Print the neutral reviews
    print("Neutral Reviews:")
    for reviewer, review in neutral_reviews:
        print(f"{reviewer}: {review}")
else:
    print("Reviews not available for the specified app or game.")

# Close the web driver
driver.quit()
