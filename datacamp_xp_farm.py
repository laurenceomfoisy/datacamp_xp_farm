import time
import os
import undetected_chromedriver as uc
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from getpass import getpass

DATACAMP_EMAIL = input('Enter your DataCamp email: ')
DATACAMP_PASSWORD = getpass('Enter your DataCamp password: ')

# Start the Chrome Driver with undetected_chromedriver
options = uc.ChromeOptions()

# Adding necessary options
options.binary_location = "/usr/bin/google-chrome-stable"
options.add_argument("--no-sandbox")  # Necessary for running Chrome as root in Docker/CI environments, but be cautious using it

# Start the Chrome Driver with specified options
driver = uc.Chrome(options=options)

# Navigate to the second website
driver.get('https://practice.datacamp.com/p/591')

# Wait for the email field to be clickable
email_field = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.ID, "user_email"))
)
email_field.send_keys(DATACAMP_EMAIL)  # Replace with the email you want to use for login

# Locate the "Next" button using its class attributes
next_button = driver.find_element(By.CSS_SELECTOR, ".dc-btn.dc-btn--green.dc-btn--block.dc-account__next-btn.js-account-check-email")
next_button.click()


password_field = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.ID, "user_password"))
) 
password_field.send_keys(DATACAMP_PASSWORD) 

sign_in_button = driver.find_element(By.NAME, "commit")
sign_in_button.click()

# Initialize the timer
start_time = time.time()  # Current time when the loop starts
escape_interval = 60  # 60 seconds

time.sleep(1.5)

try:
    while True:
        # Re-find the body element in each iteration to avoid StaleElementReferenceException
        body_element = driver.find_element(By.TAG_NAME, 'body')
        
        # Press Enter 3 times
        for _ in range(3):
            body_element.send_keys(Keys.ENTER)
            time.sleep(0.1)  # Adjust sleep time as necessary

        # Re-find the body element again as the page state might have changed
        body_element = driver.find_element(By.TAG_NAME, 'body')

        # Press "1" once
        body_element.send_keys('1')
        time.sleep(0.1)  # Adjust sleep time as necessary

        # Check if 5 minutes have passed to press Escape
        current_time = time.time()
        if current_time - start_time >= escape_interval:
            # Re-find the body element again as the page state might have changed
            body_element = driver.find_element(By.TAG_NAME, 'body')
            body_element.send_keys(Keys.ESCAPE)
            start_time = current_time  # Reset the timer

except KeyboardInterrupt:
    # Stop the loop when a keyboard interrupt (Ctrl+C) is detected
    print("Stopping the script...")