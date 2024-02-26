import time  # Import the time module for time-related tasks
import os  # Import the os module to interact with the operating system
import undetected_chromedriver as uc  # Import undetected_chromedriver to bypass bot detection mechanisms in Selenium
from selenium.webdriver.common.keys import Keys  # Import Keys for keyboard key simulation
from selenium.webdriver.common.by import By  # Import By for locating elements by their attributes
from selenium.webdriver.support.ui import WebDriverWait  # Import WebDriverWait to wait for certain conditions
from selenium.webdriver.support import expected_conditions as EC  # Import expected_conditions to specify what to wait for
from getpass import getpass  # Import getpass to securely input the password without echoing it

# Prompt the user to enter their DataCamp email and password without showing the password on the screen
DATACAMP_EMAIL = input('Enter your DataCamp email: ')
DATACAMP_PASSWORD = getpass('Enter your DataCamp password: ')

# Prompt the user for the Google Chrome binary location with a default value
chrome_binary_location = input('Enter the Google Chrome binary location [/usr/bin/google-chrome-stable]: ') or "/usr/bin/google-chrome-stable"

# Configure options for ChromeDriver
options = uc.ChromeOptions()
options.binary_location = chrome_binary_location  # Use the user-specified location or the default
options.add_argument("--no-sandbox")  # Disable the sandbox for Chrome. Use with caution, especially in production environments

# Initialize ChromeDriver with undetected_chromedriver to prevent detection
driver = uc.Chrome(options=options)

# Open the specified DataCamp practice page
driver.get('https://practice.datacamp.com/p/591')

# Wait up to 30 seconds for the email input field to become clickable, then store the element in 'email_field'
email_field = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.ID, "user_email"))
)
email_field.send_keys(DATACAMP_EMAIL)  # Type the user's email into the email field

# Find the "Next" button by its CSS selector and click it to proceed to the password input
next_button = driver.find_element(By.CSS_SELECTOR, ".dc-btn.dc-btn--green.dc-btn--block.dc-account__next-btn.js-account-check-email")
next_button.click()

# Wait for the password field to become clickable, then store the element in 'password_field'
password_field = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.ID, "user_password"))
)
password_field.send_keys(DATACAMP_PASSWORD)  # Type the user's password into the password field

# Find the sign-in button by its name attribute and click it to log in
sign_in_button = driver.find_element(By.NAME, "commit")
sign_in_button.click()

# Record the start time to keep track of elapsed time
start_time = time.time()
escape_interval = 60  # Set an interval (in seconds) for how often to press the Escape key

# Brief pause to ensure the page has loaded
time.sleep(1.5)

try:
    while True:  # Start an infinite loop
        # Find the body element to send keyboard inputs. Re-finding it each time to avoid stale references
        body_element = driver.find_element(By.TAG_NAME, 'body')
        
        # Simulate pressing the Enter key three times with a short delay between each press
        for _ in range(3):
            body_element.send_keys(Keys.ENTER)
            time.sleep(0.1)

        # Re-find the body element in case the page has changed
        body_element = driver.find_element(By.TAG_NAME, 'body')

        # Simulate pressing the "1" key once
        body_element.send_keys('1')
        time.sleep(0.1)

        # Check if the set interval has passed to press the Escape key
        current_time = time.time()
        if current_time - start_time >= escape_interval:
            body_element = driver.find_element(By.TAG_NAME, 'body')  # Re-find the body element to ensure it's not stale
            body_element.send_keys(Keys.ESCAPE)  # Press the Escape key
            start_time = current_time  # Reset the start time for the next interval

except KeyboardInterrupt:
    # If a keyboard interrupt (Ctrl+C) is detected, exit the loop and end the script
    print("Stopping the script...")
