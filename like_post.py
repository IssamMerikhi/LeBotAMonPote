import time
import os
import fileinput
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def save_credentials(username, password):
    with open("credentials.txt", "w") as file:
        file.write(f"{username}\n{password}")


def load_credentials():
    if not os.path.exists("credentials.txt"):
        return None

    with open("credentials.txt", "r") as file:
        lines = file.readlines()
        if len(lines) >= 2:
            return lines[0].strip(), lines[1].strip()

    return None


def prompt_credentials():
    username = input("Enter your Instagram username: ")
    password = input("Enter your Instagram password: ")
    save_credentials(username, password)
    return username, password


def read_usernames_from_file(file_path):
    with open(file_path, "r") as file:
        usernames = [line.strip() for line in file]
    return usernames

def remove_username_from_file(username, file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    with open(file_path, 'w') as file:
        for line in lines:
            if line.strip() != username:
                file.write(line)


def like_post(usernames):
    # Set up ChromeDriver options
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--start-maximized")

    # Set up ChromeDriver service
    service = Service(r'C:\Windows\chromedriver')

    # Set up ChromeDriver instance
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Log in to Instagram
    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(10)

    username_input = driver.find_element(By.CSS_SELECTOR, "input[name='username']")
    password_input = driver.find_element(By.CSS_SELECTOR, "input[name='password']")

    username_input.send_keys('forceandbonheur')
    password_input.send_keys('Solidarite2018')
    password_input.send_keys(Keys.RETURN)
    time.sleep(5)

    # Like stories of each follower
    for follower in usernames:
        story_url = f"https://www.instagram.com/{follower}"
        driver.get(story_url)
        time.sleep(10)

        posts_list = []
        post_button = driver.find_elements(By.XPATH, ".//a[contains(@href, '/p/')]")
        for post in post_button:
            posts_list.append(post.get_attribute('href'))
        print("posts : ", posts_list, " et taille de la liste : ", len(posts_list))


        for post in posts_list[:2]:     # va aimer les 2 premières publications normalement après y a moyen ça part en couilles
            driver.get(post)                    # html/body/div[4]/div/div/div[2]/div/div/div/div/div/div[2]/section/main/div/div[1]/div/div[1]
            # clique sur le bouton like         //*[@id='mount_0_0_bV']/div/div/div[3]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/section[1]/span[1]/div
            time.sleep(15)                      #/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/section[1]/span[1]/div
            driver.find_element(By.XPATH, "(//*[name()='svg' and @height='24' and @width='24'])[10]").click()
            # ActionChains(driver).double_click(WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "html/body/div[4]/div/div/div[2]/div/div/div/div/div/div[2]/section/main/div/div[1]/div/div[1]")))).perform()
            time.sleep(5)


    remove_username_from_file(follower, followers_file)

    # Close the ChromeDriver instance
    driver.quit()

if __name__ == "__main__":
    credentials = load_credentials()

    if credentials is None:
        username, password = prompt_credentials()
    else:
        username, password = credentials

    # Ajoutez ces lignes pour récupérer le chemin du fichier à partir de l'interface GUI :
    import sys
    if len(sys.argv) > 1:
        followers_file = sys.argv[1]
        usernames = read_usernames_from_file(followers_file)
    else:
        print("Veuillez fournir le chemin du fichier d'utilisateurs en tant qu'argument.")
        sys.exit(1)

    like_post(usernames)