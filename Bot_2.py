import re
import os
import time
import random
import string
import imaplib
import email
import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"]
def extract_sec_code(email_address, email_password):
    options = webdriver.ChromeOptions()
    # random_user_agent = random.choice(user_agents)
    # options.add_argument(f'user-agent={random_user_agent}')
    # options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    try:
        driver.get('https://login.live.com/login.srf?wa=wsignin1.0&rpsnv=157&ct=1723061878&rver=7.0.6738.0&wp=MBI_SSL&wreply=https%3a%2f%2foutlook.live.com%2fowa%2f%3fnlp%3d1%26cobrandid%3dab0455a0-8d03-46b9-b18b-df2f57b9e44c%26deeplink%3dowa%252f%26RpsCsrfState%3d3ed97c09-c25b-ed4a-006c-e6ebeb4b3f89&id=292841&aadredir=1&CBCXT=out&lw=1&fl=dob%2cflname%2cwld&cobrandid=ab0455a0-8d03-46b9-b18b-df2f57b9e44c')
        wait = WebDriverWait(driver, 60)

        time.sleep(random.uniform(5, 7))
        email_input = wait.until(EC.presence_of_element_located((By.NAME, 'loginfmt')))
        email_input.clear()
        time.sleep(random.uniform(1, 2))
        
        for char in email_address:
            email_input.send_keys(char)
            time.sleep(random.uniform(0.1, 0.3))
        time.sleep(random.uniform(1, 2))
        
        driver.find_element(By.ID, 'idSIButton9').click()
        time.sleep(random.uniform(3, 5))

        password_input = wait.until(EC.presence_of_element_located((By.NAME, 'passwd')))
        time.sleep(random.uniform(1, 2))
        
        for char in email_password:
            password_input.send_keys(char)
            time.sleep(random.uniform(0.1, 0.3))
        time.sleep(random.uniform(1, 2))
        
        driver.find_element(By.ID, 'idSIButton9').click()
        time.sleep(random.uniform(3, 5))

        try:
            yes_button = wait.until(EC.element_to_be_clickable((By.ID, 'acceptButton')))
            time.sleep(random.uniform(1, 2))
            yes_button.click()
            time.sleep(random.uniform(2, 4))
        except TimeoutException:
            print("Stay signed in page did not appear.")

        print("Logged in successfully!")
        time.sleep(random.uniform(3, 5))

        try:
            div_element = WebDriverWait(driver, 90).until(EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@aria-label, 'Ankama security code')]")
            ))
        except TimeoutException:
            print("Ankama security code email not found.")
            return False

        time.sleep(random.uniform(1, 2))
        aria_label_text = div_element.get_attribute('aria-label')
        print("Aria-label text:", aria_label_text)

        pattern = r'nickname\s*:\s*(\w+)'
        match = re.search(pattern, aria_label_text)

        if match:
            code = match.group(1)
            print(f"Extracted code: {code}")
            return code
        else:
            print("Code not found.")

    except Exception as e:
        print(e)
    finally:
        time.sleep(random.uniform(2, 4))
        driver.quit()
def scroll_to_end(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

def check_for_error(driver):
    try:
        error_element = driver.find_element(By.CLASS_NAME, "alert-danger")
        error_message = error_element.text
        print(f"Error message detected: {error_message}")
        return True, error_message
    except NoSuchElementException:
        return False, ""

def login_to_dofus(email_address, email_password, password):
    options = webdriver.ChromeOptions()
    random_user_agent = random.choice(user_agents)
    options.add_argument(f'user-agent={random_user_agent}')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    try:
        driver.get('https://auth.ankama.com/login?client_id=0&code_challenge=aOSYe9tHRXjHSAkqddTls6RgZhnkLDndLjhx_dN9ks4&redirect_uri=https://account.ankama.com/authorized&origin_tracker=https%3A%2F%2Faccount.ankama.com%2Fen%2Faccount%2Finformation&direct')

        time.sleep(random.uniform(2, 4))

        ankama_connect_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.btn.btn-primary.btn-lg.w-100'))
        )
        ankama_connect_button.click()

        time.sleep(random.uniform(1, 3))

        email_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'login')))
        for char in email_address:
            email_input.send_keys(char)
            time.sleep(random.uniform(0.1, 0.3))
        time.sleep(random.uniform(1, 2))

        password_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'password')))
        for char in password:
            password_input.send_keys(char)
            time.sleep(random.uniform(0.1, 0.3))
        time.sleep(random.uniform(1, 2))

        driver.find_element(By.CSS_SELECTOR, 'button.btn.btn-lg.btn-primary.w-100').click()

        error_detected, error_message = check_for_error(driver)
        if error_detected:
            print(f"Aborting process due to error: {error_message}")
            return False, error_message

        time.sleep(random.uniform(3, 5))

        try:
            scroll_to_end(driver)
            continue_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btn.btn-lg.btn-primary.w-100[href^='https://account.ankama.com/authorized?code']"))
            )
            continue_button.click()
        except:
            print("1. Continue button not found.")

        time.sleep(random.uniform(2, 4))

        button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.ak-accept")))
        button.click()
        print("Logged into Dofus successfully!")

        time.sleep(random.uniform(2, 4))

        try:
            button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".ak-idbar-right .ak-nav-not-logged a[href*='account.ankama.com/webauth/authorize']")))
            button.click()

            time.sleep(random.uniform(2, 4))

            ankama_connect_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.btn.btn-primary.btn-lg.w-100'))
            )
            ankama_connect_button.click()

            time.sleep(random.uniform(1, 3))

            email_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'login')))
            for char in email_address:
                email_input.send_keys(char)
                time.sleep(random.uniform(0.1, 0.3))
            time.sleep(random.uniform(1, 2))

            password_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'password')))
            for char in password:
                password_input.send_keys(char)
                time.sleep(random.uniform(0.1, 0.3))
            time.sleep(random.uniform(1, 2))

            driver.find_element(By.CSS_SELECTOR, 'button.btn.btn-lg.btn-primary.w-100').click()

            time.sleep(random.uniform(3, 5))

            try:
                scroll_to_end(driver)
                continue_button = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btn.btn-lg.btn-primary.w-100[href^='https://account.ankama.com/authorized?code']"))
                )
                continue_button.click()
            except:
                print("1. Continue button not found.")

            print("Logged into Dofus successfully for second time!")
            try:
                button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.ak-accept")))
                button.click()
            except:
                pass

        except:
            pass

        time.sleep(random.uniform(2, 4))

        try:
            input_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'ak_field_1')))

            sec_code = extract_sec_code(email_address, email_password)
            if not sec_code:
                return True, "Security code not found."
            time.sleep(random.uniform(1, 3))
            input_field.clear()
            for char in sec_code:
                input_field.send_keys(char)
                time.sleep(random.uniform(0.1, 0.3))
            time.sleep(random.uniform(1, 2))
            confirm_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'input.btn.btn-primary.btn-lg'))
            )
            confirm_button.click()

            time.sleep(random.uniform(2, 4))

            button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'cancel')))
            button.click()

            time.sleep(random.uniform(2, 4))

            span_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'span.ak-edit-link')))
            span_element.click()

            time.sleep(random.uniform(2, 4))

            link_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btn.btn-primary.btn-sm")))
            link_element.click()

            sec_code = extract_sec_code(email_address, email_password)
            if not sec_code:
                return True, "Security code not found."
            time.sleep(random.uniform(1, 3))
            input_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'security_security')))
            input_field.clear()
            for char in sec_code:
                input_field.send_keys(char)
                time.sleep(random.uniform(0.1, 0.3))
            time.sleep(random.uniform(1, 2))
            confirm_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input.btn.btn-primary.btn-lg[type='submit']"))
            )        
            confirm_button.click()

            time.sleep(random.uniform(2, 4))

            link_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btn.btn-sm.btn-primary.ak-btn-home")))
            link_element.click()
            time.sleep(random.uniform(3, 5))
        except:
            print("Account already verified.")

        return True, None

    except Exception as e:
        print(e)
        return False, str(e)
    finally:
        driver.quit()

def load_names(filename):
    with open(filename, 'r') as file:
        names = [line.strip() for line in file if line.strip()]
    return names

def generate_realistic_name(names):
    if len(names) < 2:
        raise ValueError("Not enough names in the file.")
    first_name = random.choice(names)
    last_name = random.choice(names)
    return first_name, last_name

def create_dofus_account(email_address, email_password, names, signup_url):
    options = webdriver.ChromeOptions()
    random_user_agent = random.choice(user_agents)
    options.add_argument(f'user-agent={random_user_agent}')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.get(signup_url)
    time.sleep(random.uniform(2, 4))

    try:
        driver.find_element(By.CLASS_NAME, 'ui-button-text').click()
        time.sleep(random.uniform(1, 3))
    except Exception as e:
        print("Cookies popup not found or already closed", e)

    first_name, last_name = generate_realistic_name(names)
    birth_day = random.randint(1, 28)
    birth_month = random.randint(1, 12)
    birth_year = random.randint(1990, 2007)
    password = email_address.split('@')[0] + ''.join(random.choices(string.ascii_letters + string.digits, k=5))

    form_fields = [
        ('firstname', first_name),
        ('lastname', last_name),
        ('useremail', email_address),
        ('userpassword', password),
        ('user_password_confirm', password)
    ]

    for field, value in form_fields:
        element = driver.find_element(By.NAME, field)
        for char in value:
            element.send_keys(char)
            time.sleep(random.uniform(0.1, 0.3))
        time.sleep(random.uniform(1, 2))

    Select(driver.find_element(By.NAME, 'birth_day')).select_by_value(str(birth_day))
    time.sleep(random.uniform(1, 2))
    
    Select(driver.find_element(By.NAME, 'birth_month')).select_by_value(str(birth_month))
    time.sleep(random.uniform(1, 2))
    
    Select(driver.find_element(By.NAME, 'birth_year')).select_by_value(str(birth_year))
    time.sleep(random.uniform(1, 2))

    submit_button = driver.find_element(By.CSS_SELECTOR, 'input.btn.btn-primary.ak-btn-big.ak-submit')
    driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
    time.sleep(random.uniform(1, 2))
    submit_button.click()

    time.sleep(random.uniform(2, 4))

    try:
        progress_bar = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "progress-bar")))
        account_created = True
    except (TimeoutException, NoSuchElementException):
        account_created = False

    driver.quit()
    return account_created, password

def start(community_url, names_file='GAME_NAMES.txt'):
    if os.path.getsize('outlook_accounts.txt') == 0:
        print("No emails found! Aborting.")
        return

    with open('outlook_accounts.txt', 'r') as file:
        lines = file.readlines()
        copied_lines = lines.copy()

    names = load_names(names_file)
    
    for line in copied_lines:
        email_address, email_password = line.strip().split(':')
        account_created, password = create_dofus_account(email_address, email_password, names, community_url)
        #email_address, email_password, password="mohdfaizan21052@outlook.com","Lebron06*james","mohdfaizan21052qAryX"
        if not account_created:
            print("Dofus account not created, removing email from txt file")
            lines.remove(line)
        else:
            print("Dofus Account Created")
            #logged_in, reason = login_to_dofus(email_address, email_password, password)
            logged_in, reason = login_to_dofus(email_address, email_password, password)
            if not logged_in:
                print("Dofus account not logging in, removing email from txt file")
                lines.remove(line)
            else:
                if reason != None:
                    print("DoFus account logging in completed but 'Ankama Shield' could not be deactivated as security code not found")
                else:
                    print("DoFus account logging in completed and 'Ankama Shield' deactivated")
                    # Save verified account to new file
                    with open('verified_accounts.txt', 'a') as verified_file:
                        verified_file.write(f"{email_address}:{email_password}\n")
                    # Save successful account to success.txt
                    with open('success.txt', 'a') as success_file:
                        success_file.write(f"{email_address}:{password}\n")
                    print(f"Account {email_address} has been successfully processed and saved to success.txt")
                # Remove from outlook_accounts.txt
                lines.remove(line)
        
        # Write the updated lines back to the file
        with open('outlook_accounts.txt', 'w') as file:
            file.writelines(lines)

# Streamlit interface for the second bot
def dofus_bot_interface():
    st.title("Dofus Touch Account Creation Bot")
    community_choice = st.radio("Choose Community", ("FR", "ENG", "ES"))
    
    if community_choice == "FR":
        community_url = "https://account.ankama.com/fr/creer-un-compte"
    elif community_choice == "ENG":
        community_url = "https://account.ankama.com/en/account-creation"
    else:
        community_url = "https://account.ankama.com/es/crear-cuenta"

    if st.button("Start Bot"):
        start(community_url, 'GAME_NAMES.txt')

if __name__ == "__main__":
    dofus_bot_interface()